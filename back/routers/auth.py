# back/routers/auth.py
from fastapi import APIRouter, HTTPException, status

from models.user import UserResponse, LoginRequest, UserPassword
from db.user import get_user_from_db

router = APIRouter()


async def authenticate_user(login: str, password: str) -> bool:
    user = await get_user_from_db(login)
    if not user or user.password != password:
        return False
    return True


@router.post("/login", response_model=UserResponse)
async def login(form_data: LoginRequest):
    if not await authenticate_user(form_data.login, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return UserResponse(login=form_data.login)
