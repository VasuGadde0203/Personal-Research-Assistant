from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models.user import UserRegister, UserLogin
from databases.mongodb import get_user_by_email, insert_user
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user: UserRegister) -> str:
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    hashed_password = pwd_context.hash(user.password)
    user_dict = {
        "user_id": user_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    insert_user(user_dict)
    token = create_access_token({"sub": user.email, "user_id": user_id})
    return token

def authenticate_user(user: UserLogin) -> str:
    db_user = get_user_by_email(user.email)
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email, "user_id": db_user["user_id"]})
    return token, db_user["user_id"]

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_email(email)
        if user is None or user["user_id"] != user_id:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")