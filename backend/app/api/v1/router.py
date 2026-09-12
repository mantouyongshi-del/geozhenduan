from fastapi import APIRouter
from app.api.v1.endpoints import company, keyword, audit, report, diagnostic, distribution

api_router = APIRouter()

api_router.include_router(company.router, prefix="/companies", tags=["企业管理"])
api_router.include_router(keyword.router, prefix="/keywords", tags=["词库矩阵"])
api_router.include_router(audit.router, prefix="/audit", tags=["巡检引擎"])
api_router.include_router(report.router, prefix="/report", tags=["客户报表与数据看板"])
api_router.include_router(diagnostic.router, prefix="/diagnostic", tags=["准客户售前AI体检引擎"])
api_router.include_router(distribution.router, prefix="/distribution", tags=["下游内容分发舰队对接"])
