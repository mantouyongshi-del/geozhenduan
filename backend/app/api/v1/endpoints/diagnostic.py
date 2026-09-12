from fastapi import APIRouter, Depends, HTTPException, Query, Request, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import re
import time
from collections import defaultdict
from app.core.config import settings
from app.core.database import get_db
from app.core.uscc import validate_or_none
from app.models.diagnostic import DiagnosticReport
from app.schemas.diagnostic import (
    DiagnosticCreateRequest, DiagnosticReportOut,
    GenerateQueriesRequest, GenerateQueriesResponse
)
from app.services.diagnostic_service import DiagnosticService
from app.services.amap_service import AmapService
from app.services.distribution_client import schedule_auto_dispatch

router = APIRouter()

# 内部控制台授权口令（保护删除等破坏性接口免遭外部公网穿透滥用）
INTERNAL_CONSOLE_TOKEN = "xunling-console-secure-access-2026"
# 报告单号安全白名单正则（严禁任何 SQL 注入、路径穿越或脚本探测字符）
REPORT_CODE_PATTERN = re.compile(r"^[A-Za-z0-9\-_]{6,50}$")

class SecurityShield:
    """
    轻量级防攻击、防穿透与防爆破熔断安全盾
    1. 报告单号严格白名单校验（防御 SQL 注入、路径穿越、XSS 探测）
    2. IP 滑动窗口频次限制（防高频 DoS 刷接口）
    3. 异常遍历探测熔断机制（防批量爆破枚举其他企业客户体检报告）
    4. 敏感破坏性管理接口权限隔离（防外部通过公开页面越权穿透删除数据）
    """
    def __init__(self):
        # 记录 IP 请求时间戳: {ip: [ts1, ts2, ...]}
        self.request_timestamps = defaultdict(list)
        # 记录 IP 查询 404 不存在报告的时间戳: {ip: [ts1, ts2, ...]}
        self.failed_lookups = defaultdict(list)
        # 被熔断锁定的 IP 及解封时间戳: {ip: unblock_timestamp}
        self.blocked_ips = {}

    def get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        return request.client.host if request.client else "127.0.0.1"

    def check_ip_status(self, ip: str):
        now = time.time()
        if ip in self.blocked_ips:
            unblock_time = self.blocked_ips[ip]
            if now < unblock_time:
                remaining = int(unblock_time - now)
                raise HTTPException(
                    status_code=429,
                    detail=f"安全系统拦截：检测到该 IP 存在高频探测或异常扫号行为，已触发安全熔断保护，请等待 {remaining} 秒后再试"
                )
            else:
                del self.blocked_ips[ip]

    def record_and_limit_rate(self, ip: str, max_requests: int = 120, window_seconds: int = 60):
        """滑动窗口限流"""
        now = time.time()
        timestamps = self.request_timestamps[ip]
        valid_ts = [t for t in timestamps if now - t < window_seconds]
        valid_ts.append(now)
        self.request_timestamps[ip] = valid_ts

        if len(valid_ts) > max_requests:
            raise HTTPException(
                status_code=429,
                detail="请求频次过高，系统已触发流量保护，请稍候再试"
            )

    def record_failed_lookup(self, ip: str):
        """记录一次 404 探测失败，若 60 秒内累计超过 8 次即判定为恶意枚举爆破，熔断锁定 10 分钟"""
        now = time.time()
        failures = self.failed_lookups[ip]
        valid_failures = [t for t in failures if now - t < 60]
        valid_failures.append(now)
        self.failed_lookups[ip] = valid_failures

        if len(valid_failures) >= 8:
            self.blocked_ips[ip] = now + 600  # 锁定 10 分钟
            raise HTTPException(
                status_code=429,
                detail="系统检测到连续尝试探测未授权或不存在的报告，判定为恶意探测攻击，已熔断封禁该 IP 10 分钟"
            )

    def validate_report_code(self, report_code: str):
        """报告单号格式防御校验"""
        if not report_code or not REPORT_CODE_PATTERN.match(report_code):
            raise HTTPException(
                status_code=400,
                detail="报告单号格式不合法，拒绝处理潜在的注入或遍历参数"
            )

