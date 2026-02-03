import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'backend', 'data', 'app.db')

def add_column():
    print(f"嘗試連接資料庫: {db_path}")
    if not os.path.exists(db_path):
        print(f"❌ 找不到資料庫檔案: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 檢查欄位是否已存在
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'full_name' not in columns:
            print("正在新增 full_name 欄位...")
            cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
            conn.commit()
            print("✅ 成功新增 full_name 欄位")
        else:
            print("ℹ️ full_name 欄位已存在")
            
        conn.close()
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    add_column()
