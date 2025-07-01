from fastapi import FastAPI, HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from contextlib import asynccontextmanager

from KIZAK.back.db.db_connector import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()

app = FastAPI(lifespan=lifespan)

class LoginRequest(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    login: str

async def get_user_from_db(login: str):

    row = await db.fetchrow(
        """
        SELECT login, password
        FROM users
        WHERE login = $1
        """,
        login,
    )
    return row

async def authenticate_user(login: str, password: str) -> bool:

    user_row = await get_user_from_db(login)
    if not user_row or user_row["password"] != password:
        return False
    return True

@app.post("/login", response_model=UserResponse)
async def login(
        form_data: LoginRequest
):
    if not await authenticate_user(form_data.login, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return UserResponse(login=form_data.login)
