from fastapi.routing import APIRouter
from fastapi import HTTPException

router = APIRouter()

@router.get("/roadmap/{roadmap_id}")
async def get_roadmap(roadmap_id: str):
    return HTTPException(status_code=501, detail="In progress")
