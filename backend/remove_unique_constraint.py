import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'backend', 'data', 'app.db')

def migrate():
    print(f"嘗試連接資料庫: {db_path}")
    if not os.path.exists(db_path):
        print(f"❌ 找不到資料庫檔案: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA busy_timeout = 30000") # 30 seconds timeout
        cursor = conn.cursor()
        
        # 1. 取得現有表結構 (這裡假設我們已經知道結構，但為了安全可以檢查)
        # SQLite 移除 UNIQUE 的標準做法是重建表
        
        print("正在進行資料表遷移以移除 product_code 的唯一限制...")
        
        # 關閉外鍵檢查
        cursor.execute("PRAGMA foreign_keys=OFF")
        
        # 開始交易
        cursor.execute("BEGIN TRANSACTION")
        
        # 2. 建立新表 (與舊表相同，但 product_code 沒有 UNIQUE)
        # 注意：我們移除原本欄位定義中的 UNIQUE 
        cursor.execute("""
            CREATE TABLE products_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code VARCHAR NOT NULL,
                name VARCHAR NOT NULL,
                category VARCHAR,
                specification VARCHAR,
                customer_price FLOAT NOT NULL,
                distributor_price FLOAT NOT NULL,
                price_spec VARCHAR,
                status VARCHAR,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
        """)
        
        # 3. 複製資料
        cursor.execute("""
            INSERT INTO products_new (
                id, product_code, name, category, specification, 
                customer_price, distributor_price, price_spec, 
                status, notes, created_at, updated_at
            )
            SELECT 
                id, product_code, name, category, specification, 
                customer_price, distributor_price, price_spec, 
                status, notes, created_at, updated_at
            FROM products
        """)
        
        # 4. 刪除舊表並重新命名新表
        cursor.execute("DROP TABLE products")
        cursor.execute("ALTER TABLE products_new RENAME TO products")
        
        # 5. 重新建立索引 (不含 UNIQUE)
        cursor.execute("CREATE INDEX ix_products_id ON products (id)")
        cursor.execute("CREATE INDEX ix_products_product_code ON products (product_code)")
        
        conn.commit()
        print("✅ 成功移除 product_code 的唯一限制")
        
        conn.close()
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    migrate()
