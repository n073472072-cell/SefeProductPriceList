#!/bin/bash
echo "=========================================="
echo "🚀 啟動協飛全端環境 (Zeabur Single-Port Mode)"
echo "=========================================="

# 建立必要的資料夾
mkdir -p backend/data

# 啟動後端
echo "📦 初始化資料庫與管理員帳號..."
cd backend
python3 init_db.py

echo "📦 啟動後端服務 (FastAPI on 8000)..."
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > /app/backend_output.log 2>&1 &
BACKEND_PID=$!

# 返回根目錄
cd /app

# 檢查後端是否啟動成功 (給予足夠的寬限時間)
echo "⏳ 等待後端服務準備中 (Max 30s)..."
for i in {1..30}; do
    if grep -q "Uvicorn running on" /app/backend_output.log; then
        echo "✅ 後端已準備就緒！"
        break
    fi
    echo "..."
    sleep 1
done

# 啟動前端 (主要對外端口 3000)
echo "🎨 啟動前端服務 (Express on 3000)..."
cd frontend
node server.js
