"""
爬虫注册中心 - 管理所有新闻源爬虫
"""
from typing import Type

from app.crawlers.base import BaseCrawler
from app.crawlers.rss_crawler import RSSCrawler

# 导入所有具体爬虫
from app.crawlers.sources.cls import CLSCrawler
from app.crawlers.sources.wallstreetcn import WallStreetCNCrawler
from app.crawlers.sources.sina_finance import SinaFinanceCrawler
from app.crawlers.sources.eastmoney import EastMoneyCrawler
from app.crawlers.sources.thepaper import ThePaperCrawler
from app.crawlers.sources.kr36 import Kr36Crawler


# ---------- 爬虫注册表 ----------
_CRAWLER_REGISTRY: dict[str, Type[BaseCrawler] | BaseCrawler] = {}


def register_crawler(crawler_cls: Type[BaseCrawler]):
    """注册爬虫类"""
    _CRAWLER_REGISTRY[crawler_cls.source_id] = crawler_cls
    return crawler_cls


def get_crawler(source_id: str) -> BaseCrawler | None:
    """获取爬虫实例"""
    cls_or_instance = _CRAWLER_REGISTRY.get(source_id)
    if cls_or_instance is None:
        return None
    if isinstance(cls_or_instance, BaseCrawler):
        return cls_or_instance
    return cls_or_instance()


def get_all_crawlers() -> dict[str, BaseCrawler]:
    """获取所有爬虫实例"""
    result = {}
    for source_id, cls_or_instance in _CRAWLER_REGISTRY.items():
        if isinstance(cls_or_instance, BaseCrawler):
            result[source_id] = cls_or_instance
        else:
            result[source_id] = cls_or_instance()
    return result


# ---------- 注册内置爬虫 ----------
register_crawler(CLSCrawler)
register_crawler(WallStreetCNCrawler)
register_crawler(SinaFinanceCrawler)
register_crawler(EastMoneyCrawler)
register_crawler(ThePaperCrawler)
register_crawler(Kr36Crawler)


# ---------- 预置 RSS 源 ----------
_RSS_SOURCES = [
    {
        "source_id": "jinse",
        "source_name": "金色财经",
        "source_url": "https://www.jinse.cn",
        "feed_url": "https://www.jinse.cn/rss",
        "category": "finance",
    },
    {
        "source_id": "zaobao",
        "source_name": "联合早报",
        "source_url": "https://www.zaobao.com",
        "feed_url": "https://www.zaobao.com/rss/znews-t.xml",
        "category": "world",
    },
    {
        "source_id": "techcrunch",
        "source_name": "TechCrunch",
        "source_url": "https://techcrunch.com",
        "feed_url": "https://techcrunch.com/feed/",
        "category": "tech",
    },
    {
        "source_id": "hackernews",
        "source_name": "Hacker News",
        "source_url": "https://news.ycombinator.com",
        "feed_url": "https://hnrss.org/best",
        "category": "tech",
    },
]

for rss_cfg in _RSS_SOURCES:
    _CRAWLER_REGISTRY[rss_cfg["source_id"]] = RSSCrawler(**rss_cfg)
