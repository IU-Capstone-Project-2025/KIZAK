from pydantic import BaseModel
from typing import List


class RoadmapData(BaseModel):
    user_role: str
    user_skills: List[str]
    user_query: str


class RoadmapUpdateData(BaseModel):
    pass


class RoadmapResponse(BaseModel):
    nodes: List
    links: List
