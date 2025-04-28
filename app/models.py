from sqlalchemy import Column, Integer, String, Text, DateTime,Boolean
from datetime import datetime
from app.database import Base
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(String)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False, nullable=False)
    summary = Column(String, nullable=True)  # New field


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    summary = Column(String, nullable=True)  # New fiel


