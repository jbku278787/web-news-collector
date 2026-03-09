"""
爬虫调度器 - 定时抓取新闻源
"""
import asyncio
import sys
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.core.config import settings
from app.core.database import async_session, init_db
from app.crawlers.registry import get_all_crawlers, get_crawler
from app.processors.pipeline import NewsPipeline


async def crawl_source(source_id: str):
    """抓取单个新闻源"""
    crawler = get_crawler(source_id)
    if not crawler:
        logger.warning(f"未找到爬虫: {source_id}")
        return

    try:
        items = await crawler.run()
        if items:
            async with async_session() as session:
                pipeline = NewsPipeline(
                    db=session,
                    enable_ai=bool(settings.LLM_API_KEY),
                )
                new_count = await pipeline.process(items)
                logger.info(
                    f"[{source_id}] 入库 {new_count} 条 / 共 {len(items)} 条"
                )
    except Exception as e:
        logger.error(f"[{source_id}] 抓取任务失败: {e}")


async def crawl_all():
    """抓取所有新闻源"""
    crawlers = get_all_crawlers()
    logger.info(f"开始全量抓取，共 {len(crawlers)} 个源...")

    # 并发抓取，但限制最大并发数
    semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_CRAWLERS)

    async def _limited_crawl(source_id: str):
        async with semaphore:
            await crawl_source(source_id)

    tasks = [_limited_crawl(sid) for sid in crawlers]
    await asyncio.gather(*tasks, return_exceptions=True)

    logger.info("全量抓取完成")


def start_scheduler():
    """启动定时调度器"""
    scheduler = AsyncIOScheduler()

    # 全量抓取任务
    scheduler.add_job(
        crawl_all,
        "interval",
        seconds=settings.CRAWL_INTERVAL,
        id="crawl_all",
        name="全量新闻抓取",
        next_run_time=datetime.now(),  # 启动时立即执行一次
    )

    scheduler.start()
    logger.info(
        f"爬虫调度器已启动，抓取间隔: {settings.CRAWL_INTERVAL}s"
    )
    return scheduler


async def main():
    """入口"""
    logger.info("🕷️  Web News Collector - Crawler Worker")

    # 初始化数据库
    await init_db()

    # 判断是否单次执行
    if "--once" in sys.argv:
        logger.info("单次执行模式")
        await crawl_all()
        return

    # 定时执行
    scheduler = start_scheduler()

    try:
        # 保持运行
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("爬虫调度器已停止")


if __name__ == "__main__":
    asyncio.run(main())
