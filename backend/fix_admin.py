import sqlite3
import os

# 確保資料夾存在
os.makedirs("data", exist_ok=True)
db_path = "data/app.db"

# 直接連接資料庫並寫入一個測試帳號 (密碼 123 的雜湊值)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 建立使用者資料表 (如果還沒建立的話)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    hashed_password TEXT,
    role TEXT
)
''')

# 插入帳號：admin / 密碼：123
# 注意：這裡是用 plain text 測試，如果後端有加密邏輯，這只是讓你確認資料庫能動
try:
    cursor.execute("INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)", 
                   ("admin", "123", "admin"))
    conn.commit()
    print("✅ 成功建立帳號：admin / 密碼：123")
except:
    print("❌ 帳號可能已存在或資料表結構不符")

conn.close()