"""
快讯时间轴 API - 对标财联社的 7×24 快讯流
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crawlers.registry import get_all_crawlers
from app.models.news import NewsItem
from app.schemas.news import NewsTimelineItem

router = APIRouter()


@router.get("", response_model=list[NewsTimelineItem])
async def get_timeline(
    category: Optional[str] = Query(None, description="栏目: finance/tech/general/world"),
    hours: int = Query(24, ge=1, le=168, description="时间范围（小时）"),
    limit: int = Query(100, ge=1, le=500),
    before: Optional[str] = Query(None, description="加载更早的新闻（游标分页）"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取实时快讯时间轴

    模拟财联社 7×24 快讯模式：
    - 按时间倒序排列
    - 支持按栏目过滤
    - 支持游标分页加载更多
    """
    crawlers = get_all_crawlers()
    source_names = {c.source_id: c.source_name for c in crawlers.values()}

    query = select(NewsItem)

    # 时间范围
    since = datetime.utcnow() - timedelta(hours=hours)
    query = query.where(NewsItem.published_at >= since)

    # 栏目过滤
    if category:
        query = query.where(NewsItem.category == category)

    # 游标分页
    if before:
        try:
            cursor_time = datetime.fromisoformat(before)
            query = query.where(NewsItem.published_at < cursor_time)
        except ValueError:
            pass

    query = query.order_by(desc(NewsItem.published_at)).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    return [
        NewsTimelineItem(
            id=item.id,
            title=item.title,
            url=item.url,
            source_id=item.source_id,
            source_name=source_names.get(item.source_id, item.source_id),
            summary=item.summary,
            sentiment=item.sentiment,
            tags=item.tags,
            importance=item.importance or 0,
            published_at=item.published_at,
        )
        for item in items
    ]


@router.get("/stats")
async def get_timeline_stats(
    db: AsyncSession = Depends(get_db),
):
    """获取时间轴统计信息"""
    now = datetime.utcnow()

    # 最近24小时各栏目统计
    since_24h = now - timedelta(hours=24)

    query = (
        select(NewsItem.category, func.count(NewsItem.id))
        .where(NewsItem.published_at >= since_24h)
        .group_by(NewsItem.category)
    )
    result = await db.execute(query)
    category_counts = dict(result.all())

    # 最近24小时情绪分布
    sentiment_query = (
        select(NewsItem.sentiment, func.count(NewsItem.id))
        .where(NewsItem.published_at >= since_24h)
        .where(NewsItem.sentiment.isnot(None))
        .group_by(NewsItem.sentiment)
    )
    result = await db.execute(sentiment_query)
    sentiment_counts = dict(result.all())

    return {
        "period": "24h",
        "total": sum(category_counts.values()),
        "by_category": category_counts,
        "by_sentiment": sentiment_counts,
    }
