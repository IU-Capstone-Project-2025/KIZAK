from uuid import UUID
from utils.logger import logger

from db.user import create_user, remove_user, retrieve_user, update_user
from fastapi import Response, status
from fastapi.routing import APIRouter
from models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()





@router.get("/users/{user_id}", response_model=UserResponse, tags=["User"])
async def get_user(user_id: UUID) -> UserResponse:
    logger.info(f"Getting user {user_id}")
    return await retrieve_user(user_id)


@router.post(
    "/users/",
    response_model=UserResponse,
    tags=["User"],
    status_code=status.HTTP_201_CREATED,
)
async def post_user(new_user: UserCreate, response: Response) -> UserResponse:
    user = await create_user(new_user)
    logger.info(f"Created user {user.user_id}")
    response.headers["Location"] = f"/users/{user.user_id}"
    return user


@router.put(
    "/users/",
    response_model=UserResponse,
    tags=["User"]
)
async def put_user(user: UserUpdate) -> UserResponse:
    logger.info(f"Putting user {user.user_id}")
    return await update_user(user)


@router.delete(
    "/users/{user_id}",
    tags=["User"],
    status_code=status.
    HTTP_204_NO_CONTENT
)
async def delete_user(user_id: UUID) -> None:
    logger.info(f"Deleting user {user_id}")
    return await remove_user(user_id)
