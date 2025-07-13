from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class NodeBase(BaseModel):
    roadmap_id: UUID = Field(
        ...,
        description="Unique identifier of the roadmap this node belongs to",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    title: str = Field(
        ...,
        description="Title of the node",
        examples=["Introduction to Python"]
    )
    summary: str = Field(
        ...,
        description="Short description or summary of the node",
        examples=["Basics of Python syntax and data types"]
    )
    resource_id: UUID = Field(
        ...,
        description="Unique identifier of the associated resource",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    progress: str = Field(
        ...,
        description="Progress status of the node, e.g., percentage or step number",
        examples=['Not started', 'In progress', 'Done']
    )


class NodeResponse(NodeBase):
    node_id: UUID = Field(
        ...,
        description="Unique identifier for the node",
        examples=["123e4567-e89b-12d3-a456-426614174001"]
    )


class NodeCreate(NodeBase):
    """Schema for creating a new node. Inherits all fields from NodeBase."""
    pass


class NodeUpdate(BaseModel):
    node_id: UUID = Field(
        ...,
        description="Unique identifier of the node to update",
        examples=["123e4567-e89b-12d3-a456-426614174001"]
    )
    roadmap_id: Optional[UUID] = Field(
        None,
        description="(Optional) New roadmap ID to reassign the node",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    title: Optional[str] = Field(
        None,
        description="(Optional) New title of the node",
        examples=["Advanced Python Concepts"]
    )
    summary: Optional[str] = Field(
        None,
        description="(Optional) New summary or description of the node",
        examples=["Deep dive into decorators and generators"]
    )
    resource_id: Optional[UUID] = Field(
        None,
        description="(Optional) New resource ID to associate with this node",
        examples=["123e4567-e89b-12d3-a456-426614174002"]
    )
    progress: Optional[str] = Field(
        ...,
        description="Progress status of the node, e.g., percentage or step number",
        examples=['Not started', 'In progress', 'Done']
    )


class LinkBase(BaseModel):
    roadmap_id: UUID = Field(
        ...,
        description="Unique identifier of the roadmap for this link",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    from_node: UUID = Field(
        ...,
        description="Unique identifier of the source node",
        examples=["123e4567-e89b-12d3-a456-426614174001"]
    )
    to_node: UUID = Field(
        ...,
        description="Unique identifier of the target node",
        examples=["123e4567-e89b-12d3-a456-426614174002"]
    )


class LinkResponse(LinkBase):
    link_id: UUID = Field(
        ...,
        description="Unique identifier for the link",
        examples=["123e4567-e89b-12d3-a456-426614174003"]
    )


class LinkCreate(LinkBase):
    """Schema for creating a new link between nodes in a roadmap. Inherits from LinkBase."""
    pass


class RoadmapBase(BaseModel):
    user_id: UUID = Field(
        ...,
        description="Unique identifier of the user who owns the roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174004"]
    )


class RoadmapCreate(RoadmapBase):
    """Schema for creating a new roadmap. Inherits user_id from RoadmapBase."""
    pass


class RoadmapResponse(RoadmapBase):
    roadmap_id: UUID = Field(
        ...,
        description="Unique identifier for the created roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174005"]
    )


class RoadmapInfo(BaseModel):
    roadmap_id: UUID = Field(
        ...,
        description="Unique identifier of the roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174005"]
    )
    nodes: List[NodeResponse] = Field(
        ...,
        description="List of nodes belonging to the roadmap",
        examples=[[
            {
                "node_id": "123e4567-e89b-12d3-a456-426614174001",
                "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
                "title": "Introduction to Python",
                "summary": "Basics of Python syntax",
                "resource_id": "123e4567-e89b-12d3-a456-426614174000",
                "progress": "Done"
            }
        ]]
    )
    links: List[LinkResponse] = Field(
        ...,
        description="List of links (edges) connecting nodes in the roadmap",
        examples=[[
            {
                "link_id": "123e4567-e89b-12d3-a456-426614174003",
                "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
                "from_node": "123e4567-e89b-12d3-a456-426614174001",
                "to_node": "123e4567-e89b-12d3-a456-426614174002"
            }
        ]]
    )

class RoadmapFeedback(BaseModel):
    user_id: UUID = Field(
        ...,
        description="Unique identifier of the user to update",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    roadmap_id: UUID = Field(
        ...,
        description="Unique identifier of the roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174005"]
    )
