#!/bin/bash
# 協飛產品系統 - 雲端最終啟動腳本

echo "--- [$(date)] 系統啟動程序開始 ---"

# 確保在正確目錄
cd /app

# 1. 處理資料存放目錄
echo "📂 [Step 1] 準備資料庫目錄..."
mkdir -p /app/backend/data
chmod 777 /app/backend/data || true

# 2. 強制設定環境變數
export DATABASE_URL="sqlite:////app/backend/data/app.db"
export PYTHONIOENCODING=utf-8

# 3. 初始化資料庫 (確保 admin 存在)
echo "📦 [Step 2] 正在檢查/初始化資料庫..."
cd /app/backend
# 執行初始化，如果不成功也要繼續，以免阻礙主程式啟動
python3 init_db.py || echo "⚠️ 初始化腳本執行時遇到問題 (可能資料庫已存在)"

# 4. 啟動後端 FastAPI (改為監聽 0.0.0.0 以提高容器相容性)
echo "⚙️  [Step 3] 啟動後端 FastAPI (Port 8000)..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 5. 返回根目錄並啟動前端
cd /app
echo "🌐 [Step 4] 啟動前端 Express 代理 (Port 3000)..."
cd /app/frontend

# 檢查一下後端進程是否還活著
sleep 2
if ps -p $BACKEND_PID > /dev/null; then
   echo "✅ 後端進程 (PID: $BACKEND_PID) 運行中"
else
   echo "❌ 警告：後端進程似乎啟動失敗，請檢查日誌"
fi

# 執行前端主進程
exec node server.js
