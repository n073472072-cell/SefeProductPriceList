# backend/app/routers/news.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.news import NewsCreate, NewsUpdate, NewsResponse
from app.services import news_service
from app.security.dependencies import get_current_admin_user

router = APIRouter()

@router.get("/latest", response_model=Optional[NewsResponse])
def get_latest_news(db: Session = Depends(get_db)):
    """(公開) 取得最新一則有效公告"""
    return news_service.get_latest_active_news(db)

@router.post("/", response_model=NewsResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin_user)])
def create_new_announcement(news: NewsCreate, db: Session = Depends(get_db)):
    """新增最新消息 (僅限管理員)"""
    return news_service.create_news(db, news)

@router.get("/", response_model=List[NewsResponse], dependencies=[Depends(get_current_admin_user)])
def read_all_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """取得所有消息 (僅限管理員管理用)"""
    return news_service.get_all_news(db, skip, limit)
