"""
RSS 通用爬虫 - 支持任意 RSS/Atom 源
"""
from datetime import datetime
from typing import Optional

import feedparser
from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class RSSCrawler(BaseCrawler):
    """
    RSS / Atom 通用爬虫

    用法:
        crawler = RSSCrawler(
            source_id="36kr",
            source_name="36氪",
            source_url="https://36kr.com",
            feed_url="https://36kr.com/feed",
            category="tech",
        )
        items = await crawler.run()
    """

    feed_url: str = ""
    max_items: int = 50

    def __init__(
        self,
        source_id: str = "",
        source_name: str = "",
        source_url: str = "",
        feed_url: str = "",
        category: str = "general",
        max_items: int = 50,
    ):
        super().__init__()
        if source_id:
            self.source_id = source_id
        if source_name:
            self.source_name = source_name
        if source_url:
            self.source_url = source_url
        if feed_url:
            self.feed_url = feed_url
        if category:
            self.category = category
        self.max_items = max_items

    async def fetch(self) -> list[NewsItemCreate]:
        client = await self.get_client()
        resp = await client.get(self.feed_url)
        resp.raise_for_status()

        feed = feedparser.parse(resp.text)
        items: list[NewsItemCreate] = []

        for entry in feed.entries[: self.max_items]:
            published_at = self._parse_feed_date(entry)
            url = entry.get("link", "")
            if not url:
                continue

            items.append(
                NewsItemCreate(
                    title=entry.get("title", "").strip(),
                    url=url,
                    source_id=self.source_id,
                    content=entry.get("summary", ""),
                    author=entry.get("author", ""),
                    published_at=published_at,
                    category=self.category,
                )
            )

        return items

    @staticmethod
    def _parse_feed_date(entry) -> Optional[datetime]:
        """从 feedparser entry 解析发布时间（feedparser 返回 UTC struct_time）"""
        for field in ("published_parsed", "updated_parsed"):
            parsed = entry.get(field)
            if parsed:
                try:
                    import calendar
                    # calendar.timegm 把 UTC struct_time → Unix timestamp，再存为 UTC datetime
                    return datetime.utcfromtimestamp(calendar.timegm(parsed))
                except Exception:
                    continue
        return None
