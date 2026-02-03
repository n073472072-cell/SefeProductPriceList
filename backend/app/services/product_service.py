# backend/app/services/product_service.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from io import BytesIO
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session, skip: int = 0, limit: int = 100, price_type: str = None) -> List[Product]:
    query = db.query(Product)
    if price_type:
        query = query.filter(Product.price_type == price_type)
    return query.order_by(Product.updated_at.desc()).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        **product.model_dump(),
        updated_at=datetime.now()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db_product.updated_at = datetime.now()
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True

def create_products_from_excel(db: Session, file_content: bytes, import_mode: str = 'all') -> Dict:
    """
    import_mode: 'customer', 'distributor', 'all'
    """
    import_mode = import_mode.lower() if import_mode else 'customer'
    if import_mode == 'all':
        import_mode = 'customer'
        
    try:
        df = pd.read_excel(BytesIO(file_content))
        # 移除標題空格
        df.columns = [str(c).strip() for c in df.columns]
        
        # 建立欄位映射
        column_map = {
            '商品編號': 'product_code', '產品編號': 'product_code', '編號': 'product_code', '代號': 'product_code',
            '商品名稱': 'name', '產品名稱': 'name', '名稱': 'name',
            '商品分類': 'category', '產品分類': 'category', '分類': 'category',
            '規格': 'specification', '產品規格': 'specification',
            '售價 (未稅)': 'customer_price', '客戶售價(未稅)': 'customer_price', 
            '產品客戶售價(未稅)': 'customer_price', '售價(未稅)': 'customer_price',
            '經銷進價': 'distributor_price', '經銷售價': 'distributor_price', '經銷價': 'distributor_price', '經銷價格': 'distributor_price',
            '售價規格': 'price_spec', '更新日期': 'updated_at_excel',
            '狀態': 'status', '備註': 'notes'
        }
        
        found_fields = {}
        for excel_col in df.columns:
            if excel_col in column_map:
                found_fields[excel_col] = column_map[excel_col]
        
        current_time = datetime.now()
        
        count = 0
        for index, row in df.iterrows():
            p_data = {}
            for excel_col, model_field in found_fields.items():
                val = row[excel_col]
                if pd.isna(val) or str(val).lower() in ['nan', 'none', 'null', 'nan.0']:
                    val = ''
                p_data[model_field] = str(val).strip()

            p_code = p_data.get('product_code', '')
            p_name = p_data.get('name', '')
            if not p_name: continue 

            # 【使用者要求】售價直接存為字串，不做 float 轉換
            final_status_str = p_data.get('status', '上架')
            if not final_status_str: final_status_str = '上架'

            existing = db.query(Product).filter(
                Product.product_code == p_code,
                Product.name == p_name,
                Product.price_type == import_mode
            ).first()

            if existing:
                for field, value in p_data.items():
                    if field != 'status':
                        setattr(existing, field, value)
                
                existing.status = final_status_str
                existing.price_type = import_mode
                existing.updated_at = current_time
            else:
                new_item = Product(
                    product_code=p_code,
                    name=p_name,
                    category=p_data.get('category', ''),
                    specification=p_data.get('specification', ''),
                    customer_price=p_data.get('customer_price', '0'),
                    distributor_price=p_data.get('distributor_price', '0'),
                    price_spec=p_data.get('price_spec', ''),
                    status=final_status_str,
                    notes=p_data.get('notes', ''),
                    price_type=import_mode,
                    updated_at=current_time
                )
                db.add(new_item)
            count += 1
        
        db.commit()
        return {"success": True, "message": f"成功處理 {count} 筆資料 (模式: {import_mode})"}
    except Exception as e:
        db.rollback()
        import traceback
        print(traceback.format_exc())
        return {"success": False, "message": f"處理失敗: {str(e)}"}

def clear_all_products(db: Session, mode: str = 'all') -> int:
    if mode == 'all':
        count = db.query(Product).delete()
    else:
        count = db.query(Product).filter(Product.price_type == mode).delete()
    db.commit()
    return count

def export_products_to_excel(db: Session, mode: str = 'all') -> bytes:
    query = db.query(Product)
    if mode != 'all':
        query = query.filter(Product.price_type == mode)
    
    products = query.all()
    if not products: return b""
    
    data = []
    for p in products:
        # 格式化日期為 YYYY/MM/DD
        updated_at_str = p.updated_at.strftime("%Y/%m/%d") if p.updated_at else ""
        
        # 格式化狀態為中文
        status_zh = "上架" if p.status in ["active", "上架"] else "下架"
        
        row = {
            '商品編號': p.product_code,
            '產品名稱': p.name,
            '商品分類': p.category,
            '規格': p.specification,
            '售價規格': p.price_spec,
            '更新日期': updated_at_str,
            '狀態': status_zh,
            '備註': p.notes
        }
        
        # 根據模式決定價格欄位名稱
        if mode == 'distributor':
            row['經銷售價'] = p.distributor_price
        elif mode == 'customer':
            row['售價 (未稅)'] = p.customer_price
        else:
            # 'all' 模式下包含兩種價格
            row['售價 (未稅)'] = p.customer_price
            row['經銷進價'] = p.distributor_price
            
        data.append(row)
    
    # 重新整理欄位順序以符合範本/頁面顯示
    base_cols = ['商品編號', '產品名稱', '商品分類', '規格']
    if mode == 'distributor':
        final_cols = base_cols + ['經銷售價', '售價規格', '更新日期', '狀態', '備註']
    elif mode == 'customer':
        final_cols = base_cols + ['售價 (未稅)', '售價規格', '更新日期', '狀態', '備註']
    else:
        final_cols = base_cols + ['售價 (未稅)', '經銷進價', '售價規格', '更新日期', '狀態', '備註']

    df = pd.DataFrame(data, columns=final_cols)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='產品資料')
    return output.getvalue()

def create_product_template(template_type: str = 'all') -> bytes:
    base_columns = ['商品編號', '產品名稱', '商品分類', '規格']
    if template_type == 'distributor':
        columns = base_columns + ['經銷售價', '售價規格', '更新日期', '狀態', '備註']
    elif template_type == 'customer':
        columns = base_columns + ['售價 (未稅)', '售價規格', '更新日期', '狀態', '備註']
    else:
        columns = base_columns + ['售價 (未稅)', '經銷進價', '售價規格', '更新日期', '狀態', '備註']

    df = pd.DataFrame(columns=columns)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='範本')
    return output.getvalue()
