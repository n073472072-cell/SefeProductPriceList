#!/bin/bash
echo "=========================================="
echo "🚀 啟動協飛全端環境 (Linux/Zeabur)"
echo "=========================================="

# 安裝後端依賴 (如果需要)
if [ -f "backend/requirements.txt" ]; then
    echo "📦 檢查/安裝後端依賴..."
    pip3 install -r backend/requirements.txt --break-system-packages
fi

# 啟動後端 (背景執行)
echo "📦 啟動後端 (FastAPI on port 8000)..."
cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 返回根目錄
cd ..

# 啟動前端
echo "🎨 啟動前端 (Express on port 3000)..."
cd frontend && node server.js
