#!/bin/bash
# 關閉 set -e 以免背景進程意外終止導致整個腳本退出
# set -e 

echo "=========================================="
echo "🚀 啟動協飛全端環境 (Zeabur Single-Port Mode)"
echo "=========================================="

# 建立必要的資料夾
mkdir -p backend/data

# 啟動後端 (監聽 127.0.0.1 即可，由前端代理)
echo "📦 啟動後端服務 (FastAPI on 8000)..."
cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > backend_output.log 2>&1 &
BACKEND_PID=$!

# 返回根目錄
cd ..

# 檢查後端是否啟動成功 (簡單輪詢)
echo "⏳ 等待後端服務準備中..."
sleep 3

# 啟動前端 (主要對外端口)
echo "🎨 啟動前端代理服務 (Express on 3000)..."
cd frontend
node server.js
