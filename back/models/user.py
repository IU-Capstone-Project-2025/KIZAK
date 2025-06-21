from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str
    background: str
    education: str
    goals: str
    goal_vacancy: str
    skills: List[str] = []
    skills_levels: List[str] = []
    goal_skills: List[str]


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: UUID
    creation_date: datetime


class UserUpdate(BaseModel):
    user_id: UUID
    login: Optional[str] = None
    password: Optional[str] = None
    background: Optional[str] = None
    education: Optional[str] = None
    goals: Optional[str] = None
    goal_vacancy: Optional[str] = None
    skills: Optional[List[str]] = None
    skills_levels: Optional[List[str]] = None
    goal_skills: Optional[List[str]] = None
