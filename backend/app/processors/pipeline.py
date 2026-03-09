"""
新闻处理管道
将抓取的原始新闻数据经过清洗、去重、AI加工后入库
"""
from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crawlers.base import BaseCrawler
from app.models.news import NewsItem
from app.processors.ai_processor import ai_processor
from app.schemas.news import NewsItemCreate


class NewsPipeline:
    """新闻处理管道"""

    def __init__(self, db: AsyncSession, enable_ai: bool = True):
        self.db = db
        self.enable_ai = enable_ai

    async def process(self, items: list[NewsItemCreate]) -> int:
        """
        处理一批新闻条目
        返回实际新增的条目数
        """
        new_count = 0

        for item in items:
            try:
                # 1. 生成 ID
                item_id = BaseCrawler.make_id(item.source_id, item.url)

                # 2. 检查是否已存在（去重）
                existing = await self.db.get(NewsItem, item_id)
                if existing:
                    continue

                # 3. AI 加工（可选）
                ai_result = {}
                if self.enable_ai:
                    try:
                        ai_result = await ai_processor.process_news(
                            title=item.title,
                            content=item.content or "",
                        )
                    except Exception as e:
                        logger.warning(f"AI 处理跳过: {e}")

                # 4. 入库
                news_item = NewsItem(
                    id=item_id,
                    source_id=item.source_id,
                    title=item.title,
                    url=item.url,
                    content=item.content,
                    cover_image=item.cover_image,
                    author=item.author,
                    published_at=item.published_at,
                    crawled_at=datetime.utcnow(),
                    category=item.category,
                    # AI 加工字段
                    summary=ai_result.get("summary"),
                    sentiment=ai_result.get("sentiment"),
                    sentiment_score=ai_result.get("sentiment_score"),
                    tags=ai_result.get("tags"),
                    sectors=ai_result.get("sectors"),
                    stocks=ai_result.get("stocks"),
                    importance=ai_result.get("importance", 0),
                    processed_at=datetime.utcnow() if ai_result else None,
                )

                self.db.add(news_item)
                new_count += 1

            except Exception as e:
                logger.error(f"处理新闻条目失败: {item.title[:50]} - {e}")
                continue

        if new_count > 0:
            await self.db.commit()
            logger.info(f"管道处理完成: {new_count}/{len(items)} 条新增入库")

        return new_count
