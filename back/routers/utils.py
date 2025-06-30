from fastapi.routing import APIRouter
from utils.conf import USER_SKILLS

router = APIRouter()


@router.get("/skills_list/")
async def get_skills_list() -> set[str]:
    return USER_SKILLS
