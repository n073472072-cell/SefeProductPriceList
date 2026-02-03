#!/bin/bash
# 協飛產品系統 - 雲端啟動腳本 (修正版本)

echo "=========================================="
echo "🚀 啟動協飛全端環境 (Zeabur)"
echo "=========================================="

# 確保在根目錄
cd /app

# 1. 建立資料庫目錄並賦予權限
echo "📂 建立資料夾並檢查權限..."
mkdir -p /app/backend/data
chmod 777 /app/backend/data

# 2. 初始化資料庫 (確保 admin 帳號存在)
echo "📦 初始化資料庫..."
cd /app/backend
# 強制設定環境變數，確保使用絕對路徑
export DATABASE_URL="sqlite:////app/backend/data/app.db"
python3 init_db.py || echo "⚠️ 資料庫初始化跳過或已完成"

# 3. 啟動後端 (使用 bg 運行)
echo "⚙️  啟動後端 FastAPI (Port: 8000)..."
# 同樣對後端 API 指定絕對路徑的資料庫連結
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 4. 啟動前端 (主服務，Port: 3000)
echo "🌐 啟動前端 Express (Port: 3000)..."
cd /app/frontend
node server.js
