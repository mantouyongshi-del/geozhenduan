"""模型 / API / 分发主键优先级 离线测试套件。

- 分发主键优先级：用 httpx.MockTransport 记录实际发出的请求 body，断言 brand_id。
- API 层：通过依赖注入把 get_db 重定向到**独立临时 SQLite**，从而验证真实端点接线
  （含响应模型序列化 uscc），同时保证本机 geo_system.db 不被写脏。

异步协程在同步测试函数内用 asyncio.run(...) 驱动（本 venv 无 pytest-asyncio）。
"""
from __future__ import annotations

import asyncio
import json
import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.core.migrations import ensure_schema
from app.core.uscc import complete_uscc
from app.models.company import Company
from app.models.diagnostic import DiagnosticReport
from app.services.distribution_client import DistributionClient
from tests.conftest import FakeReport, FakeTask, make_handler, make_transport

VALID_USCC = complete_uscc("91430100MA4L2X8K3")  # 91430100MA4L2X8K3T
FALLBACK_KEY = "长沙岳麓万豪酒店管理有限公司::长沙"


# ===========================================================================
# 一、dispatch_report 三档主键优先级（单元级，MockTransport 记录 body）
# ===========================================================================
def _captured_brand_id(report, *, brand_id=None):
    records: list = []
    handler = make_handler(record=records, status=200, json_body={"items": []})
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    asyncio.run(client.dispatch_report(report, brand_id=brand_id))
    assert records, "应当至少发出一次请求"
    payload = json.loads(records[0]["content"])
    return payload["brand_id"]


def test_priority_fallback_when_no_uscc():
    """① report.uscc 为空且未显式指定 → 降级键 `{企业全称}::{城市}`。"""
    report = FakeReport(
        target_company="长沙岳麓万豪酒店管理有限公司",
        city="长沙",
        uscc=None,
        geo_tasks=[FakeTask("T1")],
    )
    assert _captured_brand_id(report) == FALLBACK_KEY


def test_priority_uscc_when_report_has_valid():
    """② report.uscc 为合法 USCC → 发出的 brand_id 等于该 USCC。"""
    report = FakeReport(
        target_company="长沙岳麓万豪酒店管理有限公司",
        city="长沙",
        uscc=VALID_USCC,
        geo_tasks=[FakeTask("T1")],
    )
    assert _captured_brand_id(report) == VALID_USCC


def test_priority_explicit_overrides_uscc():
    """③ brand_id 显式指定 → 显式值优先于 report.uscc。"""
    report = FakeReport(
        target_company="长沙岳麓万豪酒店管理有限公司",
        city="长沙",
        uscc=VALID_USCC,
        geo_tasks=[FakeTask("T1")],
    )
    assert _captured_brand_id(report, brand_id="EXPLICIT-BRAND-ID") == "EXPLICIT-BRAND-ID"


def test_priority_dirty_uscc_falls_back():
    """④ report.uscc 是脏数据（形态检查不过）→ 回落降级键（防御历史脏数据）。"""
    report = FakeReport(
        target_company="长沙岳麓万豪酒店管理有限公司",
        city="长沙",
        uscc="NOT-A-USCC",  # 含连字符、长度不对，必然过不了 is_uscc_format
        geo_tasks=[FakeTask("T1")],
    )
    assert _captured_brand_id(report) == FALLBACK_KEY


