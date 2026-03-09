"""
新浪财经爬虫
"""
from datetime import datetime

from bs4 import BeautifulSoup
from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class SinaFinanceCrawler(BaseCrawler):
    """
    新浪财经 (finance.sina.com.cn)
    """

    source_id = "sina_finance"
    source_name = "新浪财经"
    source_url = "https://finance.sina.com.cn"
    category = "finance"
    crawl_interval = 300

    # 要闻 API
    NEWS_API = "https://feed.mix.sina.com.cn/api/roll/get"

    async def fetch(self) -> list[NewsItemCreate]:
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.get(
                self.NEWS_API,
                params={
                    "pageid": "153",
                    "lid": "2516",
                    "k": "",
                    "num": 50,
                    "page": 1,
                    "r": "0.1",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("result", {}).get("data", []):
                title = item.get("title", "")
                if not title:
                    continue

                ctime = item.get("ctime", "")
                published_at = self.parse_datetime(ctime, "%Y-%m-%d %H:%M:%S")

                items.append(
                    NewsItemCreate(
                        title=title,
                        url=item.get("url", ""),
                        source_id=self.source_id,
                        content=item.get("summary", ""),
                        cover_image=item.get("img", {}).get("u", ""),
                        author=item.get("media_name", ""),
                        published_at=published_at,
                        category="finance",
                    )
                )

        except Exception as e:
            logger.warning(f"[sina_finance] 抓取失败: {e}")

        return items
