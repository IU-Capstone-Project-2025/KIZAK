from pydantic import BaseModel
from typing import List
from uuid import UUID


class RoadmapData(BaseModel):
    user_id: UUID
    user_role: str
    user_skills: List[str]
    user_query: str


class RoadmapUpdateData(BaseModel):
    user_id: UUID
    nodes: List
    reason: str #will be updated to dict {node - reason}


class RoadmapResponse(BaseModel):
    nodes: List
    links: List
