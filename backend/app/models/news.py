"""
新闻数据模型
"""
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, DateTime, Float, JSON, Index,
)
from app.core.database import Base


class NewsItem(Base):
    """新闻条目"""
    __tablename__ = "news_items"

    id = Column(String(64), primary_key=True)  # source_id + hash(url)
    source_id = Column(String(32), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(2000), nullable=False)
    content = Column(Text, nullable=True)  # 全文内容
    summary = Column(Text, nullable=True)  # AI 摘要
    cover_image = Column(String(2000), nullable=True)
    author = Column(String(200), nullable=True)

    # 财经特有字段
    sentiment = Column(String(20), nullable=True)  # positive / negative / neutral
    sentiment_score = Column(Float, nullable=True)  # -1.0 ~ 1.0
    tags = Column(JSON, nullable=True)  # ["科技", "互联网", "阿里巴巴"]
    sectors = Column(JSON, nullable=True)  # 行业板块 ["消费电子", "半导体"]
    stocks = Column(JSON, nullable=True)  # 关联个股 ["AAPL", "600519"]
    importance = Column(Integer, default=0)  # 重要性 0-5

    # 时间
    published_at = Column(DateTime, nullable=True, index=True)
    crawled_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)  # AI 处理完成时间

    # 元信息
    category = Column(String(50), nullable=True, index=True)  # 栏目分类
    extra = Column(JSON, nullable=True)  # 额外字段

    __table_args__ = (
        Index("ix_news_source_published", "source_id", "published_at"),
        Index("ix_news_category_published", "category", "published_at"),
    )
