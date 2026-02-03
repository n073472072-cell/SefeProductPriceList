# backend/app/services/news_service.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate

def get_latest_active_news(db: Session) -> News:
    return db.query(News).filter(News.is_active == True).order_by(desc(News.publish_at)).first()

def create_news(db: Session, news: NewsCreate) -> News:
    db_news = News(**news.model_dump())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def get_all_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(News).order_by(desc(News.publish_at)).offset(skip).limit(limit).all()
