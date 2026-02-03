#!/bin/bash
# 協飛產品系統 - 雲端啟動腳本 (權限與路徑強化版)

echo "=========================================="
echo "🚀 啟動協飛全端環境 (Zeabur)"
echo "=========================================="

# 確保在根目錄
cd /app

# 1. 強制建立資料夾並賦予最高讀寫權限
echo "📂 處理資料庫目錄..."
mkdir -p /app/backend/data
chmod 777 /app/backend/data || true
# 如果已有資料庫，也確保權限正確
if [ -f "/app/backend/data/app.db" ]; then
    chmod 666 /app/backend/data/app.db || true
fi

# 2. 清理可能干擾的舊設定 (雲端環境不依賴 .env 檔案路徑)
if [ -f "backend/.env" ]; then
    echo "🧹 移除舊的 .env 設定檔以避免路徑衝突..."
    rm backend/.env
fi

# 3. 初始化資料庫
echo "📦 初始化資料庫與管理員帳號..."
cd /app/backend
# 再次明確注入絕對路徑環境變數
export DATABASE_URL="sqlite:////app/backend/data/app.db"
python3 init_db.py

# 4. 啟動後端 (使用 bg 運行)
echo "⚙️  啟動後端 FastAPI (Port: 8000)..."
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 5. 啟動前端 (主服務，Port: 3000)
echo "🌐 啟動前端 Express (Port: 3000)..."
cd /app/frontend
node server.js
