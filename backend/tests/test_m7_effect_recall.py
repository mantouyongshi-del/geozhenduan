"""M7.2 发布效果回采：01 侧 latest / recall 端点离线测试。

- DB 通过 dependency_overrides 指向临时 SQLite，绝不污染本机 geo_system.db；
- 重体检路径 monkeypatch DiagnosticService，只验证「同口径复用」契约本身；
- 零真实网络。
"""
from __future__ import annotations

import asyncio
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as app_database
from app.core.database import Base, get_db
from main import app
from app.models.diagnostic import DiagnosticReport
from app.schemas.diagnostic import DiagnosticReportOut
from app.services.diagnostic_service import DiagnosticService

USCC = "91430100MA4L2X8K3T"


@pytest.fixture()
def db_client():
    """独立临时库 + get_db 依赖覆写，全程隔离真实库。"""
    tmpdir = Path(tempfile.mkdtemp(prefix="xl-m72-"))
    engine = create_engine(f"sqlite:///{tmpdir / 'diag.db'}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def _override():
        session = factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _override
    try:
        with TestClient(app) as client:
            yield client, factory
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()
        shutil.rmtree(tmpdir, ignore_errors=True)


def seed_report(factory, *, code: str, uscc: Optional[str] = USCC, **overrides: Any) -> DiagnosticReport:
    row = DiagnosticReport(
        report_code=code,
        target_company=overrides.get("target_company", "长沙岳麓万豪酒店管理有限公司"),
        brand_name=overrides.get("brand_name", "长沙岳麓万豪酒店"),
        industry=overrides.get("industry", "酒店住宿"),
        city=overrides.get("city", "长沙"),
        uscc=uscc,
        search_keywords_json=overrides.get(
            "search_keywords_json", json.dumps(["长沙岳麓万豪酒店 怎么样"], ensure_ascii=False)
        ),
        summary_verdict=overrides.get("summary_verdict", "E2E 回采基线样本"),
        visibility_score=overrides.get("visibility_score", 15),
        risk_level=overrides.get("risk_level", "HIGH_RISK"),
        competitors_json=overrides.get("competitors_json", "[]"),
        prescriptions_json=overrides.get("prescriptions_json", "[]"),
    )
    session = factory()
    try:
        session.add(row)
        session.commit()
        session.refresh(row)
    finally:
        session.close()
    return row


def make_report_out(code: str) -> DiagnosticReportOut:
    return DiagnosticReportOut(
        id=999,
        report_code=code,
        target_company="长沙岳麓万豪酒店管理有限公司",
        brand_name="长沙岳麓万豪酒店",
        industry="酒店住宿",
        city="长沙",
        uscc=USCC,
        search_keywords=["长沙岳麓万豪酒店 怎么样"],
        agency_name="蜉蝣小宝",
        visibility_score=66,
        risk_level="MEDIUM_RISK",
        summary_verdict="回采样本",
        competitors=[],
        prescriptions=[],
        items=[],
        consultant_name="资深数字化顾问",
        created_at=1,
    )


# ------------------------------------------------------------------ latest


def test_latest_requires_at_least_one_param(db_client):
    client, _ = db_client
    resp = client.get("/api/v1/diagnostic/latest")
    assert resp.status_code == 400
    assert "至少" in resp.json()["detail"]


def test_latest_matches_by_uscc_and_prefers_newest(db_client):
    client, factory = db_client
    seed_report(factory, code="GEO-BASE-1")
    seed_report(factory, code="GEO-BASE-2", visibility_score=42)

    resp = client.get("/api/v1/diagnostic/latest", params={"uscc": USCC})
    assert resp.status_code == 200
    body = resp.json()
    assert body["report_code"] == "GEO-BASE-2"  # id 更大者胜
    assert body["visibility_score"] == 42
    assert body["uscc"] == USCC


def test_latest_falls_back_to_company_then_brand(db_client):
    client, factory = db_client
    seed_report(factory, code="GEO-BASE-C", uscc=None)

    # uscc 未命中 -> target_company 命中
    resp = client.get(
        "/api/v1/diagnostic/latest", params={"uscc": USCC, "company": "长沙岳麓万豪酒店管理有限公司"}
    )
    assert resp.status_code == 200
    assert resp.json()["report_code"] == "GEO-BASE-C"

    # company 也未命中 -> brand_name 兜底
    resp2 = client.get("/api/v1/diagnostic/latest", params={"brand": "长沙岳麓万豪酒店"})
    assert resp2.status_code == 200
    assert resp2.json()["report_code"] == "GEO-BASE-C"


def test_latest_returns_404_when_no_match(db_client):
    client, factory = db_client
    seed_report(factory, code="GEO-BASE-X")
    resp = client.get("/api/v1/diagnostic/latest", params={"uscc": "91110000MA01ABCD2X"})
    assert resp.status_code == 404


def test_latest_is_pure_read_and_includes_platform_items(db_client):
    """零误杀负向：latest 是只读端点，查询后报告数不变。"""
    client, factory = db_client
    seed_report(factory, code="GEO-BASE-R")
    session = factory()
    try:
        before = session.query(DiagnosticReport).count()
    finally:
        session.close()
    resp = client.get("/api/v1/diagnostic/latest", params={"uscc": USCC})
    assert resp.status_code == 200
    assert "items" in resp.json()
    session = factory()
    try:
        after = session.query(DiagnosticReport).count()
    finally:
        session.close()
    assert before == after


# ------------------------------------------------------------------ recall


def test_recall_rejects_bad_report_code(db_client):
    client, _ = db_client
    resp = client.post("/api/v1/diagnostic/short/recall")  # 5 位，不满足白名单 {6,50}
    assert resp.status_code == 400


def test_recall_unknown_code_returns_404(db_client):
    client, _ = db_client
    resp = client.post("/api/v1/diagnostic/GEO-NOPE-404/recall")
    assert resp.status_code == 404


def test_recall_reuses_original_payload_verbatim(db_client):
    """核心契约：回采必须用原报告的 同企业/关键词/城市/USCC，保证前后可比。"""
    client, factory = db_client
    old = seed_report(
        factory,
        code="GEO-OLD-1",
        search_keywords_json=json.dumps(["长沙岳麓万豪酒店 推荐", "岳麓区酒店"], ensure_ascii=False),
        city="长沙",
        uscc=USCC,
    )
    captured: Dict[str, Any] = {}

    async def fake_execute(payload, db):  # noqa: ANN001
        captured["payload"] = payload
        return old

    monkey_out = make_report_out("GEO-NEW-9")
    saved_exec = DiagnosticService.execute_diagnostic
    saved_out = DiagnosticService.get_report_by_code
    DiagnosticService.execute_diagnostic = staticmethod(fake_execute)
    DiagnosticService.get_report_by_code = classmethod(lambda cls, code, db: monkey_out)
    try:
        resp = client.post("/api/v1/diagnostic/GEO-OLD-1/recall")
    finally:
        DiagnosticService.execute_diagnostic = saved_exec
        DiagnosticService.get_report_by_code = saved_out

    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["report_code"] == "GEO-NEW-9"  # 产出全新报告
    payload = captured["payload"]
    assert payload.target_company == "长沙岳麓万豪酒店管理有限公司"
    assert payload.brand_name == "长沙岳麓万豪酒店"
    assert payload.industry == "酒店住宿"
    assert payload.city == "长沙"
    assert list(payload.keywords) == ["长沙岳麓万豪酒店 推荐", "岳麓区酒店"]
    assert payload.uscc == USCC

    # 原报告一动不动
    session = factory()
    try:
        row = session.query(DiagnosticReport).filter_by(report_code="GEO-OLD-1").one()
        assert row.visibility_score == 15
        assert session.query(DiagnosticReport).count() == 1
    finally:
        session.close()


def test_recall_of_report_without_keywords_is_422(db_client):
    client, factory = db_client
    seed_report(factory, code="GEO-NOKW", search_keywords_json="[]")
    resp = client.post("/api/v1/diagnostic/GEO-NOKW/recall")
    assert resp.status_code == 422
    assert "关键词" in resp.json()["detail"]


def test_recall_survives_executor_failure_as_500(db_client):
    client, factory = db_client
    seed_report(factory, code="GEO-BOOM")

    async def boom(payload, db):  # noqa: ANN001
        raise RuntimeError("LLM 集群爆炸")

    saved = DiagnosticService.execute_diagnostic
    DiagnosticService.execute_diagnostic = staticmethod(boom)
    try:
        resp = client.post("/api/v1/diagnostic/GEO-BOOM/recall")
    finally:
        DiagnosticService.execute_diagnostic = saved
    assert resp.status_code == 500
    assert "回采" in resp.json()["detail"]


def test_recall_does_not_auto_dispatch_or_sync(db_client):
    """回采是度量动作：即使自动下发/回流开关全开，也不得触发下游副作用。"""
    client, factory = db_client
    old = seed_report(factory, code="GEO-SIDE")
    dispatched, synced = [], []

    async def fake_exec(payload, db):  # noqa: ANN001
        return old

    saved_exec = DiagnosticService.execute_diagnostic
    saved_out = DiagnosticService.get_report_by_code
    DiagnosticService.execute_diagnostic = staticmethod(fake_exec)
    DiagnosticService.get_report_by_code = classmethod(lambda cls, code, db: make_report_out(code))
    import app.api.v1.endpoints.diagnostic as diag_mod

    saved_dispatch, saved_sync = diag_mod.schedule_auto_dispatch, diag_mod.schedule_auto_sync
    diag_mod.schedule_auto_dispatch = lambda report: dispatched.append(report)
    diag_mod.schedule_auto_sync = lambda report: synced.append(report)
    try:
        resp = client.post("/api/v1/diagnostic/GEO-SIDE/recall")
    finally:
        DiagnosticService.execute_diagnostic = saved_exec
        DiagnosticService.get_report_by_code = saved_out
        diag_mod.schedule_auto_dispatch = saved_dispatch
        diag_mod.schedule_auto_sync = saved_sync

    assert resp.status_code == 200, resp.text
    assert dispatched == [] and synced == []
