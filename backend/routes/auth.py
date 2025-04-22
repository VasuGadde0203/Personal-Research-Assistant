from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models.user import UserRegister, UserLogin, Token
from services.auth import create_user, authenticate_user, create_access_token
from typing import Annotated

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register")
def register_user(user: UserRegister) -> dict:
    base_respone = {
        "success": False,
        "status_code": 400,
        "message": "Failed to register user",
        "data": None
    }
    try:
        token = create_user(user)
        base_respone["success"] = True
        base_respone["status_code"] = 200
        base_respone["message"] = "User registered succesfully"
        base_respone["data"] = {"email": user.email, "token": token}
        return base_respone
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(user: UserLogin) -> dict:
    base_respone = {
        "success": False,
        "status_code": 400,
        "message": "Failed to register user",
        "data": None
    }
    try:
        token, user_id = authenticate_user(user)
        
        base_respone["success"] = True
        base_respone["status_code"] = 200
        base_respone["message"] = "User authenticated succesfully"
        base_respone["data"] = {"email": user.email, "access_token": token, "user_id": user_id}
        return base_respone
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))