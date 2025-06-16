from pydantic import BaseModel

class GetUser(BaseModel):
    id: str
    login: str
    password: str
    timestamp: str
    background: str
    background_vector: list[float]
    education: str
    skills: list[str]
    skills_levels: list[str]
    goal_skills: list[str]
    goals: str
    goals_vector: list[float]
    goal_vacancy: str
    goal_vacancy_vector: list[float]

class CreateUser(BaseModel):
    login: str
    password: str
    background: str
    education: str
    skills: list[str]
    skills_levels: list[str]
    goal_skills: list[str]
    goals: str
    goal_vacancy: str
