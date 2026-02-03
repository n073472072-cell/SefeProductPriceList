#!/bin/bash
# 協飛產品系統 - 雲端啟動腳本 (最終診斷版)

# 顯示所有執行的指令與日誌
# set -x

echo "--- 系統啟動中 ---"
date
whoami
pwd

# 1. 資料夾與權限
echo "📂 檢查資料夾權限..."
mkdir -p /app/backend/data
chmod 777 /app/backend/data || true

# 2. 初始化資料庫
echo "📦 正在初始化資料庫..."
cd /app/backend
export DATABASE_URL="sqlite:////app/backend/data/app.db"
# 使用 python3 直接執行，並將錯誤輸出到標準輸出
python3 init_db.py 2>&1

# 3. 啟動後端
echo "⚙️  正在背景啟動 FastAPI (Port 8000)..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug &
# 給予一點時間啟動
sleep 5

# 4. 啟動前端代理 (主程序)
echo "🌐 正在啟動前端 Express 代理 (Port 3000)..."
cd /app/frontend
# 確保 node 執行
exec node server.js