security_shield = SecurityShield()

@router.post("/run", response_model=DiagnosticReportOut)
async def run_enterprise_diagnostic(payload: DiagnosticCreateRequest, request: Request, db: Session = Depends(get_db)):
    """
    【蜉蝣小宝 · 售前获客核武器】
    输入准客户企业名称与核心搜索词，真实调度主流 AI 搜索引擎，出具深度可见度体检报告
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)
    # 单 IP 限制 5 分钟内最多发起 6 次全网真实探测评测，防止 API 配额被恶意刷爆
    security_shield.record_and_limit_rate(f"run:{ip}", max_requests=6, window_seconds=300)

    target_company = payload.target_company.strip()
    if not target_company:
        raise HTTPException(status_code=400, detail="企业名称不能为空")
    if len(target_company) > 100:
        raise HTTPException(status_code=400, detail="企业名称长度不能超过100字符")
    if not payload.keywords or len(payload.keywords) == 0:
        raise HTTPException(status_code=400, detail="至少需输入一个测试关键词")
    if len(payload.keywords) > 8:
        raise HTTPException(status_code=400, detail="单次体检关键词不能超过8个")

    # 统一社会信用代码：可选字段，但"填了就必须对"。
    # 必须在 try 之前校验 —— 下面的兜底会把一切异常吞成 500，
    # 而格式错误是可修正的客户端输入问题，必须返回 422 让前端明确提示。
    try:
        uscc_value = validate_or_none(payload.uscc)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    payload.uscc = uscc_value

    try:
        report = await DiagnosticService.execute_diagnostic(payload, db)
        report_out = DiagnosticService.get_report_by_code(report.report_code, db)
        if settings.DISTRIBUTION_AUTO_DISPATCH:
            # 体检产出 GeoActionTask 后，自动下发给下游 03 内容分发系统。
            # 走后台任务不阻塞体检报告实时返回，失败静默降级（AGENTS.md 五.3）。
            schedule_auto_dispatch(report_out)
        return report_out
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"体检执行异常: {str(e)}")

@router.post("/generate_queries", response_model=GenerateQueriesResponse)
async def generate_intent_queries_endpoint(payload: GenerateQueriesRequest, request: Request):
    """
    【DeepSeek Flash 裁判中枢 · 30 题高拟真意图生成器】
    覆盖 8 大决策维度，动态生成专属于企业画像的真实消费者/采购者 AI 搜索提问
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)
    security_shield.record_and_limit_rate(f"gen_queries:{ip}", max_requests=30, window_seconds=60)

    try:
        queries = await DiagnosticService.generate_intent_queries(
            brand_name=payload.brand_name.strip(),
            industry=payload.industry.strip(),
            city=payload.city.strip() if payload.city else "全国",
            company_name=payload.company_name.strip() if payload.company_name else None,
            target_audience=payload.target_audience,
            key_products=payload.key_products,
            count=payload.count or 30
        )
        return {"queries": queries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"意图提问生成异常: {str(e)}")

