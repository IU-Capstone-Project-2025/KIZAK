from pydantic import BaseModel
from typing import List, Optional

class CreateUser(BaseModel):
    login: str
    password: str
    background: str
    education: str
    skills: List[str]
    skills_levels: List[str]
    goal_skills: List[str]
    goals: str
    goal_vacancy: str

class UpdateUser(BaseModel):
    login: Optional[str]
    password: Optional[str]
    background: Optional[str]
    education: Optional[str]
    skills: Optional[List[str]]
    skills_levels: Optional[List[str]]
    goal_skills: Optional[List[str]]
    goals: Optional[str]
    goal_vacancy: Optional[str]

class GetUser(BaseModel):
    id: str
    login: str
    password: str
    timestamp: str
    background: str
    background_vector: List[float]
    education: str
    skills: List[str]
    skills_levels: List[str]
    goal_skills: List[str]
    goals: str
    goals_vector: List[float]
    goal_vacancy: str
    goal_vacancy_vector: List[float]
