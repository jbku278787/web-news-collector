"""
新闻源管理 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crawlers.registry import get_all_crawlers, get_crawler
from app.models.news import NewsItem
from app.schemas.source import SourceResponse, SourceStatusResponse

router = APIRouter()


@router.get("", response_model=list[dict])
async def list_sources():
    """列出所有可用的新闻源"""
    crawlers = get_all_crawlers()
    return [
        {
            "id": crawler.source_id,
            "name": crawler.source_name,
            "url": crawler.source_url,
            "category": crawler.category,
            "crawl_interval": crawler.crawl_interval,
        }
        for crawler in crawlers.values()
    ]


@router.get("/status", response_model=SourceStatusResponse)
async def get_sources_status(
    db: AsyncSession = Depends(get_db),
):
    """获取所有源的状态概览"""
    crawlers = get_all_crawlers()

    # 查询每个源的新闻数
    query = (
        select(NewsItem.source_id, func.count(NewsItem.id))
        .group_by(NewsItem.source_id)
    )
    result = await db.execute(query)
    counts = dict(result.all())

    total_items = sum(counts.values())
    sources = []
    for source_id, crawler in crawlers.items():
        sources.append(
            SourceResponse(
                id=crawler.source_id,
                name=crawler.source_name,
                url=crawler.source_url,
                category=crawler.category,
                crawler_type="api",
                crawl_interval=crawler.crawl_interval,
                enabled=True,
                total_items=counts.get(source_id, 0),
            )
        )

    return SourceStatusResponse(
        total_sources=len(crawlers),
        active_sources=len(crawlers),
        total_items=total_items,
        sources=sources,
    )


@router.post("/{source_id}/crawl")
async def trigger_crawl(source_id: str):
    """手动触发某个源的抓取"""
    from app.workers.crawler_scheduler import crawl_source

    crawler = get_crawler(source_id)
    if not crawler:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"未找到源: {source_id}")

    # 异步执行抓取
    import asyncio
    asyncio.create_task(crawl_source(source_id))

    return {"message": f"已触发 {source_id} 抓取任务", "source": crawler.source_name}
