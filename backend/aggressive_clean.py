import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'backend', 'data', 'app.db')

def aggressive_clean():
    print(f"啟動強力清理: {db_path}")
    if not os.path.exists(db_path):
        print("❌ 找不到資料庫")
        return

    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA busy_timeout = 30000")
        cursor = conn.cursor()
        
        # 定義需要檢查的文字欄位
        text_fields = ['notes', 'specification', 'category', 'price_spec']
        
        for field in text_fields:
            # 1. 清理完全等於 'nan' (不分大小寫) 的資料
            cursor.execute(f"UPDATE products SET {field} = '' WHERE LOWER(TRIM({field})) = 'nan'")
            print(f"已清理 {field} 欄位中的 'nan' (影響 {cursor.rowcount} 筆)")
            
            # 2. 清理完全等於 'none' (不分大小寫) 的資料
            cursor.execute(f"UPDATE products SET {field} = '' WHERE LOWER(TRIM({field})) = 'none'")
            print(f"已清理 {field} 欄位中的 'none' (影響 {cursor.rowcount} 筆)")
            
            # 3. 處理包含 'nan' 字串但可能帶有其他空白的特殊情況 (SQLite 特定)
            cursor.execute(f"UPDATE products SET {field} = '' WHERE {field} GLOB '*[nN][aA][nN]*' AND LENGTH({field}) <= 4")
            print(f"已清理 {field} 欄位中的模糊 'nan' (影響 {cursor.rowcount} 筆)")

        conn.commit()
        
        # 最後再跑一次查詢確認
        print("\n--- 最終驗證 ---")
        cursor.execute("SELECT COUNT(*) FROM products WHERE notes = 'nan' OR notes = 'None'")
        remaining = cursor.fetchone()[0]
        print(f"剩餘無效備註數量: {remaining}")
        
        conn.close()
        print("✅ 強力清理完成")
    except Exception as e:
        print(f"❌ 清理失敗: {e}")

if __name__ == "__main__":
    aggressive_clean()
