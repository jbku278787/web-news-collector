"""
应用配置 - 从环境变量加载
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 基础
    APP_NAME: str = "web-news-collector"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # 后端
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 5173

    # 数据库
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/news.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI / LLM
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"

    # 爬虫
    CRAWL_INTERVAL: int = 600  # 秒
    CACHE_TTL: int = 1800  # 秒
    MAX_CONCURRENT_CRAWLERS: int = 10
    REQUEST_TIMEOUT: int = 15

    # GitHub OAuth
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_CALLBACK_URL: str = "http://localhost:5173/auth/callback"

    # 日志
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
