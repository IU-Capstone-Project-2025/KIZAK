from fastapi.routing import APIRouter
from fastapi import HTTPException
from models.user import GetUser, CreateUser, UpdateUser

router = APIRouter()

@router.get("/user/{user_id}", response_model=GetUser, summary="Get a user")
async def get_user(user_id: str) -> GetUser:
    return HTTPException(status_code=501, detail="In progress")

@router.post("/user/", response_model=GetUser, summary="Create user")
async def create_user(new_user: CreateUser) -> GetUser:
    return HTTPException(status_code=501, detail="In progress")

@router.put("/user/", response_model=UpdateUser, summary="Update user")
async def update_user(new_user: CreateUser) -> GetUser:
    return HTTPException(status_code=501, detail="In progress")

@router.delete("/user/{user_id}", summary="Delete user")
async def delete_user(user_id: str) -> str:
    return HTTPException(status_code=501, detail="In progress")
