"""
爬虫基类 - 所有新闻源爬虫的公共抽象
"""
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

import httpx
from loguru import logger

from app.core.config import settings
from app.schemas.news import NewsItemCreate


class BaseCrawler(ABC):
    """
    新闻源爬虫基类

    每个新闻源实现一个子类，覆写 `fetch()` 方法即可。
    """

    source_id: str = ""
    source_name: str = ""
    source_url: str = ""
    category: str = "general"  # finance / tech / general / world
    crawl_interval: int = 600  # 默认抓取间隔（秒）

    # HTTP 客户端默认配置
    default_headers: dict = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        """懒加载 HTTP 客户端"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers=self.default_headers,
                timeout=httpx.Timeout(settings.REQUEST_TIMEOUT),
                follow_redirects=True,
            )
        return self._client

    async def close(self):
        """关闭 HTTP 客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @abstractmethod
    async def fetch(self) -> list[NewsItemCreate]:
        """
        抓取新闻源数据，返回结构化的新闻列表。
        子类必须实现此方法。
        """
        ...

    async def run(self) -> list[NewsItemCreate]:
        """执行抓取，带错误处理和日志"""
        try:
            logger.info(f"[{self.source_id}] 开始抓取 {self.source_name}...")
            items = await self.fetch()
            logger.info(f"[{self.source_id}] 抓取完成，获取 {len(items)} 条新闻")
            return items
        except Exception as e:
            logger.error(f"[{self.source_id}] 抓取失败: {e}")
            raise
        finally:
            await self.close()

    # ---------- 工具方法 ----------

    @staticmethod
    def make_id(source_id: str, url: str) -> str:
        """生成新闻条目 ID"""
        url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
        return f"{source_id}_{url_hash}"

    @staticmethod
    def parse_datetime(dt_str: str, fmt: str = None, cst_to_utc: bool = False) -> Optional[datetime]:
        """安全地解析时间字符串。cst_to_utc=True 时将尾部所1律视为 CST +8 转为 UTC"""
        if not dt_str:
            return None
        try:
            result = None
            if fmt:
                result = datetime.strptime(dt_str, fmt)
            else:
                # 尝试常见格式
                for f in [
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%dT%H:%M:%S.%f",
                    "%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M",
                    "%Y/%m/%d %H:%M:%S",
                ]:
                    try:
                        result = datetime.strptime(dt_str.strip(), f)
                        break
                    except ValueError:
                        continue
            if result is not None and cst_to_utc and result.tzinfo is None:
                result = result - timedelta(hours=8)  # CST (UTC+8) 转为 UTC
            return result
        except Exception:
            pass
        return None
