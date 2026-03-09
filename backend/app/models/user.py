"""
用户数据模型
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Text
from app.core.database import Base


class User(Base):
    """用户"""
    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    email = Column(String(200), nullable=True, unique=True)
    username = Column(String(100), nullable=True)
    avatar = Column(String(500), nullable=True)
    auth_type = Column(String(20), default="github")  # github / email

    # 用户偏好
    preferences = Column(JSON, nullable=True)  # 关注源、栏目布局等
    subscriptions = Column(JSON, nullable=True)  # 订阅推送配置

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
