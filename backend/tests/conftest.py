"""离线测试公共夹具与构造器。

所有网络访问一律通过 `httpx.MockTransport` 注入，绝不发起真实请求。
API 层测试用 `fastapi.testclient.TestClient` 驱动 `main:app`。
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional, Sequence

import httpx
import pytest

from app.schemas.distribution import DispatchBatchResult, DispatchTaskResult, DistributionStatus
from app.schemas.diagnostic import GeoActionTask


# ---------------------------------------------------------------------------
# 被测对象的轻量替身（仅暴露实现所读取的属性，避免构造完整 Pydantic 模型）
# ---------------------------------------------------------------------------
class FakeTask:
    """模拟 01 侧产出的 GeoActionTask 工单（实现只读取部分字段）。"""

    def __init__(
        self,
        id: str,
        action: str = "create_content",
        recommended_platforms: Optional[List[str]] = None,
        suggested_title: Optional[str] = None,
        core_keywords: Optional[List[str]] = None,
        format_guide: Optional[str] = None,
        expected_impact: str = "",
    ) -> None:
        self.id = id
        self.action = action
        self.recommended_platforms = recommended_platforms or []
        self.suggested_title = suggested_title
        self.core_keywords = core_keywords or []
        self.format_guide = format_guide
        self.expected_impact = expected_impact


class FakeReport:
    """模拟 DiagnosticReportOut（实现只读取 geo_tasks 与目标字段）。"""

    def __init__(
        self,
        *,
        report_code: str = "R-001",
        target_company: str = "示例科技有限公司",
        brand_name: str = "示例科技",
        city: str = "深圳",
        industry: str = "SaaS",
        uscc: Optional[str] = None,
        geo_tasks: Optional[Sequence[Any]] = None,
    ) -> None:
        self.report_code = report_code
        self.target_company = target_company
        self.brand_name = brand_name
        self.city = city
        self.industry = industry
        self.uscc = uscc
        self.geo_tasks = list(geo_tasks or [])


# ---------------------------------------------------------------------------
# MockTransport 构造器
# ---------------------------------------------------------------------------
def make_handler(
    *,
    status: int = 200,
    json_body: Optional[Dict[str, Any]] = None,
    record: Optional[List[Dict[str, Any]]] = None,
    raise_exc: Optional[Exception] = None,
):
    """返回一个记录每次请求的 MockTransport handler。

    - record: 若提供，每次请求会把 {method, url, headers} 追加进去（用于断言零网络/请求头）；
    - raise_exc: 若提供，每次请求抛出该异常（模拟 ConnectError 等网络故障）；
    - 否则按 status/json_body 返回固定响应。
    """

    def handler(request: httpx.Request) -> httpx.Response:
        if record is not None:
            record.append(
                {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "content": request.content,
                }
            )
        if raise_exc is not None:
            raise raise_exc
        return httpx.Response(status, json=json_body if json_body is not None else {})

    return handler


def make_transport(handler):
    return httpx.MockTransport(handler)


# ---------------------------------------------------------------------------
# 假 sleep：记录退避参数，不产生真实等待
# ---------------------------------------------------------------------------
class FakeSleep:
    def __init__(self) -> None:
        self.calls: List[float] = []

    async def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


# ---------------------------------------------------------------------------
# 假 distribution_client（供 API 层 monkeypatch 使用）
# ---------------------------------------------------------------------------
class FakeDistributionClient:
    def __init__(self, batch: Optional[DispatchBatchResult] = None,
                 status: Optional[DistributionStatus] = None) -> None:
        self._batch = batch or DispatchBatchResult(
            report_code="R-001", target_company="X", brand_id="X"
        )
        self._status = status or DistributionStatus(
            enabled=True, configured=True, base_url="http://test", reachable=True
        )

    async def dispatch_report(self, report, *, brand_id=None, task_ids=None) -> DispatchBatchResult:
        return self._batch

    async def probe(self) -> DistributionStatus:
        return self._status


@pytest.fixture
def fake_sleep() -> FakeSleep:
    return FakeSleep()
