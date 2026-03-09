"""
新闻源相关 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SourceBase(BaseModel):
    id: str
    name: str
    name_en: Optional[str] = None
    url: str
    category: str
    favicon: Optional[str] = None
    color: Optional[str] = None


class SourceCreate(SourceBase):
    crawler_type: str = "api"
    crawler_config: Optional[dict] = None
    crawl_interval: int = 600
    enabled: bool = True


class SourceResponse(SourceBase):
    crawler_type: str
    crawl_interval: int
    enabled: bool
    last_crawled_at: Optional[datetime] = None
    total_items: int = 0
    error_count: int = 0
    last_error: Optional[str] = None

    class Config:
        from_attributes = True


class SourceStatusResponse(BaseModel):
    """源状态聚合"""
    total_sources: int
    active_sources: int
    total_items: int
    sources: list[SourceResponse]
