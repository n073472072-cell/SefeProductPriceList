# backend/app/models/product.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class ProductStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    specification = Column(String)
    customer_price = Column(String, nullable=False, default="0")
    distributor_price = Column(String, nullable=False, default="0")
    price_spec = Column(String)
    status = Column(String, default="active")
    notes = Column(Text)
    price_type = Column(String, default="customer") # "customer" or "distributor"
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
