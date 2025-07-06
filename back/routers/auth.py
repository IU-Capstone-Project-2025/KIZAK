# back/routers/auth.py
from fastapi import APIRouter, HTTPException, status, Body, Response
from typing import Dict

from models.user import UserResponse, LoginRequest, UserPassword, UserCreate
from models import user as user_model
from db.user import get_user_from_db, get_userResp_from_db, create_user, \
    retrieve_user_by_login
from utils.logger import logger

router = APIRouter()


@router.post('/login', response_model=Dict, tags=["User"],
             status_code=status.HTTP_200_OK)
async def login(
        payload: UserPassword = Body(),
):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - login: Unique identifier for a user

    - password:
    """
    try:
        user = await retrieve_user_by_login(payload.login)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    return user.generate_token()


@router.post('/signup', response_model=UserResponse, tags=["User"],
             status_code=status.HTTP_201_CREATED)
async def signup(
        payload: UserCreate,
        response: Response
) -> UserResponse:
    """Processes request to register user account."""
    payload.password = user_model.UserBase.hash_password(payload.password)
    user = await create_user(payload)
    logger.info(f"Created user {user.user_id}")
    response.headers["Location"] = f"/users/{user.user_id}"
    return user
