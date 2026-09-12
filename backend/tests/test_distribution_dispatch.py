"""跨仓工单下发 —— 离线测试套件。

全部用例离线：网络仅通过 httpx.MockTransport 注入。
异步协程在同步测试函数内用 asyncio.run(...) 驱动（本 venv 无 pytest-asyncio）。
"""
from __future__ import annotations

import asyncio
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from app.services.distribution_client import DistributionClient, auto_dispatch_report
from app.schemas.distribution import DispatchBatchResult, DistributionStatus
from app.schemas.diagnostic import GeoActionTask

from tests.conftest import (
    FakeTask,
    FakeReport,
    FakeSleep,
    FakeDistributionClient,
    make_handler,
    make_transport,
)


# ===========================================================================
# 一、dispatch_task 单条下发
# ===========================================================================
def test_dispatch_task_unconfigured_sends_zero_requests():
    """未配置时一次网络请求都不发，直接降级。"""
    calls: list = []
    handler = make_handler(record=calls, status=200, json_body={"items": []})
    client = DistributionClient(
        base_url="", enabled=False, transport=make_transport(handler)
    )
    assert client.configured is False

    result = asyncio.run(
        client.dispatch_task({"brand_id": "B"}, task_id="T1")
    )
    assert calls == []  # 硬性要求：零网络前置
    assert result.degraded is True
    assert result.ok is False
    assert result.reason == "下游分发系统未启用或未配置"


def test_dispatch_task_no_token_header_absent():
    """token 为空时，请求头不得包含 X-Internal-Token。"""
    calls: list = []
    handler = make_handler(record=calls, status=200, json_body={"items": []})
    client = DistributionClient(
        base_url="http://dist", token="", transport=make_transport(handler)
    )
    asyncio.run(client.dispatch_task({"brand_id": "B"}, task_id="T1"))

    assert calls, "应当至少发出一次请求"
    headers = calls[0]["headers"]
    # httpx 头键统一小写化，做大小写不敏感断言
    assert "x-internal-token" not in {k.lower() for k in headers}  # 双向断言：空 token 不存在


def test_dispatch_task_token_header_present_and_equal():
    """token 非空时，请求头 X-Internal-Token 必须等于该值。"""
    calls: list = []
    handler = make_handler(record=calls, status=200, json_body={"items": []})
    client = DistributionClient(
        base_url="http://dist", token="s3cr3t", transport=make_transport(handler)
    )
    asyncio.run(client.dispatch_task({"brand_id": "B"}, task_id="T1"))

    headers = calls[0]["headers"]
    assert headers.get("x-internal-token") == "s3cr3t"  # 双向断言：非空 token 等于
    assert headers.get("content-type") == "application/json"


def test_dispatch_task_200_ok_negative_case_no_false_kill():
    """零误杀负向用例：完全正常的工单必须 ok=True、created=True。

    下游返回 {"total":1,"created":1,...items:[{task_id:"T1",status:"pending",created:true}]}
    """
    body = {
        "total": 1,
        "created": 1,
        "updated": 0,
        "items": [
            {
                "brand_id": "B",
                "task_id": "T1",
                "status": "pending",
                "created": True,
                "record": {"foo": "bar"},
            }
        ],
    }
    handler = make_handler(status=200, json_body=body)
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    result = asyncio.run(
        client.dispatch_task({"brand_id": "B"}, task_id="T1")
    )
    assert result.ok is True
    assert result.degraded is False
    assert result.status == "pending"
    assert result.created is True
    assert result.attempts == 1


def test_dispatch_task_200_match_by_task_id_items0_fallback():
    """响应 items 不匹配 task_id 时，回退取 items[0]。"""
    body = {"items": [{"task_id": "OTHER", "status": "queued", "created": False}]}
    handler = make_handler(status=200, json_body=body)
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    result = asyncio.run(
        client.dispatch_task({"brand_id": "B"}, task_id="T1")
    )
    assert result.ok is True
    assert result.status == "queued"
    assert result.created is False


def test_dispatch_task_retry_backoff_no_real_wait():
    """非 200 时按 0.5*2**(n-1) 退避重试，注入假 sleep 确保零真实等待。"""
    sleep = FakeSleep()
    handler = make_handler(status=500, json_body={"detail": "boom"})
    client = DistributionClient(
        base_url="http://dist",
        max_retries=3,
        sleep=sleep,
        transport=make_transport(handler),
    )
    started = time.perf_counter()
    result = asyncio.run(
        client.dispatch_task({"brand_id": "B"}, task_id="T1")
    )
    elapsed = time.perf_counter() - started

    # max_retries=3 -> 失败 3 次，退避发生在第 1、2 次失败后：0.5, 1.0
    assert sleep.calls == [0.5, 1.0]
    assert result.ok is False
    assert result.degraded is True
    assert result.attempts == 3
    assert elapsed < 0.5  # 整个过程远小于真实退避（1.5s）


