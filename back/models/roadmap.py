from pydantic import BaseModel
from typing import List

class RoadmapNode(BaseModel):
    pass

class RoadmapLink(BaseModel):
    pass

class Roadmap(BaseModel):
    nodes: List[RoadmapNode]
    links: List[RoadmapLink]

class CreateNode(BaseModel):
    pass
