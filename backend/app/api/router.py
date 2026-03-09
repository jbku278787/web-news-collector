"""
API 路由汇总
"""
from fastapi import APIRouter

from app.api.routes import news, sources, timeline

api_router = APIRouter()

api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
