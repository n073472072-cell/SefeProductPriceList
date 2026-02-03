# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.token import Token
from app.services import user_service
from app.security import auth, password

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends(),
    remember_me: bool = Form(False)
):
    user = user_service.get_user_by_username(db, username=form_data.username)
    if not user or not password.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="不正確的帳號或密碼",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 根據是否勾選「記住我」調整過期時間
    if remember_me:
        expires_delta = auth.timedelta(days=30)
    else:
        expires_delta = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role.value},
        expires_delta=expires_delta
    )
    return {"access_token": access_token, "token_type": "bearer"}
