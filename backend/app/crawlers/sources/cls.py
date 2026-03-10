"""
财联社爬虫 - 核心财经信息源
"""
from datetime import datetime

from loguru import logger

from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate


class CLSCrawler(BaseCrawler):
    """
    财联社 (cls.cn) 快讯与要闻抓取

    API:
    - 快讯: https://www.cls.cn/nodeapi/updateTelegraphList
    - 要闻: https://www.cls.cn/nodeapi/rollnewsListV2
    """

    source_id = "cls"
    source_name = "财联社"
    source_url = "https://www.cls.cn"
    category = "finance"
    crawl_interval = 120  # 财联社更新频率高，2分钟一次

    # 快讯 API
    TELEGRAPH_API = "https://www.cls.cn/nodeapi/updateTelegraphList"
    # 要闻 API
    ROLL_NEWS_API = "https://www.cls.cn/nodeapi/rollnewsListV2"

    async def fetch(self) -> list[NewsItemCreate]:
        items = []

        # 抓取快讯
        telegraph_items = await self._fetch_telegraph()
        items.extend(telegraph_items)

        # 抓取要闻
        roll_items = await self._fetch_roll_news()
        items.extend(roll_items)

        return items

    async def _fetch_telegraph(self) -> list[NewsItemCreate]:
        """抓取实时快讯"""
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.get(
                self.TELEGRAPH_API,
                params={"app": "CailianpressWeb", "os": "web", "sv": "8.4.6"},
            )
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", {}).get("roll_data", []):
                title = item.get("title", "") or item.get("content", "")
                if not title:
                    continue

                # 去除 HTML 标签（简单处理）
                title = title.replace("<em>", "").replace("</em>", "")
                content = item.get("content", "")

                ctime = item.get("ctime")
                published_at = (
                    datetime.utcfromtimestamp(ctime) if ctime else None
                )

                url = f"https://www.cls.cn/detail/{item.get('id', '')}"

                items.append(
                    NewsItemCreate(
                        title=title[:200],
                        url=url,
                        source_id=self.source_id,
                        content=content,
                        published_at=published_at,
                        category="finance",
                    )
                )
        except Exception as e:
            logger.warning(f"[cls] 快讯抓取失败: {e}")

        return items

    async def _fetch_roll_news(self) -> list[NewsItemCreate]:
        """抓取滚动要闻"""
        client = await self.get_client()
        items: list[NewsItemCreate] = []

        try:
            resp = await client.get(
                self.ROLL_NEWS_API,
                params={"app": "CailianpressWeb", "os": "web", "sv": "8.4.6"},
            )
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", {}).get("roll_data", []):
                title = item.get("title", "")
                if not title:
                    continue

                ctime = item.get("ctime")
                published_at = (
                    datetime.utcfromtimestamp(ctime) if ctime else None
                )

                article_url = item.get("shareurl") or f"https://www.cls.cn/detail/{item.get('id', '')}"

                items.append(
                    NewsItemCreate(
                        title=title[:200],
                        url=article_url,
                        source_id=self.source_id,
                        content=item.get("brief", ""),
                        cover_image=item.get("img", ""),
                        published_at=published_at,
                        category="finance",
                    )
                )
        except Exception as e:
            logger.warning(f"[cls] 要闻抓取失败: {e}")

        return items
