import time
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class DiagnosticReport(Base):
    __tablename__ = "diagnostic_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_code = Column(String(64), unique=True, index=True, nullable=False, comment="体检报告唯一分享码")
    
    # 目标企业信息
    target_company = Column(String(255), nullable=False, index=True, comment="目标企业工商全称")
    brand_name = Column(String(100), nullable=False, index=True, comment="品牌常用简称")
    industry = Column(String(100), nullable=False, comment="所属行业领域")
    city = Column(String(50), nullable=True, default="全国", comment="目标地域/城市")
    
    # 测试的搜索词 JSON: ["关键词1", "关键词2"]
    search_keywords_json = Column(Text, nullable=False, comment="测试提示词列表")
    
    # 授权服务中心与顾问署名 (蜉蝣小宝加盟商)
    agency_name = Column(String(100), default="蜉蝣小宝 · 官方直营授权运营中心", comment="加盟商授权中心名称")
    consultant_name = Column(String(50), default="资深数字化顾问", comment="顾问姓名")
    consultant_phone = Column(String(50), nullable=True, comment="顾问联系方式")
    
    # 诊断核心指标
    visibility_score = Column(Integer, default=15, comment="AI 可见度综合健康得分 (0-100)")
    risk_level = Column(String(50), default="HIGH_RISK", comment="风险评级: HIGH_RISK, MEDIUM_RISK, LOW_RISK")
    summary_verdict = Column(Text, nullable=False, comment="一句话痛点诊断结论")
    
    # 挖掘出的同行竞品与解决方案 (JSON 存储)
    competitors_json = Column(Text, nullable=True, comment="同行霸屏与截流分析")
    prescriptions_json = Column(Text, nullable=True, comment="四维场景 GEO 处方建议")
    
    # 工业级重构增强字段 (DeepSeek Flash 裁判与事实核验)
    fact_checks_json = Column(Text, nullable=True, comment="原子事实核验结果 JSON")
    geo_tasks_json = Column(Text, nullable=True, comment="P0/P1/P2落地任务清单 JSON")
    brand_facts_json = Column(Text, nullable=True, comment="企业事实基准库 JSON")
    aivs_dimensions_json = Column(Text, nullable=True, comment="AIVS六维得分明细 JSON")
    
    created_at = Column(Integer, default=lambda: int(time.time()), index=True)

    # 关联单项测试记录
    items = relationship("DiagnosticItem", back_populates="report", cascade="all, delete-orphan")


class DiagnosticItem(Base):
    __tablename__ = "diagnostic_items"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("diagnostic_reports.id", ondelete="CASCADE"), nullable=False, index=True)
    
    keyword = Column(String(255), nullable=False, comment="提问搜索词")
    platform = Column(String(50), nullable=False, comment="平台标识: doubao, deepseek, tongyi, yuanbao, baidu")
    platform_name = Column(String(50), nullable=False, comment="大模型名称: 豆包, DeepSeek, 通义千问等")
    model_name = Column(String(100), nullable=True, comment="模型内核代号")
    
    # 检测结果
    is_target_mentioned = Column(Boolean, default=False, comment="目标客户是否被提及")
    target_rank = Column(Integer, default=0, comment="推荐位次(0为未收录)")
    
    # 挖掘出的竞品
    mined_competitors = Column(Text, nullable=True, comment="该问题下被大模型推荐的竞品(逗号分隔)")
    
    # 原始大模型回答与 RAG 引用
    raw_content = Column(Text, nullable=False, comment="大模型原始回答完整正文")
    citations_json = Column(Text, nullable=True, comment="大模型检索引用的外部信源")
    
    duration_ms = Column(Integer, default=1200, comment="探针耗时(毫秒)")

    report = relationship("DiagnosticReport", back_populates="items")
