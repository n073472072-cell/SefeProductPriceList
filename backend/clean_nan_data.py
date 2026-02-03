import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'backend', 'data', 'app.db')

def clean_db():
    print(f"嘗試連接資料庫進行清理: {db_path}")
    if not os.path.exists(db_path):
        print(f"❌ 找不到資料庫檔案: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 清理字串欄位中的 'nan'
        fields = ['notes', 'specification', 'category', 'price_spec']
        for field in fields:
            cursor.execute(f"UPDATE products SET {field} = '' WHERE {field} = 'nan' OR {field} = 'None'")
            print(f"已清理 {field} 欄位中的無效字串 (影響 {cursor.rowcount} 筆)")
        
        conn.commit()
        conn.close()
        print("✅ 全域資料庫清理完成")
    except Exception as e:
        print(f"❌ 清理失敗: {e}")

if __name__ == "__main__":
    clean_db()
