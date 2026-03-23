
from passlib.context import CryptContext
from FastAPI_back.configuration.config import get_app_settings
from datetime import datetime, timedelta
import jwt



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_app_settings()



def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str: 
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(
    to_encode,
    settings.secret_key.get_secret_value(),
    algorithm=settings.jwt_algorithm)
    return token



