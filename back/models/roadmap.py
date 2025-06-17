from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class NodeBase(BaseModel):
    roadmap_id: UUID
    title: str
    summary: str
    resource_id: UUID
    progress: int

class NodeResponse(NodeBase):
    id: UUID

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    id: UUID
    roadmap_id: Optional[UUID]
    title: Optional[str]
    summary: Optional[str]
    resource_id: Optional[UUID]
    progress: Optional[int]

class LinkBase(BaseModel):
    roadmap_id: UUID
    from_node: UUID
    to_node: UUID

class LinkResponse(LinkBase):
    id: UUID

class LinkCreate(LinkBase):
    pass

class RoadmapBase(BaseModel):
    user_id: UUID

class RoadmapCreate(RoadmapBase):
    pass

class RoadmapResponse(RoadmapBase):
    roadmap_id: UUID
    nodes: List[NodeResponse]
    links: List[NodeResponse]
