"""M7.1 跨仓事实同步客户端离线用例（全程 httpx.MockTransport，零真实网络）。

重点防线：
- 零网络前置：未启用/未配置/无合法 USCC 时一次请求都不发；
- 零误杀：一份正常的、带 USCC 与事实的报告必须能同步成功（历史上子代理只测
  「该拦的拦住了」而漏测这一侧，导致整条链路报废）；
- 退避无真实等待：sleep 注入后断言退避序列严格为 [0.5, 1.0]；
- 强引用保护：后台任务必须入池（防 GC 中途回收）并在完成后出池（防泄漏）。
"""
from __future__ import annotations

import asyncio
import json
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from app.schemas.knowledge_sync import KnowledgeSyncResult, KnowledgeSyncStatus
from app.services import knowledge_sync_client as ksc_mod
from app.services.knowledge_sync_client import KnowledgeSyncClient

from tests.conftest import FakeReport, make_handler, make_transport

USCC = "91430100MA4L2X8K3T"

BRAND_FACTS = json.dumps(
    [
        {"fact_type": "工商主体", "fact_key": "企业工商全称", "fact_value": "长沙岳麓万豪酒店管理有限公司"},
        {"fact_type": "主营赛道", "fact_key": "主营业务领域", "fact_value": "酒店住宿"},
    ],
    ensure_ascii=False,
)


def _ok_body(**overrides):
    body = {
        "brand_id": USCC,
        "synced": True,
        "total": 2,
        "inserted": 2,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
        "reason": "",
        "items": [],
    }
    body.update(overrides)
    return body


# ---------------------------------------------------------------------------
# 零网络前置
# ---------------------------------------------------------------------------
def test_disabled_client_sends_no_request():
    record: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb", transport=make_transport(make_handler(record=record)), enabled=False
    )
    assert client.configured is False

    result = asyncio.run(client.merge_facts({"brand_id": USCC, "facts": []}))

    assert record == [], "未启用时严禁发起任何请求"
    assert result.ok is False
    assert result.degraded is True
    assert "未启用或未配置" in result.reason


def test_empty_base_url_sends_no_request():
    record: list = []
    client = KnowledgeSyncClient(base_url="", transport=make_transport(make_handler(record=record)))
    assert client.configured is False

    report = FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)
    result = asyncio.run(client.sync_report(report))

    assert record == []
    assert result.degraded is True


def test_probe_unconfigured_sends_no_request():
    record: list = []
    client = KnowledgeSyncClient(base_url="http://kb", enabled=False,
                                 transport=make_transport(make_handler(record=record)))

    status = asyncio.run(client.probe())

    assert record == []
    assert status.reachable is False
    assert status.configured is False


# ---------------------------------------------------------------------------
# 无合法 USCC / 无事实 -> 静默跳过（绝不发注定失败的请求）
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad_uscc", [None, "", "   ", "NOT-A-USCC", "123", USCC[:-1]])
def test_sync_report_skips_without_valid_uscc(bad_uscc):
    record: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb", transport=make_transport(make_handler(status=200, record=record))
    )
    report = FakeReport(uscc=bad_uscc, brand_facts_json=BRAND_FACTS)

    result = asyncio.run(client.sync_report(report))

    assert record == [], "USCC 非法时严禁发请求（02 会直接 422）"
    assert result.ok is False
    assert result.degraded is True
    assert "未登记合法统一社会信用代码" in result.reason


def test_sync_report_skips_when_no_usable_facts():
    record: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb", transport=make_transport(make_handler(record=record))
    )
    report = FakeReport(uscc=USCC, brand_facts_json=json.dumps([{"fact_key": "", "fact_value": "x"}]))

    result = asyncio.run(client.sync_report(report))

    assert record == []
    assert result.degraded is True