def test_dispatch_task_succeeds_on_third_attempt():
    """前两次 500、第三次 200：attempts 记录为成功时的第 3 次。"""
    sleep = FakeSleep()
    state = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        state["n"] += 1
        if state["n"] < 3:
            return httpx.Response(500, json={"detail": "retry"})
        return httpx.Response(200, json={"items": [{"task_id": "T1", "status": "pending", "created": True}]})

    client = DistributionClient(
        base_url="http://dist", max_retries=3, sleep=sleep,
        transport=make_transport(handler),
    )
    result = asyncio.run(client.dispatch_task({"brand_id": "B"}, task_id="T1"))
    assert result.ok is True
    assert result.attempts == 3  # 真实尝试次数
    assert result.created is True


def test_dispatch_task_connect_error_degraded_no_raise():
    """底层抛 ConnectError 时绝不向上抛，收敛为降级结果。"""
    handler = make_handler(raise_exc=httpx.ConnectError("connection refused"))
    client = DistributionClient(
        base_url="http://dist", max_retries=2,
        transport=make_transport(handler),
    )
    # 若实现违反红线抛异常，此处会冒泡为测试错误
    result = asyncio.run(client.dispatch_task({"brand_id": "B"}, task_id="T1"))
    assert result.ok is False
    assert result.degraded is True
    assert "ConnectError" in result.reason


# ===========================================================================
# 二、probe 连通性探测
# ===========================================================================
def test_probe_unconfigured_sends_zero_requests():
    calls: list = []
    handler = make_handler(record=calls, status=200, json_body={})
    client = DistributionClient(
        base_url="", enabled=False, transport=make_transport(handler)
    )
    status = asyncio.run(client.probe())
    assert calls == []
    assert status.reachable is False
    assert status.configured is False


def test_probe_reachable_true_on_200():
    handler = make_handler(status=200, json_body={"status": "ok"})
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    status = asyncio.run(client.probe())
    assert status.reachable is True
    assert status.detail == "HTTP 200"


def test_probe_unreachable_no_raise():
    handler = make_handler(raise_exc=httpx.ConnectError("down"))
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    status = asyncio.run(client.probe())
    assert status.reachable is False  # 异常只报不可达，不抛


# ===========================================================================
# 三、build_brand_id 主键构造
# ===========================================================================
def test_build_brand_id_explicit_stripped():
    assert DistributionClient.build_brand_id("X", city="深圳", explicit="  USCC123  ") == "USCC123"


def test_build_brand_id_fallback_with_city():
    assert DistributionClient.build_brand_id("示例科技有限公司", city="深圳") == "示例科技有限公司::深圳"


def test_build_brand_id_fallback_city_empty_uses_nationwide():
    assert DistributionClient.build_brand_id("示例科技有限公司", city="") == "示例科技有限公司::全国"
    assert DistributionClient.build_brand_id("示例科技有限公司", city="   ") == "示例科技有限公司::全国"


# ===========================================================================
# 四、dispatch_report 批量下发 + auto_dispatch_report
# ===========================================================================
def test_dispatch_report_counts_total_succeeded_degraded():
    """混合结果：统计 total / succeeded / degraded。"""
    body_ok = {
        "items": [{"task_id": "T1", "status": "pending", "created": True}]
    }
    body_fail = {"items": []}

    def handler(request: httpx.Request) -> httpx.Response:
        # 按 body 中的 brand_id 之外的 task_id 无法区分，这里用 content 判断
        # 简化：奇数次成功、偶数次失败
        handler.n += 1  # type: ignore[attr-defined]
        if handler.n % 2 == 1:  # type: ignore[attr-defined]
            return httpx.Response(200, json=body_ok)
        return httpx.Response(500, json=body_fail)

    handler.n = 0  # type: ignore[attr-defined]

    report = FakeReport(
        geo_tasks=[FakeTask("T1"), FakeTask("T2"), FakeTask("T3")]
    )
    client = DistributionClient(
        base_url="http://dist", max_retries=1,
        transport=make_transport(handler),
    )
    batch = asyncio.run(client.dispatch_report(report))
    assert batch.total == 3
    # T1 ok, T2 fail, T3 ok -> succeeded=2, degraded=1
    assert batch.succeeded == 2
    assert batch.degraded == 1
    assert batch.brand_id == "示例科技有限公司::深圳"


