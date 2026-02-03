# backend/diagnose_db.py
import os
import sys

# Ensure backend dir is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.database import SessionLocal, engine
    from app.models.user import User
    from sqlalchemy import text
    print("✅ Successfully imported database modules")
except Exception as e:
    print(f"❌ Failed to import modules: {e}")
    sys.exit(1)

def diagnose():
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Database URL: {os.getenv('DATABASE_URL')}")
    
    # Check if DB directory exists
    db_dir = "/app/backend/data"
    if os.path.exists(db_dir):
        print(f"✅ DB directory exists: {db_dir}")
        print(f"Permissions: {oct(os.stat(db_dir).st_mode)[-3:]}")
    else:
        print(f"❌ DB directory NOT found: {db_dir}")

    # Try to connect to engine
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"✅ Basic SQL execution successful: {result.fetchone()}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

    # Try to query users
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        print(f"✅ User table query successful. Total users: {user_count}")
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print(f"✅ Admin user found: {admin.username}")
        else:
            print("❌ Admin user NOT found")
    except Exception as e:
        print(f"❌ User table query failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    diagnose()
