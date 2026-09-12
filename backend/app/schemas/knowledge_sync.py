"""M7.1 跨仓事实同步契约（01-radar-monitor → 02-brand-knowledge）。

01 体检产出的 `brand_facts`（企业事实基准库）此前只落在报告里、从未回流 02，
导致下游出稿的事实注入完全依赖人工录入 —— 这是矩阵「数据流第 0 步」的断点。
本模块定义回流所需的请求/结果模型。

设计约束（AGENTS.md 五）：
- 五.1 全局主键：02 的事实档案以 18 位 USCC 为主键，因此**没有 USCC 就不同步**
  （降级键会直接被 02 的 USCC 校验拦成 422，属无意义请求）；
- 五.3 优雅降级：任何网络异常、非 2xx、契约异常都绝不向上抛，统一收敛为结构化结果。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeSyncRequest(BaseModel):
    """手动/补推触发一次事实回流（E2E 与运维补数用）。"""

    model_config = ConfigDict(extra="ignore")

    report_code: str = Field(..., min_length=1, description="体检报告分享码")
    brand_id: Optional[str] = Field(
        None, description="显式指定 USCC 覆盖报告档案上的 uscc（用于修正历史数据）"
    )


class KnowledgeSyncResult(BaseModel):
    """单次回流结果。任何失败都体现为 `degraded=True` + `reason`，绝不抛异常。"""

    model_config = ConfigDict(extra="ignore")

    report_code: str = ""
    brand_id: str = ""
    ok: bool = False
    synced: bool = Field(False, description="02 是否真的写入了事实（主档缺失时为 False）")
    total: int = 0
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0
    skipped: int = 0
    degraded: bool = False
    reason: str = ""
    attempts: int = 0
    latency_ms: float = 0.0
    # 逐条合并明细（{fact_key, action, incoming_value, existing_value}）：
    # 只给计数无法断言「某条人工事实是否被保护」，明细是红线可验证性的前提。
    items: List[Dict[str, Any]] = Field(default_factory=list)


class KnowledgeSyncStatus(BaseModel):
    """下游知识库连通性自检（供 E2E 与运维排障）。"""

    enabled: bool = False
    configured: bool = False
    base_url: str = ""
    reachable: bool = False
    detail: str = ""
    latency_ms: float = 0.0
