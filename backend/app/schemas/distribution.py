"""跨仓工单下发数据模型 (Pydantic v2)。

01 雷达作为"处方发起者"，把体检产出的 `GeoActionTask` 主动推送给下游
03 内容分发系统。此处模型严格对齐 03 的入站契约
(`POST /api/v1/tasks/receive` → `DispatchTaskPayload` / `BatchIngestResult`)，
并遵循 AGENTS.md 二.3 宽容解析与五.3 优雅降级。
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DispatchRequest(BaseModel):
    """触发一次报告工单下发的入参。"""

    model_config = ConfigDict(extra="ignore")

    report_code: str = Field(min_length=1, description="体检报告分享码")
    brand_id: Optional[str] = Field(
        default=None,
        description=(
            "企业 18 位统一社会信用代码。01 侧暂无 USCC 档案字段，"
            "缺省时按 AGENTS.md 五.1 降级为 `{企业全称}::{城市}` 联合主键"
        ),
    )
    task_ids: Optional[List[str]] = Field(
        default=None, description="仅下发指定工单编号；缺省下发报告内全部工单"
    )


class DispatchTaskResult(BaseModel):
    """单条工单的下发结果。

    下游不可达、超时、契约异常一律收敛为 `ok=False + degraded=True`，
    绝不向上抛出异常（AGENTS.md 五.3）。
    """

    task_id: str
    brand_id: str
    ok: bool = False
    status: Optional[str] = Field(default=None, description="下游落库后的工单状态")
    created: Optional[bool] = Field(default=None, description="True=新建，False=命中幂等键优雅更新")
    attempts: int = 0
    degraded: bool = Field(default=False, description="是否发生降级（下游不可用或未启用）")
    reason: str = ""
    latency_ms: float = 0.0


class DispatchBatchResult(BaseModel):
    """一次报告下发的整体结果汇总。"""

    report_code: str
    target_company: str
    brand_id: str
    total: int = 0
    succeeded: int = 0
    degraded: int = 0
    items: List[DispatchTaskResult] = Field(default_factory=list)


class DistributionStatus(BaseModel):
    """下游内容分发系统连通性探测结果。"""

    enabled: bool = False
    configured: bool = False
    base_url: str = ""
    reachable: bool = False
    detail: str = ""
    latency_ms: float = 0.0
