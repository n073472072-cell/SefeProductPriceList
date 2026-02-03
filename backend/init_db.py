# backend/init_db.py
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.security.password import get_password_hash
from app.models import * # 確保模型被加載

def init_db():
    # 建立資料表
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 檢查是否已有管理員
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("正在建立預設管理員帳號...")
            hashed_password = get_password_hash("admin123")
            new_admin = User(
                username="admin",
                hashed_password=hashed_password,
                role=UserRole.ADMIN
            )
            db.add(new_admin)
            db.commit()
            print("✅ 預設管理員帳號建立完成！")
            print("帳號: admin")
            print("密碼: admin123")
        else:
            print("⚠️ 管理員帳號已存在。")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
