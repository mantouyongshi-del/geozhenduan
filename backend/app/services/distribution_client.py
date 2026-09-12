"""跨仓工单下发客户端：把 01 雷达的 `GeoActionTask` 推送到 03 内容分发系统。

对应 03 的 `POST /api/v1/tasks/receive`（支持单条或批量）。

设计红线（对齐 AGENTS.md）：
- 五.3 优雅降级：任何网络异常、非 2xx、契约异常都绝不向上抛，统一收敛为结构化结果；
- 五.4 内部令牌：请求头附加 `X-Internal-Token`（仅在密钥非空时），本地联调默认信任放行；
- 五.1 全局主键：优先 USCC，01 侧暂无该字段时降级为 `{企业全称}::{城市}`。
"""
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional, Sequence, Set

import httpx

from app.core.config import settings
from app.schemas.distribution import (
    DispatchBatchResult,
    DispatchTaskResult,
    DistributionStatus,
)

_RECEIVE_PATH = "/api/v1/tasks/receive"
_HEALTH_PATH = "/health"
_TOKEN_HEADER = "X-Internal-Token"


class DistributionClient:
    """下游分发系统 HTTP 客户端。所有协作者均可注入，便于离线测试。"""

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[float] = None,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        max_retries: Optional[int] = None,
        enabled: Optional[bool] = None,
        sleep: Optional[Any] = None,
    ) -> None:
        self._base_url = (
            base_url if base_url is not None else settings.DISTRIBUTION_API_URL
        ).rstrip("/")
        self._token = token if token is not None else settings.INTERNAL_SERVICE_SECRET
        self._timeout = timeout if timeout is not None else settings.DISTRIBUTION_TIMEOUT_S
        self._max_retries = max(
            1, max_retries if max_retries is not None else settings.DISTRIBUTION_MAX_RETRIES
        )
        self._enabled = enabled if enabled is not None else settings.DISTRIBUTION_ENABLED
        self._transport = transport
        self._sleep = sleep or asyncio.sleep

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def enabled(self) -> bool:
        return bool(self._enabled)

    @property
    def configured(self) -> bool:
        """启用且配置了目标地址才认为可下发；否则一次网络请求都不发。"""
        return bool(self._enabled and self._base_url)

    @staticmethod
    def build_brand_id(
        target_company: str, city: str = "", explicit: Optional[str] = None
    ) -> str:
        """全局实体主键：优先 USCC，缺失时降级 `{企业全称}::{城市}`（AGENTS.md 五.1）。"""
        if explicit and explicit.strip():
            return explicit.strip()
        name = (target_company or "").strip()
        region = (city or "").strip() or "全国"
        return f"{name}::{region}"

    @staticmethod
    def build_payload(
        *,
        brand_id: str,
        brand_name: str,
        city: str,
        industry: str,
        task: Any,
    ) -> Dict[str, Any]:
        """把 01 的 `GeoActionTask` 映射为 03 的 `DispatchTaskPayload` 信封。"""
        return {
            "brand_id": brand_id,
            "brand_name": brand_name or "",
            "city": city or "",
            "industry": industry or "",
            "task": {
                "id": getattr(task, "id", "") or "",
                "action": getattr(task, "action", "") or "create_content",
                "recommended_platforms": list(getattr(task, "recommended_platforms", None) or []),
                "suggested_title": getattr(task, "suggested_title", None),
                "core_keywords": list(getattr(task, "core_keywords", None) or []),
                "format_guide": getattr(task, "format_guide", None),
                "expected_impact": getattr(task, "expected_impact", None) or "",
            },
        }

    @staticmethod
    def _pick_item(data: Any, task_id: str) -> Dict[str, Any]:
        """从下游 `BatchIngestResult` 中取出本工单对应的条目。"""
        items = data.get("items") if isinstance(data, dict) else None
        if isinstance(items, list) and items:
            for item in items:
                if isinstance(item, dict) and item.get("task_id") == task_id:
                    return item
            if isinstance(items[0], dict):
                return items[0]
        return {}

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self._token:
            headers[_TOKEN_HEADER] = self._token
        return headers

    async def dispatch_task(
        self, payload: Dict[str, Any], *, task_id: str
    ) -> DispatchTaskResult:
        """下发单条工单。退避重试耗尽后返回降级结果，绝不抛异常。"""
        result = DispatchTaskResult(
            task_id=task_id, brand_id=str(payload.get("brand_id", ""))
        )
        if not self.configured:
            result.degraded = True
            result.reason = "下游分发系统未启用或未配置"
            return result

        started = time.perf_counter()
        last_reason = ""
        try:
            async with httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                transport=self._transport,
                trust_env=False,
            ) as client:
                for attempt in range(1, self._max_retries + 1):
                    result.attempts = attempt
                    try:
                        resp = await client.post(
                            _RECEIVE_PATH, json=payload, headers=self._headers()
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            item = self._pick_item(data, task_id)
                            result.ok = True
                            result.status = item.get("status")
                            result.created = item.get("created")
                            result.latency_ms = round(
                                (time.perf_counter() - started) * 1000, 2
                            )
                            return result
                        last_reason = f"下游返回 HTTP {resp.status_code}"
                    except Exception as exc:  # noqa: BLE001 — 降级红线：任何异常都不外抛
                        last_reason = f"{type(exc).__name__}: {exc}"

                    if attempt < self._max_retries:
                        await self._sleep(0.5 * (2 ** (attempt - 1)))
        except Exception as exc:  # noqa: BLE001 — 建连/关闭异常同样降级
            last_reason = f"{type(exc).__name__}: {exc}"

        result.degraded = True
        result.reason = last_reason or "下游分发失败"
        result.latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return result

    async def dispatch_report(
        self,
        report: Any,
        *,
        brand_id: Optional[str] = None,
        task_ids: Optional[Sequence[str]] = None,
    ) -> DispatchBatchResult:
        """把一份体检报告内的工单批量下发到下游内容分发系统。"""
        tasks: List[Any] = list(getattr(report, "geo_tasks", None) or [])
        if task_ids:
            wanted = set(task_ids)
            tasks = [t for t in tasks if getattr(t, "id", None) in wanted]

        resolved_brand_id = self.build_brand_id(
            getattr(report, "target_company", "") or getattr(report, "brand_name", ""),
            getattr(report, "city", "") or "",
            explicit=brand_id,
        )
        batch = DispatchBatchResult(
            report_code=getattr(report, "report_code", "") or "",
            target_company=getattr(report, "target_company", "") or "",
            brand_id=resolved_brand_id,
            total=len(tasks),
        )
        for task in tasks:
            payload = self.build_payload(
                brand_id=resolved_brand_id,
                brand_name=getattr(report, "brand_name", "") or "",
                city=getattr(report, "city", "") or "",
                industry=getattr(report, "industry", "") or "",
                task=task,
            )
            item = await self.dispatch_task(payload, task_id=getattr(task, "id", ""))
            batch.items.append(item)
            if item.ok:
                batch.succeeded += 1
            if item.degraded:
                batch.degraded += 1
        return batch

    async def probe(self) -> DistributionStatus:
        """探测下游连通性（供前端/运维一键自检）。"""
        status = DistributionStatus(
            enabled=self.enabled, configured=self.configured, base_url=self._base_url
        )
        if not self.configured:
            status.detail = "下游分发系统未启用或未配置"
            return status

        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                transport=self._transport,
                trust_env=False,
            ) as client:
                resp = await client.get(_HEALTH_PATH)
            status.reachable = resp.status_code == 200
            status.detail = f"HTTP {resp.status_code}"
        except Exception as exc:  # noqa: BLE001 — 探活失败只报不可达
            status.detail = f"{type(exc).__name__}: {exc}"
        status.latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return status

    async def close(self) -> None:
        """本客户端按请求粒度建连，无长连接池需回收；保留接口对齐下游契约。"""
        return None


