from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# Base schema for common fields
class PostBase(BaseModel):
    title: str
    content: str
    author: str
    summary: Optional[str] = None


# Schema for creating a post (no id or timestamps)
class PostCreate(PostBase):
    pass


# Schema for returning post data (includes id and timestamps)
class Post(PostBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = False

    class Config:
        orm_mode = True


# User creation schema
class UserCreate(BaseModel):
    username: str
    password: str


# Schema for returning user data
class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str


