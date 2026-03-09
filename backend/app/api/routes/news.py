"""
新闻 API 路由
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.news import NewsItem
from app.schemas.news import NewsItemResponse, NewsListResponse, SourceNewsResponse

router = APIRouter()


@router.get("", response_model=NewsListResponse)
async def get_news(
    source_id: Optional[str] = Query(None, description="按新闻源过滤"),
    category: Optional[str] = Query(None, description="按栏目过滤: finance/tech/general/world"),
    sentiment: Optional[str] = Query(None, description="情绪过滤: positive/negative/neutral"),
    tag: Optional[str] = Query(None, description="按标签过滤"),
    importance_min: int = Query(0, ge=0, le=5, description="最低重要性"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取新闻列表（支持多维度过滤）"""
    query = select(NewsItem)

    # 过滤条件
    if source_id:
        query = query.where(NewsItem.source_id == source_id)
    if category:
        query = query.where(NewsItem.category == category)
    if sentiment:
        query = query.where(NewsItem.sentiment == sentiment)
    if importance_min > 0:
        query = query.where(NewsItem.importance >= importance_min)
    if tag:
        # JSON 数组包含查询（SQLite 用 LIKE，PostgreSQL 可用 @>）
        query = query.where(NewsItem.tags.contains(tag))

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # 分页 + 排序（按发布时间倒序）
    query = (
        query.order_by(desc(NewsItem.published_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(query)
    items = result.scalars().all()

    return NewsListResponse(
        items=[NewsItemResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size < total),
    )


@router.get("/{news_id}", response_model=NewsItemResponse)
async def get_news_detail(
    news_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取新闻详情"""
    item = await db.get(NewsItem, news_id)
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="新闻不存在")
    return NewsItemResponse.model_validate(item)


@router.get("/source/{source_id}", response_model=SourceNewsResponse)
async def get_news_by_source(
    source_id: str,
    limit: int = Query(30, ge=1, le=100),
    latest: bool = Query(False, description="强制刷新"),
    db: AsyncSession = Depends(get_db),
):
    """获取指定源的最新新闻"""
    from app.core.cache import cache_get, cache_set
    from app.crawlers.registry import get_crawler

    crawler = get_crawler(source_id)
    source_name = crawler.source_name if crawler else source_id

    # 检查缓存
    if not latest:
        cached = await cache_get(f"source:{source_id}")
        if cached:
            return SourceNewsResponse(
                source_id=source_id,
                source_name=source_name,
                items=[NewsItemResponse(**item) for item in cached["items"]],
                status="cache",
                cached=True,
            )

    # 从数据库查询
    query = (
        select(NewsItem)
        .where(NewsItem.source_id == source_id)
        .order_by(desc(NewsItem.published_at))
        .limit(limit)
    )
    result = await db.execute(query)
    items = result.scalars().all()

    response_items = [NewsItemResponse.model_validate(item) for item in items]

    # 写入缓存
    await cache_set(
        f"source:{source_id}",
        {"items": [item.model_dump(mode="json") for item in response_items]},
    )

    return SourceNewsResponse(
        source_id=source_id,
        source_name=source_name,
        items=response_items,
        status="success",
        updated_at=datetime.utcnow(),
        cached=False,
    )