# ---------------------------------------------------------------------------
# 载荷构造
# ---------------------------------------------------------------------------
def test_build_payload_uses_report_uscc_and_facts():
    report = FakeReport(
        uscc=USCC,
        target_company="长沙岳麓万豪酒店管理有限公司",
        brand_name="长沙岳麓万豪酒店",
        city="长沙",
        brand_facts_json=BRAND_FACTS,
    )
    payload = KnowledgeSyncClient.build_merge_payload(report)

    assert payload is not None
    assert payload["brand_id"] == USCC
    assert payload["company_name"] == "长沙岳麓万豪酒店管理有限公司"
    assert payload["brand_name"] == "长沙岳麓万豪酒店"
    assert payload["city"] == "长沙"
    assert payload["facts"] == [
        {"fact_key": "企业工商全称", "fact_value": "长沙岳麓万豪酒店管理有限公司"},
        {"fact_key": "主营业务领域", "fact_value": "酒店住宿"},
    ]


def test_build_payload_explicit_brand_id_overrides_report_uscc():
    report = FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)
    payload = KnowledgeSyncClient.build_merge_payload(report, brand_id="91110000MA01ABCD2Q")
    assert payload["brand_id"] == "91110000MA01ABCD2Q"


def test_build_payload_empty_optional_fields_become_none():
    report = FakeReport(uscc=USCC, brand_name="", city="", brand_facts_json=BRAND_FACTS)
    payload = KnowledgeSyncClient.build_merge_payload(report)
    assert payload["brand_name"] is None
    assert payload["city"] is None


def test_extract_facts_dedupes_and_drops_empty():
    raw = json.dumps(
        [
            {"fact_key": "K", "fact_value": "旧值"},
            {"fact_key": "K", "fact_value": "新值"},
            {"fact_key": "空值", "fact_value": "   "},
            {"fact_key": "", "fact_value": "x"},
            {"fact_key": "正常", "fact_value": "ok"},
        ],
        ensure_ascii=False,
    )
    facts = KnowledgeSyncClient._extract_facts(FakeReport(brand_facts_json=raw))
    assert facts == [{"fact_key": "K", "fact_value": "新值"}, {"fact_key": "正常", "fact_value": "ok"}]


def test_extract_facts_accepts_output_model_shape():
    """回归防线：输出模型 `DiagnosticReportOut` 的字段是 `brand_facts`（已解析 list），
    而 ORM 模型是 `brand_facts_json`（JSON 字符串）。只认其中一种会让整条链路静默
    退化成「无事实可同步」—— 这个缺陷在 E2E 阶段 11 暴露过一次。
    """

    class OutModelReport:
        uscc = USCC
        target_company = "长沙岳麓万豪酒店管理有限公司"
        brand_name = "长沙岳麓万豪酒店"
        city = "长沙"
        brand_facts = [{"fact_key": "主营业务领域", "fact_value": "酒店住宿"}]

    facts = KnowledgeSyncClient._extract_facts(OutModelReport())
    assert facts == [{"fact_key": "主营业务领域", "fact_value": "酒店住宿"}]

    payload = KnowledgeSyncClient.build_merge_payload(OutModelReport())
    assert payload is not None, "输出模型形态必须能构造出载荷"
    assert payload["brand_id"] == USCC


def test_extract_facts_invalid_json_returns_empty():
    assert KnowledgeSyncClient._extract_facts(FakeReport(brand_facts_json="{不是JSON")) == []
    assert KnowledgeSyncClient._extract_facts(FakeReport(brand_facts_json=None)) == []


# ---------------------------------------------------------------------------
# 正向：真的能同步成功（零误杀）
# ---------------------------------------------------------------------------
def test_sync_report_success_is_not_degraded():
    record: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb",
        transport=make_transport(make_handler(status=200, json_body=_ok_body(), record=record)),
    )
    report = FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)

    result = asyncio.run(client.sync_report(report))

    assert result.ok is True, "正常报告必须同步成功（零误杀负向用例）"
    assert result.degraded is False
    assert result.synced is True
    assert result.inserted == 2
    assert result.attempts == 1
    assert record and record[0]["url"].endswith("/api/v1/knowledge/facts/merge")
    assert record[0]["method"] == "POST"
    assert record[0]["headers"]["content-type"] == "application/json"
    body = json.loads(record[0]["content"])
    assert body["brand_id"] == USCC
    assert len(body["facts"]) == 2


