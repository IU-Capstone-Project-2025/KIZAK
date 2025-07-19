from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class RoadmapData(BaseModel):
    user_id: UUID
    user_role: str
    user_skills: List[str]
    user_query: str


class RoadmapUpdateData(BaseModel):
    user_id: UUID
    reasons: dict[str, str]  # node_id -> reason
    user_skills: Optional[List[str]] = None
    user_role: Optional[str] = None


class RoadmapResponse(BaseModel):
    nodes: List
    links: List
    
class ResourceSend(BaseModel):
    resource_id: UUID
    title: str
    description: str
    skills: List[str]
