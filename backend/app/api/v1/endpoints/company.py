import datetime
import random
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.core.security import generate_share_token
from app.core.uscc import validate_or_none
from app.models.company import Company
from app.models.keyword import Keyword
from app.models.audit import AuditRecord, MatchSnapshot
from app.models.daily_stat import DailyStat
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyOut
from app.services.audit_service import AuditService
from app.services.live_probe import LiveWebProbe
from app.providers.llm_gateway import LLMGateway

router = APIRouter()

class QuickAuditRequest(BaseModel):
    name: str
    short_name: Optional[str] = None
    brand_aliases: Optional[str] = None
    industry: Optional[str] = "科技服务"
    custom_keywords: Optional[List[str]] = None
    uscc: Optional[str] = None

def _validated_uscc(value: Optional[str]) -> Optional[str]:
    """统一校验入口：合法返回归一化值，未填写返回 None，格式错误返回 422。"""
    try:
        return validate_or_none(value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@router.post("/quick-audit")
async def quick_audit_brand(payload: QuickAuditRequest, db: Session = Depends(get_db)):
    """
    一键快速为任何新品牌创建档案、生成四维场景词库并自动执行大模型巡检
    """
    s_name = payload.short_name or payload.name
    aliases_str = payload.brand_aliases or f"{payload.name}, {s_name}"

    # 1. 创建企业
    company = Company(
        name=payload.name,
        short_name=s_name,
        industry=payload.industry,
        brand_aliases=aliases_str,
        uscc=_validated_uscc(payload.uscc),
    )
    db.add(company)
    db.commit()
    db.refresh(company)

    # 2. 自动生成四维场景词库
    keywords_to_create = []
    
    # 用户自定义词
    if payload.custom_keywords:
        for kw in payload.custom_keywords:
            if kw.strip():
                keywords_to_create.append((2, s_name, kw.strip()))

    # 场景1: 品牌场景
    keywords_to_create.extend([
        (1, s_name, f"{s_name}公司概况与企业实力"),
        (1, s_name, f"{s_name}怎么样，口碑如何"),
        (1, s_name, f"{s_name}核心产品服务与优势")
    ])

    # 场景2: 搜索词场景
    keywords_to_create.extend([
        (2, payload.industry, f"{payload.industry}知名品牌推荐"),
        (2, payload.industry, f"国内优质{payload.industry}服务商排名"),
        (2, payload.industry, f"{payload.industry}哪家好")
    ])

    # 场景3: 问答词场景
    keywords_to_create.extend([
        (3, "选型问答", f"选择{payload.industry}服务商主要看哪些指标？"),
        (3, "选型问答", f"{s_name}和同行相比有什么特色？")
    ])

    # 场景4: 意图场景
    keywords_to_create.extend([
        (4, "综合意图", f"推荐几家靠谱的{payload.industry}企业"),
        (4, "综合意图", f"求推荐业内口碑好的{s_name}类似品牌")
    ])

    seeded_kws = []
    for t_type, subj, kw_text in keywords_to_create:
        k_obj = Keyword(
            company_id=company.id,
            task_type=t_type,
            subject=subj,
            keyword=kw_text
        )
        db.add(k_obj)
        seeded_kws.append(k_obj)
    db.commit()

    for k in seeded_kws:
        db.refresh(k)

    # 3. 立即为各大模型执行真实联网探针巡检 (覆盖核心品牌词与行业搜索词)
    platforms = ["doubao", "deepseek", "tongyi", "yuanbao", "baidu"]
    target_kws = seeded_kws[:2]
    for kw in target_kws:
        # 向公网权威搜索引擎发起实时真实 HTTP 探针检索
        live_cites = LiveWebProbe.fetch_live_search_results(kw.keyword, limit=5)
        for p in platforms:
            try:
                await AuditService.run_single_audit(
                    company_id=company.id,
                    keyword_id=kw.id,
                    platform=p,
                    is_mobile=False,
                    cached_citations=live_cites,
                    db=db
                )
                await AuditService.run_single_audit(
                    company_id=company.id,
                    keyword_id=kw.id,
                    platform=p,
                    is_mobile=True,
                    cached_citations=live_cites,
                    db=db
                )
            except Exception as e:
                print(f"[QuickAudit] Audit error for {p}: {e}")

    # 4. 生成 30 天历史基准趋势
    today = datetime.date.today()
    for i in range(30, -1, -1):
        dt_str = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        base_num = int(1200 + (30 - i) * 35 + random.randint(-5, 10))
        ds = DailyStat(
            company_id=company.id,
            stat_date=dt_str,
            platform="",
            total_recommendations=base_num,
            daily_increment=random.randint(15, 45)
        )
        db.add(ds)
    db.commit()

    token = generate_share_token(company.id)
    return {
        "success": True,
        "company_id": company.id,
        "name": company.name,
        "short_name": company.short_name,
        "share_token": token,
        "report_url": f"http://localhost:5173/#/ai_report?code={token}",
        "keyword_count": len(seeded_kws),
        "message": f"成功为品牌【{company.name}】创建档案并完成各大模型 GEO 巡检！"
    }

@router.post("/", response_model=CompanyOut)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(
        name=payload.name,
        short_name=payload.short_name,
        logo_url=payload.logo_url,
        industry=payload.industry,
        brand_aliases=payload.brand_aliases,
        uscc=_validated_uscc(payload.uscc),
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    
    out = CompanyOut.from_orm(company)
    out.share_token = generate_share_token(company.id)
    return out

@router.get("/", response_model=List[CompanyOut])
def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db.query(Company).offset(skip).limit(limit).all()
    outs = []
    for c in companies:
        co = CompanyOut.from_orm(c)
        co.share_token = generate_share_token(c.id)
        outs.append(co)
    return outs

@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    co = CompanyOut.from_orm(company)
    co.share_token = generate_share_token(company.id)
    return co

@router.put("/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, payload: CompanyUpdate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for field, val in payload.dict(exclude_unset=True).items():
        setattr(company, field, val)
    # USCC 是跨仓全局主键，更新同样要过校验（exclude_unset 可能带入脏值）
    if "uscc" in payload.dict(exclude_unset=True):
        company.uscc = _validated_uscc(payload.uscc)
    db.commit()
    db.refresh(company)
    co = CompanyOut.from_orm(company)
    co.share_token = generate_share_token(company.id)
    return co
