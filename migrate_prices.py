import sqlite3
import os

db_path = 'backend/data/app.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting migration: FLOAT to TEXT for price columns...")
    
    # 1. Create a temporary table with the new schema (TEXT for prices)
    cursor.execute("""
    CREATE TABLE products_new (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        product_code VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        category VARCHAR,
        specification VARCHAR,
        customer_price VARCHAR NOT NULL DEFAULT '0',
        distributor_price VARCHAR NOT NULL DEFAULT '0',
        price_spec VARCHAR,
        status VARCHAR DEFAULT 'active',
        notes TEXT,
        price_type VARCHAR DEFAULT 'customer',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME
    )
    """)
    
    # 2. Copy data from old table to new table, converting float to string
    cursor.execute("""
    INSERT INTO products_new (
        id, product_code, name, category, specification, 
        customer_price, distributor_price, price_spec, 
        status, notes, price_type, created_at, updated_at
    )
    SELECT 
        id, product_code, name, category, specification, 
        CAST(customer_price AS TEXT), CAST(distributor_price AS TEXT), price_spec, 
        status, notes, price_type, created_at, updated_at
    FROM products
    """)
    
    # 3. Drop old table and rename new table
    cursor.execute("DROP TABLE products")
    cursor.execute("ALTER TABLE products_new RENAME TO products")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully.")
else:
    print(f"Database not found at {db_path}")
