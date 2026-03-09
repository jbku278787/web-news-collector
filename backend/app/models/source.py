"""
新闻源数据模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from app.core.database import Base


class Source(Base):
    """新闻源配置"""
    __tablename__ = "sources"

    id = Column(String(32), primary_key=True)  # e.g. "cls", "wallstreetcn"
    name = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=True)
    url = Column(String(500), nullable=False)
    favicon = Column(String(500), nullable=True)
    category = Column(String(50), nullable=False)  # finance / tech / general / world
    color = Column(String(20), nullable=True)

    # 抓取配置
    crawler_type = Column(String(20), default="api")  # api / html / rss
    crawler_config = Column(JSON, nullable=True)  # 爬虫额外配置
    crawl_interval = Column(Integer, default=600)  # 秒
    enabled = Column(Boolean, default=True)

    # 统计
    last_crawled_at = Column(DateTime, nullable=True)
    total_items = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    last_error = Column(String(1000), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
