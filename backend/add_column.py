import sys
import os

# 將當前目錄加入 sys.path 以便匯入 backend 模組
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import text
from app.database import engine

def add_column():
    print("正在新增 full_name 欄位到 users 資料表...")
    with engine.connect() as conn:
        try:
            # 檢查是否已存在 (SQLite 不支援 IF NOT EXISTS 的 ADD COLUMN，所以直接 try-except)
            conn.execute(text("ALTER TABLE users ADD COLUMN full_name VARCHAR"))
            print("✅ 成功新增 full_name 欄位")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "no such table" not in str(e).lower():
                print(f"⚠️ 可能欄位已存在或錯誤: {e}")
            else:
                print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    add_column()
