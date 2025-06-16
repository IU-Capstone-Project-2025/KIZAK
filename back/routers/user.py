from fastapi.routing import APIRouter

from models.user import GetUser, CreateUser

router = APIRouter()

@router.get("/user/{user_id}", response_model=GetUser)
async def get_user(user_id: str) -> GetUser:
    return 1

@router.post("/user/", response_model=GetUser)
async def create_user(new_user: CreateUser) -> GetUser:
    return 1

@router.put("/user/", response_model=GetUser)
async def update_user(new_user: CreateUser) -> GetUser:
    return 1

@router.delete("/user/{user_id}")
async def delete_user(user_id: str) -> str:
    return 1
