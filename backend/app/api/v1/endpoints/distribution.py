"""跨仓工单下发端点。

体检报告生成后，把其中的 `GeoActionTask` 工单主动推送到下游 03 内容分发系统，
补齐"01 雷达诊断 → 03 内容工厂"的自动闭环第一跳。

- POST /dispatch  推送指定报告的工单（可指定 brand_id / task_ids）
- GET  /status    探测下游连通性，便于前端与运维一键自检
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.distribution import (
    DispatchBatchResult,
    DispatchRequest,
    DistributionStatus,
)
from app.services.diagnostic_service import DiagnosticService
from app.services.distribution_client import distribution_client

router = APIRouter()


@router.post("/dispatch", response_model=DispatchBatchResult, summary="下发体检工单到内容分发系统")
async def dispatch_report_tasks(
    payload: DispatchRequest, db: Session = Depends(get_db)
) -> DispatchBatchResult:
    """从已生成的体检报告提取工单并推送到下游 03。

    下游不可用或未配置时按 AGENTS.md 五.3 优雅降级——返回 degraded 明细而非 500。
    """
    try:
        report = DiagnosticService.get_report_by_code(payload.report_code, db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="体检报告不存在") from exc

    tasks = list(report.geo_tasks or [])
    if not tasks:
        raise HTTPException(status_code=422, detail="该报告未产出可下发的 GeoActionTask 工单")

    if payload.task_ids:
        wanted = set(payload.task_ids)
        missing = wanted - {getattr(t, "id", None) for t in tasks}
        if missing:
            raise HTTPException(
                status_code=400, detail=f"指定的工单不存在: {sorted(missing)}"
            )

    return await distribution_client.dispatch_report(
        report, brand_id=payload.brand_id, task_ids=payload.task_ids
    )


@router.get("/status", response_model=DistributionStatus, summary="探测下游内容分发系统连通性")
async def distribution_status() -> DistributionStatus:
    return await distribution_client.probe()