def test_dispatch_report_filters_by_task_ids():
    """task_ids 给出时只下发匹配工单。"""
    calls: list = []
    handler = make_handler(record=calls, status=200,
                           json_body={"items": [{"task_id": "T1", "status": "pending", "created": True}]})
    report = FakeReport(geo_tasks=[FakeTask("T1"), FakeTask("T2"), FakeTask("T3")])
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    batch = asyncio.run(client.dispatch_report(report, task_ids=["T1", "T2"]))
    assert batch.total == 2
    assert batch.succeeded == 2
    sent_ids = {c["content"] for c in calls}
    # 仅 T1/T2 被下发（payload 内 task.id 体现在 JSON 中）
    import json
    payloads = [json.loads(c) for c in (x["content"] for x in calls)]
    ids = {p["task"]["id"] for p in payloads}
    assert ids == {"T1", "T2"}


def test_auto_dispatch_unconfigured_returns_none_no_network():
    calls: list = []
    handler = make_handler(record=calls, status=200, json_body={"items": []})
    client = DistributionClient(
        base_url="", enabled=False, transport=make_transport(handler)
    )
    # 临时替换模块单例
    import app.services.distribution_client as dc_mod
    saved = dc_mod.distribution_client
    dc_mod.distribution_client = client
    try:
        out = asyncio.run(auto_dispatch_report(FakeReport(geo_tasks=[FakeTask("T1")])))
    finally:
        dc_mod.distribution_client = saved
    assert out is None
    assert calls == []


def test_auto_dispatch_configured_returns_batch():
    handler = make_handler(status=200,
                           json_body={"items": [{"task_id": "T1", "status": "pending", "created": True}]})
    client = DistributionClient(
        base_url="http://dist", transport=make_transport(handler)
    )
    import app.services.distribution_client as dc_mod
    saved = dc_mod.distribution_client
    dc_mod.distribution_client = client
    try:
        out = asyncio.run(auto_dispatch_report(FakeReport(geo_tasks=[FakeTask("T1")])))
    finally:
        dc_mod.distribution_client = saved
    assert isinstance(out, DispatchBatchResult)
    assert out.succeeded == 1


def test_auto_dispatch_swallows_exception_returns_none():
    """自动下发内部异常被吞掉返回 None，不反噬主流程。"""
    import app.services.distribution_client as dc_mod

    class BoomClient(DistributionClient):
        async def dispatch_report(self, report, *, brand_id=None, task_ids=None):
            raise RuntimeError("downstream exploded")

    client = BoomClient(base_url="http://dist", transport=make_transport(
        make_handler(status=200, json_body={"items": []})
    ))
    saved = dc_mod.distribution_client
    dc_mod.distribution_client = client
    try:
        out = asyncio.run(auto_dispatch_report(FakeReport(geo_tasks=[FakeTask("T1")])))
    finally:
        dc_mod.distribution_client = saved
    assert out is None


# ===========================================================================
# 五、API 层（TestClient 驱动 main:app）
# ===========================================================================
@pytest.fixture
def client():
    from main import app
    return TestClient(app)


def test_api_dispatch_404_when_report_missing(client):
    """报告不存在 -> 404（直接 POST 不存在的 report_code，无需 monkeypatch）。"""
    resp = client.post(
        "/api/v1/distribution/dispatch",
        json={"report_code": "DOES-NOT-EXIST"},
    )
    assert resp.status_code == 404


def test_api_dispatch_422_when_no_tasks(client, monkeypatch):
    """报告存在但 geo_tasks 为空 -> 422。"""
    import app.api.v1.endpoints.distribution as dist_ep
    import app.services.diagnostic_service as ds_mod

    monkeypatch.setattr(
        ds_mod.DiagnosticService, "get_report_by_code",
        lambda code, db: FakeReport(report_code=code, geo_tasks=[]),
    )
    saved = dist_ep.distribution_client
    dist_ep.distribution_client = FakeDistributionClient()
    try:
        resp = client.post(
            "/api/v1/distribution/dispatch",
            json={"report_code": "R-EMPTY"},
        )
    finally:
        dist_ep.distribution_client = saved
    assert resp.status_code == 422


