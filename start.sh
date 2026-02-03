#!/bin/bash
# 協飛產品系統 - 雲端部署啟動腳本 (強化資料庫連結)

echo "--- [$(date)] 伺服器啟動中 ---"

# 1. 確保工作目錄與資料夾權限
cd /app
mkdir -p /app/backend/data
chmod 777 /app/backend/data || true

# 2. 強制設定全局環境變數
export DATABASE_URL="sqlite:////app/backend/data/app.db"
export PYTHONIOENCODING=utf-8
export PYTHONUNBUFFERED=1

# 3. 初始化與診斷
cd /app/backend
echo "📦 正在檢查數據庫狀態..."
python3 init_db.py
echo "🔍 執行系統診斷..."
python3 diagnose_db.py || echo "❌ 診斷過程發生錯誤"

# 4. 啟動後端 FastAPI (監聽所有位址)
echo "⚙️  啟動後端程序..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers &
BACKEND_PID=$!

# 5. 啟動前端 Express 代理
echo "🌐 啟動前端入口..."
cd /app/frontend

# 檢查後端是否維持運行
sleep 3
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ 錯誤：後端啟動後意外結束，請檢查上面的報錯訊息。"
fi

exec node server.js
