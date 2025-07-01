# back/routers/auth.py
from fastapi import APIRouter, HTTPException, status

from models.user import UserResponse, LoginRequest, UserPasssword
from db.user import get_user_from_db, get_userResp_from_db

router = APIRouter()


async def authenticate_user(login: str, password: str) -> UserPasssword:
    user = await get_user_from_db(login)
    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return user


@router.post("/login", response_model=UserResponse)
async def login(form_data: LoginRequest):
    user = authenticate_user(form_data.login, form_data.password)
    return get_userResp_from_db(form_data.login)
