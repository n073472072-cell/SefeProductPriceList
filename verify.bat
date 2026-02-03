@echo off
chcp 65001 > nul
echo ========== 專案結構驗證 ==========

set STATUS=PASS

if not exist "frontend\package.json" (echo [FAIL] 缺少 frontend\package.json && set STATUS=FAIL)
if not exist "backend\app\main.py" (echo [FAIL] 缺少 backend\app\main.py && set STATUS=FAIL)
if not exist "README.md" (echo [FAIL] 缺少 README.md && set STATUS=FAIL)
if not exist "start_all.bat" (echo [FAIL] 缺少 start_all.bat && set STATUS=FAIL)

echo ==================================
if "%STATUS%"=="PASS" (
    echo ✅ 專案驗證成功！所有必要檔案皆已建立。
) else (
    echo ❌ 專案驗證失敗，請檢查遺漏檔案。
)
pause