distribution_client = DistributionClient()


async def auto_dispatch_report(report: Any) -> Optional[DispatchBatchResult]:
    """体检完成后的自动下发入口（由 `/diagnostic/run` 以后台任务方式调用）。

    - 未启用或未配置时直接返回 None，一次网络请求都不发；
    - 任何异常一律静默吞掉：体检报告生成是主流程，
      绝不因下游内容工厂不可用而失败（AGENTS.md 五.3 优雅降级）。
    """
    if not distribution_client.configured:
        return None
    try:
        return await distribution_client.dispatch_report(report)
    except Exception:  # noqa: BLE001 — 兜底红线：自动下发绝不反噬主流程
        return None


# 后台任务强引用池。
# 事件循环对 Task 只持有弱引用：不保存强引用时，任务可能在执行途中被垃圾回收，
# 表现为"偶发不推送"这类极难排查的间歇性故障（Python 官方文档明确警告）。
_BACKGROUND_TASKS: Set[Any] = set()


def schedule_auto_dispatch(report: Any) -> Optional[Any]:
    """把自动下发投递到后台事件循环执行，并保留强引用。

    - 未启用/未配置时直接返回 None，零网络；
    - 无运行中的事件循环（同步上下文）时安全放弃，绝不抛异常。
    """
    if not distribution_client.configured:
        return None
    try:
        task = asyncio.create_task(auto_dispatch_report(report))
    except RuntimeError:
        return None
    _BACKGROUND_TASKS.add(task)
    task.add_done_callback(_BACKGROUND_TASKS.discard)
    return task
