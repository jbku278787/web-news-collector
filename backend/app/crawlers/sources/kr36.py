"""
36氪爬虫
"""
from datetime import datetime

from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class Kr36Crawler(BaseCrawler):
    """
    36氪 (36kr.com)
    """

    source_id = "36kr"
    source_name = "36氪"
    source_url = "https://36kr.com"
    category = "tech"
    crawl_interval = 300

    NEWS_API = "https://gateway.36kr.com/api/mis/nav/home/nav/rank/hot"

    async def fetch(self) -> list[NewsItemCreate]:
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.post(
                self.NEWS_API,
                json={"partner_id": "wap", "timestamp": int(datetime.now().timestamp())},
                headers={
                    "Referer": "https://36kr.com/",
                    "Origin": "https://36kr.com",
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            hot_list = data.get("data", {}).get("hotRankList", [])
            for item in hot_list:
                template = item.get("templateMaterial", {})
                title = template.get("widgetTitle", "")
                if not title:
                    continue

                item_id = template.get("itemId", "")
                url = f"https://36kr.com/p/{item_id}"

                pub_time = template.get("publishTime")
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
                        content=template.get("widgetContent", ""),
                        cover_image=template.get("widgetImage", ""),
                        author=template.get("authorName", ""),
                        published_at=published_at,
                        category="tech",
                    )
                )

        except Exception as e:
            logger.warning(f"[36kr] 抓取失败: {e}")

        return items
