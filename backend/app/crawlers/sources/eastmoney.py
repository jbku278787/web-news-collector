"""
东方财富爬虫
"""
from datetime import datetime

from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class EastMoneyCrawler(BaseCrawler):
    """
    东方财富 (eastmoney.com)

    API: https://np-listapi.eastmoney.com/comm/web/getNewsByColumns
    """

    source_id = "eastmoney"
    source_name = "东方财富"
    source_url = "https://www.eastmoney.com"
    category = "finance"
    crawl_interval = 300

    NEWS_API = "https://np-listapi.eastmoney.com/comm/web/getNewsByColumns"

    async def fetch(self) -> list[NewsItemCreate]:
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.get(
                self.NEWS_API,
                params={
                    "column": "102",
                    "showContent": 1,
                    "pageSize": 50,
                    "pageNo": 1,
                    "appname": "website",
                },
                headers={
                    "Referer": "https://www.eastmoney.com/",
                    "Origin": "https://www.eastmoney.com",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", {}).get("list", []):
                title = item.get("title", "")
                if not title:
                    continue

                art_code = item.get("art_code", "")
                url = item.get("url", "") or f"https://finance.eastmoney.com/a/{art_code}.html"

                showtime = item.get("showtime", "")
                published_at = self.parse_datetime(showtime)

                items.append(
                    NewsItemCreate(
                        title=title,
                        url=url,
                        source_id=self.source_id,
                        content=item.get("digest", ""),
                        cover_image=item.get("image", ""),
                        author=item.get("source", ""),
                        published_at=published_at,
                        category="finance",
                    )
                )

        except Exception as e:
            logger.warning(f"[eastmoney] 抓取失败: {e}")

        return items
