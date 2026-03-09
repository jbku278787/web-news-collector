"""
Redis 缓存管理
"""
import json
from typing import Optional

import redis.asyncio as redis
from loguru import logger

from app.core.config import settings

_redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """获取 Redis 客户端（懒初始化）"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis_client


async def cache_get(key: str) -> Optional[dict]:
    """从缓存获取数据"""
    try:
        r = await get_redis()
        data = await r.get(f"news:{key}")
        if data:
            return json.loads(data)
    except Exception as e:
        logger.warning(f"Redis cache_get failed: {e}")
    return None


async def cache_set(key: str, value: dict, ttl: int = None):
    """写入缓存"""
    if ttl is None:
        ttl = settings.CACHE_TTL
    try:
        r = await get_redis()
        await r.setex(f"news:{key}", ttl, json.dumps(value, ensure_ascii=False))
    except Exception as e:
        logger.warning(f"Redis cache_set failed: {e}")


async def cache_delete(key: str):
    """删除缓存"""
    try:
        r = await get_redis()
        await r.delete(f"news:{key}")
    except Exception as e:
        logger.warning(f"Redis cache_delete failed: {e}")
