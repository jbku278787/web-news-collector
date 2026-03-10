"""
澎湃新闻爬虫
"""
from datetime import datetime

from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class ThePaperCrawler(BaseCrawler):
    """
    澎湃新闻 (thepaper.cn)
    """

    source_id = "thepaper"
    source_name = "澎湃新闻"
    source_url = "https://www.thepaper.cn"
    category = "general"
    crawl_interval = 300

    NEWS_API = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"

    async def fetch(self) -> list[NewsItemCreate]:
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.get(self.NEWS_API)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", {}).get("hotNews", []):
                title = item.get("name", "")
                if not title:
                    continue

                cont_id = item.get("contId", "")
                url = f"https://www.thepaper.cn/newsDetail_forward_{cont_id}"

                pub_time = item.get("pubTimeLong")
                published_at = (
                    datetime.utcfromtimestamp(pub_time / 1000)
                    if pub_time
                    else None
                )

                items.append(
                    NewsItemCreate(
                        title=title,
                        url=url,
                        source_id=self.source_id,
                        cover_image=item.get("pic", ""),
                        published_at=published_at,
                        category="general",
                    )
                )

        except Exception as e:
            logger.warning(f"[thepaper] 抓取失败: {e}")

        return items
