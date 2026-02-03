# backend/reset_admin.py
from app.database import SessionLocal
from app.models.user import User
from app.security.password import get_password_hash

def reset():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if user:
            user.hashed_password = get_password_hash("admin123")
            db.commit()
            print("✅ 管理員密碼已成功重設為: admin123")
        else:
            print("❌ 找不到 admin 帳號，請先執行 init_db.py")
    finally:
        db.close()

if __name__ == "__main__":
    reset()
