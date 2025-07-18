# back/routers/auth.py
from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter, HTTPException, status, Body, Response
from fastapi.responses import JSONResponse
from typing import Dict, Optional

from models.user import UserResponse, LoginRequest, UserPassword, UserCreate, \
    UserUpdate
from models import user as user_model
from utils.logger import logger
from db.user import create_user, retrieve_user_by_login, update_user

from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from uuid import UUID

from fastapi import Response, status, Depends
from fastapi.routing import APIRouter
from models.token import Token
from utils.security import oauth2_scheme, get_password_hash, verify_password, \
    create_url_safe_token, decode_url_safe_token

from models.auth import PasswordResetRequestModel, PasswordResetConfirmModel

import os

from config import Config

from mail.mail import mail, create_message

from db.user import retrieve_user_by_email

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


@router.post('/token', tags=["User"],
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


@router.post('/signup/', response_model=UserResponse, tags=["User"],
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

    token = create_url_safe_token({"mail": payload.mail})

    link = f"http://{Config.DOMAIN}/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[payload.mail],
        subject="Verify your Email",
        body=html_message
    )

    await mail.send_message(message)

    return user


@router.get("/verify/{token}", tags=["User"])
async def verify_user_account(token: str):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('mail')
    if user_email:
        user = await retrieve_user_by_email(user_email)

        logger.info(f"user_info: {user}")

        updated_user = UserUpdate(
            user_id=user.user_id,
            is_verified=True
        )

        await update_user(updated_user)

        return JSONResponse(content={
            "message": "Account verified successfully"
        }, status_code=status.HTTP_200_OK)

    return JSONResponse(content={
        "message": "Error occurred during verification"
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/password-reset-request", tags=["User"])
async def password_reset_request(mail_data: PasswordResetRequestModel):
    token = create_url_safe_token({"mail": mail_data.mail})

    # Use frontend domain for the reset link
    frontend_domain = "http://localhost:3000"  # Change to your actual frontend domain in production
    link = f"{frontend_domain}/password-reset-confirm/{token}"

    html_message = f"""
        <h1>Reset Your Password</h1>
        <p>Please click this <a href=\"{link}\">link</a> to Reset Your Password</p>
        """

    message = create_message(
        recipients=[mail_data.mail],
        subject="Reset your Password",
        body=html_message
    )

    await mail.send_message(message)

    return JSONResponse(content={
        "message": "Password reset request sent to email",
    }, status_code=status.HTTP_200_OK)


@router.post("/password-reset-confirm/{token}", tags=["User"])
async def reset_account_password(token: str,
                                 passwords: PasswordResetConfirmModel):
    if passwords.new_password != passwords.confirm_new_password:
        raise HTTPException(detail = "Passwords do not match",
                            status_code=status.HTTP_400_BAD_REQUEST)

    token_data = decode_url_safe_token(token)

    user_email = token_data.get('mail')
    if user_email:
        user = await retrieve_user_by_email(user_email)

        logger.info(f"user_info: {user}")

        updated_user = UserUpdate(
            user_id=user.user_id,
            password=get_password_hash(passwords.new_password)
        )

        await update_user(updated_user)

        return JSONResponse(content={
            "message": "Password reset successfully"
        }, status_code=status.HTTP_200_OK)

    return JSONResponse(content={
        "message": "Error occurred during password reset"
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
