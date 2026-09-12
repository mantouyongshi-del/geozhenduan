from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DiagnosticCreateRequest(BaseModel):
    target_company: str
    brand_name: str
    industry: str
    city: Optional[str] = "全国"
    keywords: List[str]
    agency_name: Optional[str] = "蜉蝣小宝 · 官方直营授权运营中心"
    consultant_name: Optional[str] = "资深数字化营销顾问"
    consultant_phone: Optional[str] = None
    brand_facts: Optional[List[Dict[str, str]]] = None
    target_audience: Optional[str] = None
    key_products: Optional[str] = None

class CitationDetail(BaseModel):
    title: str
    url: str
    site_name: str
    summary: Optional[str] = ""

class ApiCertificationDetail(BaseModel):
    cert_id: str
    provider: str
    model_family: str
    api_endpoint: str
    trace_id: str
    compliance_record: str
    duration_ms: int
    token_count: int
    verification_hash: str
    cert_seal_text: str
    is_live_call: bool = True

class DecisionSceneContrast(BaseModel):
    id: str
    platform: str
    platform_name: str
    model_name: str
    inquiry_scenario: str
    buyer_intent: str
    contrast_type: str = "interception"  # "interception" (失守截流) 或 "defense" (优势守擂)
    state_badge: str = "⚠️ 关键阵地 · 竞品截流"
    winner: str = "competitor"  # "competitor" 或 "target"
    target_rank: int = 0
    competitor_brand: str
    competitor_status_tag: str
    competitor_quote: str
    competitor_advantage_tags: List[str]
    buyer_reaction_competitor: str
    target_brand: str
    target_status_tag: str
    target_quote: str
    target_vulnerability_tags: List[str]
    buyer_reaction_target: str
    interception_verdict: str

class DiagnosticItemOut(BaseModel):
    id: int
    keyword: str
    platform: str
    platform_name: str
    model_name: Optional[str] = ""
    is_target_mentioned: bool
    target_rank: int
    mined_competitors: List[str]
    raw_content: str
    citations: List[CitationDetail]
    duration_ms: int
    api_certification: Optional[ApiCertificationDetail] = None

class CompetitorAnalysisItem(BaseModel):
    name: str
    mention_count: int
    dominant_platforms: List[str]
    advantage_points: str

class GeoPrescription(BaseModel):
    scenario: str
    task_type: int
    urgency: str
    action: str
    expected_result: str

class FunnelLayerItem(BaseModel):
    layer_key: str
    name: str
    score: int
    max_score: int = 25
    status: str
    status_label: str
    diagnosis: str
    core_evidence: str

class DualDeviceItem(BaseModel):
    platform_key: str
    platform_name: str
    device: str
    is_mobile: bool
    is_indexed: bool
    status_desc: str

class CompetitorSourceItem(BaseModel):
    site_name: str
    source_type: str
    citation_count: int
    target_coverage: str
    competitor_names: List[str]
    threat_level: str

class EconomicLossEstimate(BaseModel):
    industry: str
    estimated_unit_price: int
    unit_price_desc: str
    monthly_search_inquiries: int
    monthly_lost_leads_min: int
    monthly_lost_leads_max: int
    monthly_loss_amount_min: int
    monthly_loss_amount_max: int
    annual_loss_amount_est: int
    payback_leads_needed: int
    calculation_note: str

class ImplementationPhase(BaseModel):
    phase: int
    day_range: str
    title: str
    core_action: str
    deliverable: str
    expected_kpi: str

class FactCheckItem(BaseModel):
    fact_key: str
    expected_value: str
    claimed_value: Optional[str] = None
    status: str = "verified"  # verified / conflict / unmentioned / hallucination
    risk_level: str = "low"   # low / medium / high
    explanation: str

class GeoActionTask(BaseModel):
    id: str
    priority: str  # P0 / P1 / P2
    title: str
    category: str  # content / citation / technical
    action: str
    target_platform: str
    expected_impact: str
    deadline_days: int
    recommended_platforms: Optional[List[str]] = []
    suggested_title: Optional[str] = None
    core_keywords: Optional[List[str]] = []
    format_guide: Optional[str] = None

class AivsDimensionScores(BaseModel):
    presence_rate: float        # 品牌出现率 (0-100)
    recommendation_rate: float  # 明确推荐率 (0-100)
    rank_score: float           # 推荐排位分 (0-100)
    accuracy_rate: float        # 事实准确率 (0-100)
    citation_quality: float     # 引用质量 (0-100)
    stability: float            # 跨平台一致性 (0-100)
    composite_score: int        # AIVS 综合加权总分 (0-100)

class GenerateQueriesRequest(BaseModel):
    brand_name: str
    industry: str
    city: Optional[str] = "全国"
    company_name: Optional[str] = None
    target_audience: Optional[str] = None
    key_products: Optional[str] = None
    count: Optional[int] = 30

class GeneratedQueryItem(BaseModel):
    id: int
    category: str
    category_name: str
    query_text: str
    intent_rationale: str
    priority: str

class GenerateQueriesResponse(BaseModel):
    queries: List[GeneratedQueryItem]

class DiagnosticReportOut(BaseModel):
    id: int
    report_code: str
    target_company: str
    brand_name: str
    industry: str
    city: str
    search_keywords: List[str]
    agency_name: str
    consultant_name: str
    consultant_phone: Optional[str] = None
    visibility_score: int
    risk_level: str
    summary_verdict: str
    competitors: List[CompetitorAnalysisItem]
    prescriptions: List[GeoPrescription]
    funnel_metrics: Optional[List[FunnelLayerItem]] = []
    dual_device_matrix: Optional[List[DualDeviceItem]] = []
    competitor_sources: Optional[List[CompetitorSourceItem]] = []
    economic_loss: Optional[EconomicLossEstimate] = None
    implementation_roadmap: Optional[List[ImplementationPhase]] = []
    decision_contrasts: Optional[List[DecisionSceneContrast]] = []
    certification_summary: Optional[Dict[str, Any]] = None
    # 工业级重构增强呈现字段
    fact_checks: Optional[List[FactCheckItem]] = []
    geo_tasks: Optional[List[GeoActionTask]] = []
    aivs_dimensions: Optional[AivsDimensionScores] = None
    brand_facts: Optional[List[Dict[str, str]]] = []
    created_at: int
    items: List[DiagnosticItemOut]
    share_url: Optional[str] = None

