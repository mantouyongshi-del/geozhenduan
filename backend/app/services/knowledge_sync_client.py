"""M7.1 跨仓事实同步客户端：把体检产出的事实基准库回流到 02 品牌知识库。

与 `distribution_client.py` 同源范式，刻意保持结构一致以降低维护成本：
- 未启用/未配置时**零网络请求**，直接结构化降级；
- 指数退避重试，`sleep` 可注入（离线测试可断言无真实等待）；
- 任何网络异常/非 2xx 一律收敛为 `degraded=True`，**绝不向上抛**（AGENTS.md 五.3）。

关键取舍：**没有合法 USCC 就不同步**。
02 的事实档案以 18 位 USCC 为主键，传降级键（企业全称::城市）会被 02 的
USCC 校验直接拦成 422 —— 与其发一个注定失败、还污染对方错误日志的请求，
不如本地静默跳过并给出可操作的原因（提示运营去补录 USCC）。
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Set

import httpx

from app.core.config import settings
from app.core.uscc import is_uscc_format
from app.schemas.knowledge_sync import KnowledgeSyncResult, KnowledgeSyncStatus

logger = logging.getLogger(__name__)

_MERGE_PATH = "/api/v1/knowledge/facts/merge"


class KnowledgeSyncClient:
    """02 品牌知识库 HTTP 客户端。所有协作者均可注入，便于离线测试。"""

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
            base_url if base_url is not None else settings.KNOWLEDGE_API_URL
        ).rstrip("/")
        self._token = token if token is not None else settings.INTERNAL_SERVICE_SECRET
        self._timeout = timeout if timeout is not None else settings.KNOWLEDGE_SYNC_TIMEOUT_S
        self._max_retries = max(
            1, max_retries if max_retries is not None else settings.KNOWLEDGE_SYNC_MAX_RETRIES
        )
        self._enabled = enabled if enabled is not None else settings.KNOWLEDGE_SYNC_ENABLED
        self._transport = transport
        self._sleep = sleep or asyncio.sleep
        self._client: Optional[httpx.AsyncClient] = None

    # ---------------- 属性 ----------------

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def enabled(self) -> bool:
        return bool(self._enabled)

    @property
    def configured(self) -> bool:
        """启用且配置了目标地址才认为可同步；否则一次网络请求都不发。"""
        return bool(self._enabled and self._base_url)

    # ---------------- 载荷构造 ----------------

    @staticmethod
    def _extract_facts(report: Any) -> List[Dict[str, str]]:
        """抽取可回流的事实列表。

        容忍两种形态（这是真实踩到的坑）：
        - ORM 模型 `DiagnosticReport`：`brand_facts_json`（JSON 字符串）；
        - 输出模型 `DiagnosticReportOut`：`brand_facts`（已解析为 list）。
        只认其中一种会直接导致整条链路静默退化成「无事实可同步」。
        """
        raw = getattr(report, "brand_facts_json", None)
        if raw is None:
            raw = getattr(report, "brand_facts", None)
        if not raw:
            return []
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except (ValueError, TypeError):
                logger.warning("[knowledge-sync] 事实字段解析失败，跳过同步：%r", raw[:120])
                return []
        if not isinstance(raw, list):
            return []

        merged: Dict[str, str] = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            key = str(item.get("fact_key") or "").strip()
            value = str(item.get("fact_value") or "").strip()
            if key and value:
                merged[key] = value
        return [{"fact_key": k, "fact_value": v} for k, v in merged.items()]

    @staticmethod
    def build_merge_payload(report: Any, brand_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """构造 02 合并请求体；USCC 非法或无事实可同步时返回 None（调用方应跳过）。"""
        resolved = (brand_id or "").strip() or str(getattr(report, "uscc", "") or "").strip()
        if not is_uscc_format(resolved):
            return None
        facts = KnowledgeSyncClient._extract_facts(report)
        if not facts:
            return None
        return {
            "brand_id": resolved,
            "company_name": (getattr(report, "target_company", "") or "").strip()
            or (getattr(report, "brand_name", "") or "").strip(),
            "brand_name": (getattr(report, "brand_name", "") or "").strip() or None,
            "city": (getattr(report, "city", "") or "").strip() or None,
            "facts": facts,
        }

    # ---------------- 传输层 ----------------

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["X-Internal-Token"] = self._token
        return headers

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            kwargs: Dict[str, Any] = {"timeout": self._timeout}
            if self._transport is not None:
                kwargs["transport"] = self._transport
            self._client = httpx.AsyncClient(**kwargs)
        return self._client

    async def merge_facts(self, payload: Dict[str, Any]) -> KnowledgeSyncResult:
        """调用 02 的合并端点。任何失败都收敛为结构化结果，绝不抛异常。"""
        started = time.perf_counter()
        result = KnowledgeSyncResult(brand_id=str(payload.get("brand_id", "")))
        if not self.configured:
            result.degraded = True
            result.reason = "下游知识库未启用或未配置"
            return result

        client = await self._get_client()
        last_reason = ""
        for attempt in range(1, self._max_retries + 1):
            result.attempts = attempt
            try:
                resp = await client.post(
                    f"{self._base_url}{_MERGE_PATH}", json=payload, headers=self._headers()
                )
            except Exception as exc:  # noqa: BLE001 — 降级红线：任何异常都不外抛
                last_reason = f"网络异常：{type(exc).__name__}"
                logger.warning("[knowledge-sync] 第 %s 次同步失败：%s", attempt, exc)
            else:
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                    except ValueError:
                        last_reason = f"响应非 JSON（HTTP {resp.status_code}）"
                    else:
                        result.ok = True
                        result.synced = bool(data.get("synced"))
                        result.total = int(data.get("total") or 0)
                        result.inserted = int(data.get("inserted") or 0)
                        result.updated = int(data.get("updated") or 0)
                        result.unchanged = int(data.get("unchanged") or 0)
                        result.skipped = int(data.get("skipped") or 0)
                        result.reason = str(data.get("reason") or "")
                        raw_items = data.get("items") or []
                        if isinstance(raw_items, list):
                            result.items = [dict(it) for it in raw_items if isinstance(it, dict)]
                        break
                else:
                    last_reason = f"HTTP {resp.status_code}"
                    logger.warning("[knowledge-sync] 第 %s 次同步返回 %s", attempt, resp.status_code)

            if attempt < self._max_retries:
                await self._sleep(0.5 * (2 ** (attempt - 1)))

        if not result.ok:
            result.degraded = True
            result.reason = last_reason or "同步失败"
        result.latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return result

    async def sync_report(
        self, report: Any, brand_id: Optional[str] = None
    ) -> KnowledgeSyncResult:
        """同步单份体检报告的事实基准库到 02。"""
        report_code = str(getattr(report, "report_code", "") or "")
        payload = self.build_merge_payload(report, brand_id=brand_id)
        if payload is None:
            # 无 USCC 或无可同步事实：本地静默跳过，一次请求都不发
            return KnowledgeSyncResult(
                report_code=report_code,
                brand_id=str(getattr(report, "uscc", "") or ""),
                degraded=True,
                reason="报告未登记合法统一社会信用代码或无事实可同步，已跳过",
            )
        result = await self.merge_facts(payload)
        result.report_code = report_code
        return result

    async def probe(self) -> KnowledgeSyncStatus:
        """下游连通性自检：未配置时不发请求，异常不抛。"""
        status = KnowledgeSyncStatus(
            enabled=self.enabled, configured=self.configured, base_url=self._base_url
        )
        if not self.configured:
            status.detail = "未启用或未配置下游知识库地址"
            return status
        started = time.perf_counter()
        try:
            client = await self._get_client()
            resp = await client.get(f"{self._base_url}/health")
            status.reachable = resp.status_code == 200
            status.detail = f"HTTP {resp.status_code}"
        except Exception as exc:  # noqa: BLE001
            status.detail = f"{type(exc).__name__}"
        status.latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return status

    async def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()


knowledge_sync_client = KnowledgeSyncClient()


async def auto_sync_report(report: Any) -> Optional[KnowledgeSyncResult]:
    """体检完成后的自动回流入口；内部任何异常都被吞掉，绝不反噬主流程。"""
    if not knowledge_sync_client.configured:
        return None
    try:
        return await knowledge_sync_client.sync_report(report)
    except Exception:  # noqa: BLE001 — 兜底红线：同步失败绝不影响体检报告返回
        logger.exception("[knowledge-sync] 自动同步异常，已静默降级")
        return None


# asyncio 事件循环对 Task 只持弱引用：不保留强引用，任务可能在途中被 GC，
# 表现为「偶发不回流」—— 这类缺陷极难复现，必须显式持有。
_BACKGROUND_TASKS: Set[Any] = set()


def schedule_auto_sync(report: Any) -> Optional[Any]:
    """把自动回流投递到后台事件循环，并保留强引用（完成后自动出池防泄漏）。"""
    if not knowledge_sync_client.configured:
        return None
    try:
        task = asyncio.create_task(auto_sync_report(report))
    except RuntimeError:
        return None  # 无运行中的事件循环（同步上下文）：安全放弃
    _BACKGROUND_TASKS.add(task)
    task.add_done_callback(_BACKGROUND_TASKS.discard)
    return task
