from fastapi.routing import APIRouter

router = APIRouter()

@router.get("/roadmap/{roadmap_id}")
async def get_roadmap(roadmap_id: str):
    return 1
