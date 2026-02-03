# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "7b0c8d1e2f3g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x1y2z3a4b5c6d7e8f9")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 480))
    DATABASE_URL: str = os.getenv("DATABASE_URL") or (
        "sqlite:////app/backend/data/app.db" if os.path.exists("/app") 
        else "sqlite:///./data/app.db"
    )

settings = Settings()
