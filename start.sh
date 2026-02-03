#!/bin/bash
# 確保腳本在出錯時停止
set -e

echo "=========================================="
echo "🚀 啟動協飛全端環境 (Linux/Zeabur)"
echo "=========================================="

# 建立必要的資料夾
mkdir -p backend/data

# 啟動後端 (背景執行)
echo "📦 啟動後端 (FastAPI on port 8000)..."
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 返回根目錄
cd ..

# 啟動前端
echo "🎨 啟動前端 (Express on port 3000)..."
cd frontend
node server.js

# 如果前端停止了，也殺掉後端
kill $BACKEND_PID
