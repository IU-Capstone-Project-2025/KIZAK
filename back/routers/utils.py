from fastapi.routing import APIRouter
from db.user import retrieve_user_by_login
from fastapi.exceptions import HTTPException

import requests

router = APIRouter()


@router.get("/skills_list/")
async def get_skills_list():
    return requests.get("http://ml:8001/user_skills/").json()


@router.get("/check_login/{login}")
async def check_login(login: str) -> dict:
    try:
        await retrieve_user_by_login(login)
        return {"exists": True}
    except HTTPException:
        return {"exists": False}


@router.get("/check_email/{email}")
async def check_email(email: str) -> dict:
    from db.user import retrieve_user_by_email
    try:
        await retrieve_user_by_email(email)
        return {"exists": True}
    except Exception:
        return {"exists": False}