def test_api_dispatch_400_when_unknown_task_id(client, monkeypatch):
    """task_ids 含报告内不存在的编号 -> 400。"""
    import app.api.v1.endpoints.distribution as dist_ep
    import app.services.diagnostic_service as ds_mod

    monkeypatch.setattr(
        ds_mod.DiagnosticService, "get_report_by_code",
        lambda code, db: FakeReport(report_code=code, geo_tasks=[FakeTask("T1")]),
    )
    saved = dist_ep.distribution_client
    dist_ep.distribution_client = FakeDistributionClient()
    try:
        resp = client.post(
            "/api/v1/distribution/dispatch",
            json={"report_code": "R-1", "task_ids": ["T1", "NOPE"]},
        )
    finally:
        dist_ep.distribution_client = saved
    assert resp.status_code == 400


def test_api_dispatch_200_success(client, monkeypatch):
    """正常路径 -> 200 返回 DispatchBatchResult。"""
    import app.api.v1.endpoints.distribution as dist_ep
    import app.services.diagnostic_service as ds_mod

    batch = DispatchBatchResult(
        report_code="R-1", target_company="示例科技", brand_id="示例科技::深圳",
        total=1, succeeded=1,
    )
    monkeypatch.setattr(
        ds_mod.DiagnosticService, "get_report_by_code",
        lambda code, db: FakeReport(report_code=code, geo_tasks=[FakeTask("T1")]),
    )
    saved = dist_ep.distribution_client
    dist_ep.distribution_client = FakeDistributionClient(batch=batch)
    try:
        resp = client.post(
            "/api/v1/distribution/dispatch",
            json={"report_code": "R-1"},
        )
    finally:
        dist_ep.distribution_client = saved
    assert resp.status_code == 200
    data = resp.json()
    assert data["report_code"] == "R-1"
    assert data["total"] == 1
    assert data["succeeded"] == 1


def test_api_status_200(client, monkeypatch):
    """GET /status -> 200 返回 DistributionStatus。"""
    import app.api.v1.endpoints.distribution as dist_ep

    status = DistributionStatus(
        enabled=True, configured=True, base_url="http://dist", reachable=True, detail="HTTP 200"
    )
    saved = dist_ep.distribution_client
    dist_ep.distribution_client = FakeDistributionClient(status=status)
    try:
        resp = client.get("/api/v1/distribution/status")
    finally:
        dist_ep.distribution_client = saved
    assert resp.status_code == 200
    data = resp.json()
    assert data["reachable"] is True
    assert data["configured"] is True


# ===========================================================================
# 六、schedule_auto_dispatch —— 后台任务强引用保护
# ===========================================================================

def test_schedule_auto_dispatch_unconfigured_returns_none_no_network():
    """未配置时投递直接返回 None，零网络请求。"""
    calls: list = []
    handler = make_handler(record=calls, status=200, json_body={"items": []})
    client = DistributionClient(
        base_url="", enabled=False, transport=make_transport(handler)
    )
    import app.services.distribution_client as dc_mod

    saved = dc_mod.distribution_client
    dc_mod.distribution_client = client
    try:
        out = dc_mod.schedule_auto_dispatch(FakeReport(geo_tasks=[FakeTask("T1")]))
    finally:
        dc_mod.distribution_client = saved
    assert out is None
    assert calls == []


def test_schedule_auto_dispatch_keeps_strong_reference_and_cleans_up():
    """关键回归：后台任务必须被强引用池持有，且完成后自动移出。

    事件循环对 Task 只持弱引用，未保留强引用时任务可能中途被 GC，
    表现为"偶发不推送"的间歇性故障（Python 官方明确警告）。
    """
    calls: list = []
    handler = make_handler(
        record=calls, status=200,
        json_body={"items": [{"task_id": "T1", "status": "pending", "created": True}]},
    )
    client = DistributionClient(base_url="http://dist", transport=make_transport(handler))

    import app.services.distribution_client as dc_mod

    saved = dc_mod.distribution_client
    dc_mod.distribution_client = client
    dc_mod._BACKGROUND_TASKS.clear()

    async def scenario() -> tuple:
        task = dc_mod.schedule_auto_dispatch(FakeReport(geo_tasks=[FakeTask("T1")]))
        held_immediately = len(dc_mod._BACKGROUND_TASKS)
        await task
        # 回调在任务完成后由事件循环调度，让出一轮确保 discard 已执行
        await asyncio.sleep(0)
        return task, held_immediately, len(dc_mod._BACKGROUND_TASKS)

    try:
        task, held_immediately, held_after = asyncio.run(scenario())
    finally:
        dc_mod.distribution_client = saved

    assert task is not None
    assert held_immediately == 1, "后台任务未被强引用池持有，有被 GC 的风险"
    assert held_after == 0, "任务完成后应从强引用池移除，避免泄漏"
    # 且后台任务确实完成了真实下发（不是空跑）
    assert len(calls) == 1


