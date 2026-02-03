# backend/app/schemas/news.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    is_active: bool = True

class NewsCreate(NewsBase):
    publish_at: Optional[datetime] = None

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    publish_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class NewsResponse(NewsBase):
    id: int
    publish_at: datetime
    created_at: datetime
    class Config:
        from_attributes = True