@router.get("/poi_suggest")
async def poi_suggest_endpoint(
    request: Request,
    keywords: str = Query(..., min_length=1, max_length=60),
    city: Optional[str] = Query(None)
):
    """
    【高德权威 POI 智能联想与多门店消歧防呆接口】
    1. 输入品牌/企业名称自动联想标准名称、官方地址与所属区县；
    2. 自动检测多门店/连锁泛称（如“万豪酒店”），输出消歧预警与具体分店候选；
    3. 支持一键将官方门牌地址、客服电话反填至事实标尺。
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)
    security_shield.record_and_limit_rate(f"poi:{ip}", max_requests=120, window_seconds=60)

    try:
        return await AmapService.suggest_pois(keywords=keywords, city=city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"高德POI联想异常: {str(e)}")

@router.get("/poi_detail")
async def poi_detail_endpoint(
    request: Request,
    poi_id: Optional[str] = Query(None),
    name: Optional[str] = Query(None)
):
    """
    获取单体 POI 官方核准详情（地址、电话、标签、坐标）
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)
    security_shield.record_and_limit_rate(f"poidetail:{ip}", max_requests=120, window_seconds=60)

    try:
        return await AmapService.get_poi_fact_detail(poi_id=poi_id or "", name=name or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取POI详情异常: {str(e)}")

@router.get("/models/balance")
async def get_ai_models_balance(request: Request):
    """
    实时获取全网各大 AI 模型的算力余额与运行状态 (DeepSeek, Kimi, 通义千问, 豆包等)
    内部销售控制台专用，支持实时对账与余额预警
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)
    security_shield.record_and_limit_rate(f"balance:{ip}", max_requests=60, window_seconds=60)
    
    try:
        return await DiagnosticService.get_models_balance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型余额失败: {str(e)}")

@router.get("/recent/list")
def list_recent_diagnostics(
    request: Request,
    limit: int = 15,
    db: Session = Depends(get_db)
):
    """
    获取加盟商销售顾问近期生成的体检报告列表 (内部工作台使用)
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)
    security_shield.record_and_limit_rate(f"recent:{ip}", max_requests=45, window_seconds=60)

    reports = db.query(DiagnosticReport).order_by(DiagnosticReport.created_at.desc()).limit(limit).all()
    results = []
    for r in reports:
        results.append({
            "report_code": r.report_code,
            "target_company": r.target_company,
            "brand_name": r.brand_name,
            "industry": r.industry,
            "uscc": getattr(r, "uscc", None),
            "visibility_score": r.visibility_score,
            "risk_level": r.risk_level,
            "created_at": r.created_at,
            "share_url": f"http://localhost:5173/#/diagnostic_report?code={r.report_code}&share=true"
        })
    return results

@router.delete("/recent/clear")
def clear_recent_diagnostics(
    request: Request,
    x_console_token: Optional[str] = Header(None, alias="X-Console-Token"),
    db: Session = Depends(get_db)
):
    """
    一键清空所有历史体检诊断报告数据 (内部受限接口，严格校验安全令牌，阻断外部越权穿透删除)
    """
    ip = security_shield.get_client_ip(request)
    security_shield.check_ip_status(ip)

    if x_console_token != INTERNAL_CONSOLE_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="越权操作拦截：该操作仅限授权内部销售控制台执行"
        )

    try:
        from app.models.diagnostic import DiagnosticItem
        db.query(DiagnosticItem).delete()
        deleted_count = db.query(DiagnosticReport).delete()
        db.commit()
        return {"success": True, "deleted_count": deleted_count, "message": "历史诊断记录已成功清空"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"清空历史数据失败: {str(e)}")

@router.get("/{report_code}", response_model=DiagnosticReportOut)
def get_diagnostic_report(
    report_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    通过专属报告码获取公开只读体检诊断书 (支持微信 H5 扫码打开与一键打印 PDF)
    具备防注入、防枚举爆破与防 DoS 穿透安全防护
    """
    ip = security_shield.get_client_ip(request)
    # 1. 检查 IP 是否被安全熔断
    security_shield.check_ip_status(ip)
    # 2. 报告单号严格白名单校验（防御 SQL 注入、路径穿越、XSS 探测）
    security_shield.validate_report_code(report_code)
    # 3. 滑动窗口限流
    security_shield.record_and_limit_rate(f"query:{ip}", max_requests=80, window_seconds=60)

    try:
        return DiagnosticService.get_report_by_code(report_code, db)
    except ValueError:
        # 记录 404 探测；若高频探测不存在的单号，将立即触发熔断封禁
        security_shield.record_failed_lookup(ip)
        raise HTTPException(status_code=404, detail="未找到该体检报告，可能已过期或链接有误")
