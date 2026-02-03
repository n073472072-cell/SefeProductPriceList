# diagnose_item.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

DATABASE_URL = "sqlite:///./data/app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def diagnose(product_code):
    db = SessionLocal()
    try:
        # 查詢特定商品
        result = db.execute(text("SELECT * FROM products WHERE product_code = :code"), {"code": product_code}).fetchall()
        
        if not result:
            print(f"找不到商品編號: {product_code}")
            return

        print(f"--- 商品資料診斷: {product_code} ---")
        for row in result:
            row_dict = dict(row._mapping)
            print(json.dumps(row_dict, indent=4, ensure_ascii=False))
            
            # 檢查是否存在 'nan' 或 'None' 字串
            for k, v in row_dict.items():
                if str(v).lower() in ['nan', 'none']:
                    print(f"⚠️ 欄位 {k} 含有無效值字面量: '{v}'")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else "1202-5"
    diagnose(code)