def test_internal_token_header_present_only_when_configured():
    record: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb",
        token="secret-xyz",
        transport=make_transport(make_handler(json_body=_ok_body(), record=record)),
    )
    asyncio.run(client.sync_report(FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)))
    assert record[0]["headers"]["x-internal-token"] == "secret-xyz"

    record2: list = []
    client2 = KnowledgeSyncClient(
        base_url="http://kb",
        token="",
        transport=make_transport(make_handler(json_body=_ok_body(), record=record2)),
    )
    asyncio.run(client2.sync_report(FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)))
    assert "x-internal-token" not in record2[0]["headers"]


# ---------------------------------------------------------------------------
# 重试 / 退避 / 降级
# ---------------------------------------------------------------------------
def test_backoff_sequence_has_no_real_wait():
    record: list = []
    sleeps: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb",
        transport=make_transport(make_handler(status=500, record=record)),
        sleep=lambda s: sleeps.append(s) or asyncio.sleep(0),
    )

    started = time.perf_counter()
    result = asyncio.run(client.merge_facts({"brand_id": USCC, "facts": []}))
    elapsed = time.perf_counter() - started

    assert sleeps == [0.5, 1.0], "退避序列必须严格为 0.5 * 2^(n-1)"
    assert elapsed < 0.5, "注入 sleep 后不应产生真实等待"
    assert result.ok is False
    assert result.degraded is True
    assert result.attempts == 3
    assert len(record) == 3


def test_network_exception_degrades_without_raising():
    sleeps: list = []
    client = KnowledgeSyncClient(
        base_url="http://kb",
        transport=make_transport(make_handler(raise_exc=httpx.ConnectError("boom"))),
        sleep=lambda s: sleeps.append(s) or asyncio.sleep(0),
    )

    result = asyncio.run(client.merge_facts({"brand_id": USCC, "facts": []}))

    assert result.ok is False
    assert result.degraded is True
    assert result.attempts == 3
    assert "ConnectError" in result.reason


def test_retry_then_success():
    statuses = iter([500, 200])
    record: list = []

    def handler(request: httpx.Request) -> httpx.Response:
        record.append(str(request.url))
        return httpx.Response(next(statuses), json=_ok_body())

    client = KnowledgeSyncClient(
        base_url="http://kb",
        transport=make_transport(handler),
        sleep=lambda s: asyncio.sleep(0),
    )

    result = asyncio.run(client.merge_facts({"brand_id": USCC, "facts": []}))

    assert result.ok is True
    assert result.attempts == 2
    assert len(record) == 2


def test_probe_reachable_and_degrades_on_exception():
    client = KnowledgeSyncClient(
        base_url="http://kb", transport=make_transport(make_handler(status=200, json_body={}))
    )
    status = asyncio.run(client.probe())
    assert isinstance(status, KnowledgeSyncStatus)
    assert status.reachable is True
    assert status.detail == "HTTP 200"

    broken = KnowledgeSyncClient(
        base_url="http://kb",
        transport=make_transport(make_handler(raise_exc=httpx.ConnectError("down"))),
    )
    s2 = asyncio.run(broken.probe())
    assert s2.reachable is False
    assert "ConnectError" in s2.detail


# ---------------------------------------------------------------------------
# 后台任务强引用保护（修过的真实缺陷，必须守住）
# ---------------------------------------------------------------------------
def test_schedule_auto_sync_keeps_strong_reference_and_cleans_up():
    async def scenario():
        client = KnowledgeSyncClient(
            base_url="http://kb",
            transport=make_transport(make_handler(json_body=_ok_body())),
        )
        saved = ksc_mod.knowledge_sync_client
        ksc_mod.knowledge_sync_client = client
        ksc_mod._BACKGROUND_TASKS.clear()
        try:
            task = ksc_mod.schedule_auto_sync(FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS))
            assert task is not None
            assert task in ksc_mod._BACKGROUND_TASKS, "不保留强引用会被 GC，表现为偶发不回流"
            result = await task
            assert result is not None and result.ok is True
            await asyncio.sleep(0)  # 让 done_callback 执行
            assert task not in ksc_mod._BACKGROUND_TASKS, "完成后必须出池，否则泄漏"
        finally:
            ksc_mod.knowledge_sync_client = saved
            ksc_mod._BACKGROUND_TASKS.clear()

    asyncio.run(scenario())


