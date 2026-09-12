from pydantic import BaseModel
from typing import Optional, List

class CompanyBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    brand_aliases: str
    uscc: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    brand_aliases: Optional[str] = None
    uscc: Optional[str] = None
    is_active: Optional[bool] = None

class CompanyOut(CompanyBase):
    id: int
    is_active: bool
    created_at: int
    updated_at: int
    share_token: Optional[str] = None

    class Config:
        from_attributes = True
