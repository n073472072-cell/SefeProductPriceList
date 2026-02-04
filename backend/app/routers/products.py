# backend/app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service
from app.security.dependencies import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ProductResponse], dependencies=[Depends(get_current_user)])
def read_products(
    skip: int = 0, 
    limit: int = 5000, 
    price_type: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    """取得產品列表 (支援分頁與類型過濾)"""
    return product_service.get_products(db, skip, limit, price_type)

@router.post("/", response_model=ProductResponse, dependencies=[Depends(get_current_admin_user)])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """新增單項產品 (僅限管理員)"""
    return product_service.create_product(db, product)

@router.post("/upload", dependencies=[Depends(get_current_admin_user)])
async def upload_products_excel(
    db: Session = Depends(get_db), 
    file: UploadFile = File(...),
    import_mode: str = Query("all")
):
    """透過 Excel 批次上傳產品 (僅限管理員)"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="檔案格式錯誤，請上傳 .xlsx 或 .xls 檔")
    contents = await file.read()
    # 加入偵偵日誌
    print(f"[DEBUG] 接收到匯入請求: filename={file.filename}, mode={import_mode}")
    result = product_service.create_products_from_excel(db, contents, import_mode)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/export", dependencies=[Depends(get_current_user)])
def export_products_excel(mode: str = Query("all"), db: Session = Depends(get_db)):
    """匯出產品資料為 Excel (支援經銷/客戶模式)"""
    excel_data = product_service.export_products_to_excel(db, mode)
    return StreamingResponse(
        iter([excel_data]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=products_export_{mode}.xlsx"}
    )

@router.get("/template", dependencies=[Depends(get_current_user)])
def download_product_template(type: str = Query('all')):
    """下載產品匯入範本 (Excel)
       type: 'customer' | 'distributor' | 'all'
    """
    excel_data = product_service.create_product_template(type)
    filename = f"product_template_{type}.xlsx"
    
    return StreamingResponse(
        iter([excel_data]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.delete("/clear-all", dependencies=[Depends(get_current_admin_user)])
def delete_all_products(mode: str = Query("all"), db: Session = Depends(get_db)):
    """清除產品資料 (支援按模式歸零)"""
    count = product_service.clear_all_products(db, mode)
    return {"message": f"成功重置 {count} 筆產品區域資料 (模式: {mode})"}

@router.put("/{product_id:int}", response_model=ProductResponse, dependencies=[Depends(get_current_admin_user)])
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """修改產品資訊 (僅限管理員)"""
    db_product = product_service.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="產品不存在")
    return db_product

@router.delete("/{product_id:int}", dependencies=[Depends(get_current_admin_user)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """刪除單項產品 (僅限管理員)"""
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="產品不存在")
    return {"message": "產品已刪除"}
