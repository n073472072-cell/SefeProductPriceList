# backend/app/schemas/user.py
from pydantic import BaseModel
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class UserUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None
    password: str | None = None
    role: UserRole | None = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    class Config:
        from_attributes = True
