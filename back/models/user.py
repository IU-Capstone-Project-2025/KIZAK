from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserSkill(BaseModel):
    skill: str = Field(
        ...,
        description="Skill name",
        examples=["Python"]
    )
    skill_level: Optional[str] = Field(
        ...,
        description="Skill level. Must be 'Beginner', 'Intermediate' or 'Advanced'",
        examples=['Beginner', 'Intermediate', 'Advanced']
    )
    is_goal: bool = Field(
        ...,
        description="Is current skill is a goal one?",
        examples=[True]
    )


class UserBase(BaseModel):
    login: str
    password: str
    background: str
    education: str
    goals: str
    goal_vacancy: str
    skills: List[UserSkill]


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
    skills: Optional[List[UserSkill]] = None
