@echo off
chcp 65001 > nul
echo ==========================================
echo 🚀 啟動協飛全端開發環境
echo ==========================================

:: 設定環境變數以支援 UTF-8
SET PYTHONIOENCODING=utf-8

:: 檢查後端依賴是否已安裝 (檢查常用套件 fastapi)
py -c "import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo 📦 正在透過 pip 安裝後端依賴...
    cd backend
    py -m pip install fastapi uvicorn sqlalchemy aiosqlite python-multipart "python-jose[cryptography]" "passlib[bcrypt]" openpyxl pandas python-dotenv
    cd ..
)

:: 啟動後端
echo 📦 啟動後端 (FastAPI on port 8000)...
start "Backend-FastAPI" cmd /k "cd backend && py -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

:: 等待後端啟動
timeout /t 3 /nobreak >nul

:: 啟動前端
echo 🎨 啟動前端 (Express on port 3000)...
start "Frontend-Express" cmd /k "cd frontend && node server.js"

echo.
echo ==========================================
echo ✅ 服務已啟動！
echo 🎨 前端: http://localhost:3000
echo ⚙️  後端 API: http://localhost:8000
echo 📚 API 文件: http://localhost:8000/docs
echo.
echo 👉 請手動關閉命令提示字元視窗以停止服務
echo ==========================================
