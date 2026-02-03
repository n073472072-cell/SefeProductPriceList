# 協飛產品詢價系統

> 一個內部使用的產品價格查詢系統，支援使用者分級、價格查詢、最新消息公告及批次資料管理功能。

## 🚀 快速開始

### 環境需求
- Node.js 18+
- Python 3.10+

### 安裝步驟

1.  **安裝後端依賴**
    ```bash
    cd backend
    pip install fastapi uvicorn sqlalchemy aiosqlite python-multipart "python-jose[cryptography]" "passlib[bcrypt]" openpyxl pandas
    cd ..
    ```

2.  **安裝前端依賴**
    ```bash
    cd frontend
    npm install
    cd ..
    ```

3.  **建立第一個管理員帳號 (首次執行)**
    - 啟動後端伺服器。
    - 使用 Postman 或瀏覽器工具對 `http://localhost:8000/api/users/` 發送 POST 請求。
    - JSON: `{"username": "admin", "password": "yourpassword", "role": "admin"}`

4.  **啟動服務**
    執行根目錄下的 `start_all.bat` (Windows)。

### 存取網址
| 服務       | 網址                        |
| ---------- | --------------------------- |
| 🎨 前端    | http://localhost:3000       |
| ⚙️ 後端 API | http://localhost:8000       |
| 📚 API 文件 | http://localhost:8000/docs |

## 🛠 技術棧
- **前端**: Node.js + Express, Vanilla JS, Quill.js
- **後端**: Python + FastAPI
- **資料庫**: SQLite
- **資料處理**: Pandas, Openpyxl
