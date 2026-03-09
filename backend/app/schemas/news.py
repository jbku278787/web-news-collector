"""
新闻相关 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NewsItemBase(BaseModel):
    title: str
    url: str
    source_id: str
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    category: Optional[str] = None


class NewsItemCreate(NewsItemBase):
    pass


class NewsItemResponse(NewsItemBase):
    id: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    tags: Optional[list[str]] = None
    sectors: Optional[list[str]] = None
    stocks: Optional[list[str]] = None
    importance: int = 0
    crawled_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NewsTimelineItem(BaseModel):
    """快讯时间轴条目（精简版）"""
    id: str
    title: str
    url: str
    source_id: str
    source_name: str = ""
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    tags: Optional[list[str]] = None
    importance: int = 0
    published_at: Optional[datetime] = None


class NewsListResponse(BaseModel):
    """新闻列表响应"""
    items: list[NewsItemResponse]
    total: int
    page: int
    page_size: int
    has_more: bool


class SourceNewsResponse(BaseModel):
    """单个源的新闻数据响应"""
    source_id: str
    source_name: str
    items: list[NewsItemResponse]
    status: str = "success"  # success / cache / error
    updated_at: Optional[datetime] = None
    cached: bool = False
