# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.models.user import User
from typing import List
from app.security.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

# 只有管理員可以建立新使用者 (包含指定權限)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="此帳號已被註冊")
    return user_service.create_user(db=db, user=user)

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# 管理員取得所有使用者列表
@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return user_service.get_users(db, skip=skip, limit=limit)

# 管理員更新使用者
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    updated_user = user_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="找不到該使用者")
    return updated_user

# 管理員刪除使用者
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    # 防止刪除自己
    if current_admin.id == user_id:
         raise HTTPException(status_code=400, detail="不能刪除自己的帳號")
         
    success = user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="找不到該使用者")
