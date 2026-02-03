import logging
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

try:
    # 嘗試初始化加密上下文
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # 測試一次加密，確保驅動程式活著
    pwd_context.hash("test")
    print("✅ 加密模組 (bcrypt) 初始化成功")
except Exception as e:
    print(f"🔥 加密模組初始化失敗: {e}")
    # 回退方案：如果 bcrypt 失敗，則使用內建的較弱加密(僅供診斷，不建議正式使用)
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"🔥 密碼驗證執行錯誤: {e}")
        raise e

def get_password_hash(password):
    return pwd_context.hash(password)