def test_schedule_auto_dispatch_without_running_loop_returns_none():
    """同步上下文（无运行中的事件循环）投递安全放弃，绝不抛异常。"""
    handler = make_handler(status=200, json_body={"items": []})
    client = DistributionClient(base_url="http://dist", transport=make_transport(handler))

    import app.services.distribution_client as dc_mod

    saved = dc_mod.distribution_client
    dc_mod.distribution_client = client
    try:
        out = dc_mod.schedule_auto_dispatch(FakeReport(geo_tasks=[FakeTask("T1")]))
    finally:
        dc_mod.distribution_client = saved
    assert out is None


# ===========================================================================
# 七、归口装配验证：/diagnostic/run 是否真的接上了自动下发
# ===========================================================================

def _fake_report_out():
    """构造一个满足 DiagnosticReportOut 必填字段的假报告。"""
    from app.schemas.diagnostic import DiagnosticReportOut

    return DiagnosticReportOut(
        id=1,
        report_code="FYXB-FAKE-0001",
        target_company="长沙岳麓万豪酒店管理有限公司",
        brand_name="长沙岳麓万豪酒店",
        industry="酒店住宿",
        city="长沙",
        search_keywords=["长沙岳麓万豪酒店"],
        agency_name="测试授权中心",
        consultant_name="测试顾问",
        visibility_score=15,
        risk_level="HIGH_RISK",
        summary_verdict="装配验证用假报告",
        competitors=[],
        prescriptions=[],
        created_at=0,
        items=[],
    )


def _stub_diagnostic_service(monkeypatch):
    """把体检执行与报告读取替换为离线桩，返回被调度记录列表。"""
    import app.api.v1.endpoints.diagnostic as diag_ep

    dispatched: list = []

    class FakeReportRow:
        report_code = "FYXB-FAKE-0001"

    async def fake_execute(payload, db):
        return FakeReportRow()

    def fake_get_report(report_code, db):
        return _fake_report_out()

    monkeypatch.setattr(diag_ep.DiagnosticService, "execute_diagnostic", fake_execute)
    monkeypatch.setattr(diag_ep.DiagnosticService, "get_report_by_code", fake_get_report)
    monkeypatch.setattr(
        diag_ep, "schedule_auto_dispatch", lambda report: dispatched.append(report)
    )
    return dispatched


_RUN_BODY = {
    "target_company": "长沙岳麓万豪酒店管理有限公司",
    "brand_name": "长沙岳麓万豪酒店",
    "industry": "酒店住宿",
    "city": "长沙",
    "keywords": ["长沙岳麓万豪酒店"],
}


def test_diagnostic_run_triggers_auto_dispatch_when_enabled(client, monkeypatch):
    """体检成功后必须真的触发自动下发，否则 01->03 自动链路是断的。

    历史教训：子代理只测"自己那块的 API 对不对"，不测"组件装配后数据流是否正确"。
    """
    import app.api.v1.endpoints.diagnostic as diag_ep

    dispatched = _stub_diagnostic_service(monkeypatch)
    monkeypatch.setattr(diag_ep.settings, "DISTRIBUTION_AUTO_DISPATCH", True)

    resp = client.post("/api/v1/diagnostic/run", json=_RUN_BODY)

    assert resp.status_code == 200, resp.text
    assert resp.json()["report_code"] == "FYXB-FAKE-0001"
    assert len(dispatched) == 1, "体检成功却未触发自动下发 —— 跨仓自动链路断开"


def test_diagnostic_run_skips_auto_dispatch_when_disabled(client, monkeypatch):
    """开关关闭时不得触发自动下发（保留人工灰度能力）。"""
    import app.api.v1.endpoints.diagnostic as diag_ep

    dispatched = _stub_diagnostic_service(monkeypatch)
    monkeypatch.setattr(diag_ep.settings, "DISTRIBUTION_AUTO_DISPATCH", False)

    resp = client.post("/api/v1/diagnostic/run", json=_RUN_BODY)

    assert resp.status_code == 200, resp.text
    assert dispatched == []
