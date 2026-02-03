# diagnose_db.py
import sqlite3
import os

db_path = "backend/data/app.db"

def check_item(code):
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM products WHERE product_code = ?", (code,))
        rows = cursor.fetchall()
        
        if not rows:
            print(f"No item found with product_code: {code}")
            return
            
        print(f"Results for {code}:")
        for row in rows:
            print(dict(row))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else "1202-5"
    check_item(code)