def test_schedule_auto_sync_unconfigured_returns_none():
    saved = ksc_mod.knowledge_sync_client
    ksc_mod.knowledge_sync_client = KnowledgeSyncClient(base_url="http://kb", enabled=False)
    try:
        assert ksc_mod.schedule_auto_sync(FakeReport(uscc=USCC)) is None
    finally:
        ksc_mod.knowledge_sync_client = saved


def test_schedule_auto_sync_without_running_loop_returns_none():
    """同步上下文（无运行中的事件循环）投递必须安全放弃，绝不抛异常。"""
    saved = ksc_mod.knowledge_sync_client
    ksc_mod.knowledge_sync_client = KnowledgeSyncClient(base_url="http://kb")
    try:
        assert ksc_mod.schedule_auto_sync(FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)) is None
    finally:
        ksc_mod.knowledge_sync_client = saved


def test_auto_sync_report_swallows_exceptions():
    class Boom:
        configured = True

        async def sync_report(self, report, brand_id=None):
            raise RuntimeError("boom")

    saved = ksc_mod.knowledge_sync_client
    ksc_mod.knowledge_sync_client = Boom()
    try:
        assert asyncio.run(ksc_mod.auto_sync_report(FakeReport(uscc=USCC))) is None
    finally:
        ksc_mod.knowledge_sync_client = saved


# ---------------------------------------------------------------------------
# API 层
# ---------------------------------------------------------------------------
class FakeSyncClient:
    def __init__(self, result):
        self._result = result
        self.configured = True

    async def sync_report(self, report, brand_id=None):
        return self._result

    async def probe(self):
        return KnowledgeSyncStatus(enabled=True, configured=True, base_url="http://kb", reachable=True)


def test_api_sync_unknown_report_returns_404(monkeypatch):
    from app.services.diagnostic_service import DiagnosticService

    monkeypatch.setattr(DiagnosticService, "get_report_by_code", staticmethod(lambda code, db: None))
    with TestClient(__import__("main").app) as c:
        resp = c.post("/api/v1/knowledge-sync/sync", json={"report_code": "NOPE"})
    assert resp.status_code == 404


def test_api_sync_without_uscc_returns_422(monkeypatch):
    from app.services.diagnostic_service import DiagnosticService

    monkeypatch.setattr(
        DiagnosticService, "get_report_by_code", staticmethod(lambda code, db: FakeReport(uscc=None))
    )
    with TestClient(__import__("main").app) as c:
        resp = c.post("/api/v1/knowledge-sync/sync", json={"report_code": "R-1"})
    assert resp.status_code == 422, "缺 USCC 属可修正输入问题，必须 422 而非伪装成功"
    assert "统一社会信用代码" in resp.json()["detail"]


def test_api_sync_success_returns_200(monkeypatch):
    from app.services import diagnostic_service
    import app.api.v1.endpoints.knowledge_sync as ep

    monkeypatch.setattr(
        diagnostic_service.DiagnosticService,
        "get_report_by_code",
        staticmethod(lambda code, db: FakeReport(uscc=USCC, brand_facts_json=BRAND_FACTS)),
    )
    monkeypatch.setattr(
        ep,
        "knowledge_sync_client",
        FakeSyncClient(KnowledgeSyncResult(ok=True, synced=True, total=2, inserted=2, brand_id=USCC)),
    )
    with TestClient(__import__("main").app) as c:
        resp = c.post("/api/v1/knowledge-sync/sync", json={"report_code": "R-1"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True and data["inserted"] == 2


def test_api_status_returns_200(monkeypatch):
    import app.api.v1.endpoints.knowledge_sync as ep

    monkeypatch.setattr(ep, "knowledge_sync_client", FakeSyncClient(None))
    with TestClient(__import__("main").app) as c:
        resp = c.get("/api/v1/knowledge-sync/status")
    assert resp.status_code == 200
    assert resp.json()["reachable"] is True
