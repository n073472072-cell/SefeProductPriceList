# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.models import * # 匯入所有 models 以便建立資料表
from app.routers import auth, users, products, news

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 伺服器啟動中...")
    Base.metadata.create_all(bind=engine)
    print("✅ 資料庫資料表已檢查/建立")
    yield
    print("🌙 伺服器已關閉")

app = FastAPI(
    title="協飛產品詢價系統 API",
    description="提供產品查詢、使用者認證與最新消息管理功能。",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API 路由
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(news.router, prefix="/api/news", tags=["News"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "協飛 API 運行中", "docs": "/docs"}

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy"}