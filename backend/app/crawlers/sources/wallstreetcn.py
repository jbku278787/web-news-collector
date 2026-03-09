"""
华尔街见闻爬虫
"""
from datetime import datetime

from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class WallStreetCNCrawler(BaseCrawler):
    """
    华尔街见闻 (wallstreetcn.com)

    API: https://api-one.wallstcn.com/apiv1/content/lives
    """

    source_id = "wallstreetcn"
    source_name = "华尔街见闻"
    source_url = "https://wallstreetcn.com"
    category = "finance"
    crawl_interval = 180

    LIVES_API = "https://api-one.wallstcn.com/apiv1/content/lives"
    NEWS_API = "https://api-one.wallstcn.com/apiv1/content/articles"

    async def fetch(self) -> list[NewsItemCreate]:
        items = []

        # 实时快讯
        lives = await self._fetch_lives()
        items.extend(lives)

        return items

    async def _fetch_lives(self) -> list[NewsItemCreate]:
        """抓取 7×24 实时快讯"""
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.get(
                self.LIVES_API,
                params={"channel": "global-channel", "limit": 50},
            )
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", {}).get("items", []):
                content_text = item.get("content_text", "") or item.get("title", "")
                if not content_text:
                    continue

                display_time = item.get("display_time")
                published_at = (
                    datetime.fromtimestamp(display_time) if display_time else None
                )

                uri = item.get("uri", "") or str(item.get("id", ""))
                url = f"https://wallstreetcn.com/live/{uri}"

                items.append(
                    NewsItemCreate(
                        title=content_text[:200],
                        url=url,
                        source_id=self.source_id,
                        content=content_text,
                        published_at=published_at,
                        category="finance",
                    )
                )

        except Exception as e:
            logger.warning(f"[wallstreetcn] 快讯抓取失败: {e}")

        return items
