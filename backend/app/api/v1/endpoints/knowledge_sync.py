"""M7.1 跨仓事实回流端点：把体检产出的事实基准库同步到 02 品牌知识库。

设计对齐 `distribution.py`（工单下发）的既有范式：
- 正常路径返回 200 + 结构化结果；
- 下游不可用**不返回 5xx**（语义上属于可重试的降级，而非本服务故障），
  由结果体的 `degraded=True` + `reason` 表达，避免把上游故障放大成级联失败；
- 报告不存在 404，报告无事实 422。
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.knowledge_sync import (
    KnowledgeSyncRequest,
    KnowledgeSyncResult,
    KnowledgeSyncStatus,
)
from app.services.diagnostic_service import DiagnosticService
from app.services.knowledge_sync_client import knowledge_sync_client

# 前缀由 router.py 统一挂载（与 distribution.py 同约定），此处不重复声明
router = APIRouter()


@router.post(
    "/sync",
    response_model=KnowledgeSyncResult,
    summary="把指定体检报告的事实基准库回流到 02 品牌知识库",
)
async def sync_report_facts(
    payload: KnowledgeSyncRequest,
    db: Session = Depends(get_db),
) -> KnowledgeSyncResult:
    report = DiagnosticService.get_report_by_code(payload.report_code, db)
    if report is None:
        raise HTTPException(status_code=404, detail=f"未找到分享码为 {payload.report_code} 的体检报告")

    result = await knowledge_sync_client.sync_report(report, brand_id=payload.brand_id)
    result.report_code = payload.report_code
    if (
        not result.ok
        and not result.synced
        and "未登记合法统一社会信用代码" in result.reason
    ):
        # 报告压根没填 USCC：属于输入问题，明确 422 让调用方去补录，而不是伪装成功
        raise HTTPException(status_code=422, detail=result.reason)
    return result


@router.get(
    "/status",
    response_model=KnowledgeSyncStatus,
    summary="下游知识库连通性自检",
)
async def knowledge_sync_status() -> KnowledgeSyncStatus:
    return await knowledge_sync_client.probe()
