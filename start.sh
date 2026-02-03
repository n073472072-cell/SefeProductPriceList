#!/bin/bash
# 協飛產品系統 - 雲端最終啟動腳本

echo "--- [$(date)] 伺服器初始化中 ---"

cd /app

# 1. 資料夾與權限
mkdir -p /app/backend/data
chmod 777 /app/backend/data || true

# 2. 環境變數
export DATABASE_URL="sqlite:////app/backend/data/app.db"
export PYTHONIOENCODING=utf-8

# 3. 初始化資料庫
cd /app/backend
echo "📦 正在檢查/初始化數據庫..."
python3 init_db.py || echo "⚠️ 初始化略過"

# 4. 啟動後端 FastAPI
echo "⚙️  正在啟動後端 FastAPI (Port 8000)..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 5. 啟動前端代理
cd /app/frontend
echo "🌐 正在啟動前端服務 (Port 3000)..."

# 給予後端一點啟動餘裕
sleep 3

# 執行主程序
exec node server.js
