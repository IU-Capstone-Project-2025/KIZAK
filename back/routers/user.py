from typing_extensions import Annotated
from uuid import UUID
from utils.logger import logger

from db.user import create_user, remove_user, retrieve_user, update_user
from db.user import retrieve_user_profile
from fastapi import Response, status, Depends
from fastapi.routing import APIRouter
from models.user import UserCreate, UserProfileResponse, UserResponse, UserBase
from models.user import UserUpdate
from utils.security import get_current_active_user

from services.roadmap_genaretor import generate_roadmap

from utils.security import get_password_hash

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserResponse, tags=["User"])
async def get_user(user_id: UUID) -> UserResponse:
    logger.info(f"Getting user {user_id}")

    return await retrieve_user(user_id)


@router.get(
    "/users/profile/{user_id}/",
    response_model=UserProfileResponse,
    tags=["User"],
    status_code=status.HTTP_200_OK
)
async def get_user_profile(user_id: UUID) -> UserProfileResponse:
    logger.info(f"Getting user profile for {user_id}")
    return await retrieve_user_profile(user_id)


@router.post(
    "/users/",
    response_model=UserResponse,
    tags=["User"],
    status_code=status.HTTP_201_CREATED,
)
async def post_user(new_user: UserCreate, response: Response) -> UserResponse:
    new_user.password = get_password_hash(new_user.password)
    user = await create_user(new_user)
    roadmap = await generate_roadmap(
        user.user_id,
        user_role=user.goal_vacancy,
        user_skills=user.skills,
        user_query=user.goals
    )
    user.skills.sort(key=lambda skill: skill.skill)
    user.roadmap = roadmap
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
    if user.password is not None:
        user.password = get_password_hash(user.password)
    if user.skills is not None:
        user.skills.sort(key=lambda skill: skill.skill)
    
    new_user = await update_user(user)

    return new_user


@router.delete(
    "/users/{user_id}",
    tags=["User"],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(user_id: UUID) -> None:
    logger.info(f"Deleting user {user_id}")
    return await remove_user(user_id)
