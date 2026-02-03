# backend/app/schemas/product.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from datetime import datetime
from app.models.product import ProductStatus

class ProductBase(BaseModel):
    product_code: str
    name: str
    category: Optional[str] = None
    specification: Optional[str] = None
    # 允許字串以支援如 "$250-$300" 的自定義內容
    customer_price: str = "0"
    distributor_price: str = "0"
    price_spec: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None
    price_type: str = "customer"

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v):
        if not v:
            return "active"
        s = str(v).lower()
        if 'active' in s or '上架' in s or '正常' in s:
            return "active"
        if 'inactive' in s or '下架' in s or '停' in s:
            return "inactive"
        return str(v)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    specification: Optional[str] = None
    customer_price: Optional[str] = None
    distributor_price: Optional[str] = None
    price_spec: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    price_type: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
