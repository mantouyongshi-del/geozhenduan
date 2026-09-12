import time
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, comment="企业官方注册全称")
    short_name = Column(String(100), nullable=True, comment="企业简称/品牌主名")
    logo_url = Column(String(500), nullable=True, comment="企业Logo")
    industry = Column(String(100), nullable=True, comment="所属行业")

    # 统一社会信用代码 (GB 32100-2015, 18 位)
    # 跨系统全局实体主键的权威来源：下游内容工厂/知识库均以 USCC 关联品牌档案。
    # 缺失时下游只能降级为 `{企业全称}::{城市}` 联合主键，将检索不到官方事实而走兜底语料，
    # 因此生产环境应尽量补全本字段（AGENTS.md 五.1）。
    uscc = Column(
        String(18), nullable=True, index=True, comment="统一社会信用代码（全局实体主键）"
    )
    
    # 品牌别名 / 泛化匹配词 (以换行或逗号分隔，如: 嘉兴市莱沃科技培训有限公司, 科莱沃机器人, 莱沃科技培训)
    brand_aliases = Column(Text, nullable=False, default="", comment="品牌泛化词，用于大模型答案匹配")
    
    # 状态
    is_active = Column(Boolean, default=True)
    created_at = Column(Integer, default=lambda: int(time.time()))
    updated_at = Column(Integer, default=lambda: int(time.time()), onupdate=lambda: int(time.time()))

    # 关联
    keywords = relationship("Keyword", back_populates="company", cascade="all, delete-orphan")
    audit_records = relationship("AuditRecord", back_populates="company", cascade="all, delete-orphan")
    daily_stats = relationship("DailyStat", back_populates="company", cascade="all, delete-orphan")

    def get_alias_list(self):
        if not self.brand_aliases:
            return [self.name]
        return [a.strip() for a in self.brand_aliases.replace("，", ",").replace("|", ",").split(",") if a.strip()]
