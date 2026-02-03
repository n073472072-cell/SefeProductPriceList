#!/bin/bash
# 協飛產品系統 - 雲端啟動腳本

echo "=========================================="
echo "🚀 啟動協飛全端環境 (Zeabur)"
echo "=========================================="

# 確保在根目錄
cd /app

# 1. 建立資料夾
echo "📂 建立資料夾..."
mkdir -p backend/data

# 2. 初始化資料庫 (確保 admin 帳號存在)
echo "📦 初始化資料庫..."
cd /app/backend
python3 init_db.py || echo "⚠️ 資料庫初始化跳過或已完成"

# 3. 啟動後端 (使用 bg 運行)
echo "⚙️  啟動後端 FastAPI (Port: 8000)..."
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 4. 啟動前端 (主服務，Port: 3000)
echo "🌐 啟動前端 Express (Port: 3000)..."
cd /app/frontend
# 檢查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 偵測到缺少 node_modules，正在安裝..."
    npm install
fi

# 啟動並保持在前台
node server.js
