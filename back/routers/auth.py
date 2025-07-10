# back/routers/auth.py
from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter, HTTPException, status, Body, Response
from typing import Dict, Optional

from models.user import UserResponse, LoginRequest, UserPassword, UserCreate
from models import user as user_model
from utils.logger import logger
from db.user import create_user, retrieve_user_by_login

from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from uuid import UUID

from fastapi import Response, status, Depends
from fastapi.routing import APIRouter
from models.token import Token
from utils.security import oauth2_scheme, get_password_hash, verify_password

import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()


def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def authenticate_user(login: str, password: str):
    user = await retrieve_user_by_login(login)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


@router.post('/login', response_model=Token, tags=["User"],
             status_code=status.HTTP_200_OK)
async def log_in(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {
        "token": Token(access_token=access_token, token_type="bearer"),
        "user_id": user.user_id
    }


@router.post('/signup', response_model=UserResponse, tags=["User"],
             status_code=status.HTTP_201_CREATED)
async def signup(
        payload: UserCreate,
        response: Response
) -> UserResponse:
    """Processes request to register user account."""
    payload.password = get_password_hash(payload.password)
    user = await create_user(payload)
    logger.info(f"Created user {user.user_id}")
    response.headers["Location"] = f"/users/{user.user_id}"
    return user
