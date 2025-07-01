from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    login: str
