# migrate_db.py
import sqlite3
import os

db_path = "backend/data/app.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"資料庫不存在於: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔍 正在檢查資料表結構...")
        cursor.execute("PRAGMA table_info(products)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'price_type' not in columns:
            print("➕ 正在新增 price_type 欄位...")
            # SQLite 不支援直接新增帶有預設值的欄位並立即更新舊資料，所以分兩步
            cursor.execute("ALTER TABLE products ADD COLUMN price_type VARCHAR DEFAULT 'customer'")
            # 確保舊資料被標記為 customer
            cursor.execute("UPDATE products SET price_type = 'customer' WHERE price_type IS NULL")
            conn.commit()
            print("✅ 欄位新增成功！")
        else:
            print("ℹ️ price_type 欄位已存在，無需遷移。")
            
    except Exception as e:
        print(f"❌ 遷移發生錯誤: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
