from pydantic import BaseModel
from typing import List
from uuid import UUID

class RoadmapNode(BaseModel):
    id: UUID
    roadmap_id: UUID
    title: str
    summary: str
    resource_id: UUID
    progress: int

class RoadmapLink(BaseModel):
    id: UUID
    roadmap_id: UUID
    from_node: UUID
    to_node: UUID

class Roadmap(BaseModel):
    id: UUID
    nodes: List[RoadmapNode]
    links: List[RoadmapLink]
