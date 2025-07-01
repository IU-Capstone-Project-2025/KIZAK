from fastapi.routing import APIRouter
from utils.conf import USER_SKILLS
from db.user import retrieve_user_by_login
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.get("/skills_list/")
async def get_skills_list() -> set[str]:
    return USER_SKILLS


@router.get("/check_login/{login}")
async def check_login(login: str) -> bool:
    try:
        await retrieve_user_by_login(login)
        return True
    except HTTPException:
        return False