# ===========================================================================
# 二、API 层（依赖注入重定向到临时 SQLite，绝不写脏本机 geo_system.db）
# ===========================================================================
@pytest.fixture
def api_env():
    """构建 TestClient，并将 get_db 重定向到独立临时库（含 uscc 列）。"""
    from main import app  # noqa: WPS433 — 任务指定入口模块名 main

    d = tempfile.mkdtemp(prefix="uscc_api_")
    path = os.path.join(d, "test_geo_system.db")
    eng = create_engine(f"sqlite:///{path}")
    Base.metadata.create_all(bind=eng)
    ensure_schema(eng)  # 幂等；uscc 列已随 create_all 建好

    TestingSessionLocal = sessionmaker(bind=eng, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        yield client, eng
    finally:
        app.dependency_overrides.clear()
        eng.dispose()


def test_api_create_company_with_valid_uscc(api_env):
    """POST /companies/ 带合法 uscc → 200 且响应 uscc 等于该值。"""
    client, _ = api_env
    resp = client.post(
        "/api/v1/companies/",
        json={"name": "测试企业A", "brand_aliases": "测试企业A", "uscc": VALID_USCC},
    )
    assert resp.status_code == 200
    assert resp.json()["uscc"] == VALID_USCC


def test_api_create_company_with_illegal_uscc_422(api_env):
    """POST /companies/ 带非法 uscc → 422（不是 500、不是 400）。"""
    client, _ = api_env
    resp = client.post(
        "/api/v1/companies/",
        json={"name": "测试企业B", "brand_aliases": "测试企业B", "uscc": "123"},
    )
    assert resp.status_code == 422
    assert "统一社会信用代码" in resp.json()["detail"]


def test_api_create_company_without_uscc_null(api_env):
    """零误杀负向：不带 uscc → 200 且响应 uscc 为 null（可选字段不填必须一切正常）。"""
    client, _ = api_env
    resp = client.post(
        "/api/v1/companies/",
        json={"name": "测试企业C", "brand_aliases": "测试企业C"},
    )
    assert resp.status_code == 200
    assert resp.json()["uscc"] is None


def test_api_list_companies_has_uscc_key(api_env):
    """GET /companies/ 返回的条目含 uscc 键。"""
    client, _ = api_env
    client.post(
        "/api/v1/companies/",
        json={"name": "测试企业D", "brand_aliases": "测试企业D", "uscc": VALID_USCC},
    )
    resp = client.get("/api/v1/companies/")
    assert resp.status_code == 200
    items = resp.json()
    assert items, "列表不应为空"
    for item in items:
        assert "uscc" in item
    assert items[0]["uscc"] == VALID_USCC


def test_api_diagnostic_run_illegal_uscc_422(api_env):
    """POST /diagnostic/run 带非法 uscc → 422。

    重点回归：该端点有吞异常的兜底（except Exception -> 500），
    必须证明 uscc 校验发生在兜底之前（返回 422 而非 500）。
    同时传入合法 keywords，确保 422 由 uscc 引起而非关键词校验。
    """
    client, _ = api_env
    resp = client.post(
        "/api/v1/diagnostic/run",
        json={
            "target_company": "长沙岳麓万豪酒店管理有限公司",
            "brand_name": "万豪",
            "industry": "酒店",
            "city": "长沙",
            "keywords": ["万豪酒店 口碑怎么样"],
            "uscc": "123",  # 非法：长度不对
        },
    )
    assert resp.status_code == 422, f"期望 422 而非 {resp.status_code}: {resp.text}"
    assert "统一社会信用代码" in resp.json()["detail"]


def test_api_diagnostic_recent_list_has_uscc_key(api_env):
    """GET /diagnostic/recent/list 每条记录含 uscc 键（向临时库插入一条带 uscc 的报告）。"""
    client, eng = api_env
    Session = sessionmaker(bind=eng)
    with Session() as s:
        s.add(
            DiagnosticReport(
                report_code="R-USCC-001",
                target_company="测试企业E",
                brand_name="测试",
                industry="科技",
                city="长沙",
                uscc=VALID_USCC,
                search_keywords_json="[]",
                summary_verdict="一句话痛点诊断结论",
            )
        )
        s.commit()

    resp = client.get("/api/v1/diagnostic/recent/list")
    assert resp.status_code == 200
    items = resp.json()
    assert items, "列表不应为空"
    for item in items:
        assert "uscc" in item
    assert items[0]["uscc"] == VALID_USCC
