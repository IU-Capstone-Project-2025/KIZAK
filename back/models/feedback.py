from pydantic import BaseModel, Field
from typing import Optional

from uuid import UUID

class FeedbackBase(BaseModel):
    user_id: UUID = Field(
        ...,
        description="Unique identifier of the user who owns the roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174004"]
    )
    roadmap_id: UUID = Field(
        ...,
        description="Unique identifier for the roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    node_id: UUID = Field(
        ...,
        description="Unique identifier for the node",
        examples=["123e4567-e89b-12d3-a456-426614174001"]
    )
    resource_id: UUID = Field(
        ...,
        description="Unique identifier of the associated resource",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    is_liked: bool = Field(
        ...,
        description="Does usel likes this recommendation",
        examples=[True]
    )
    reason: Optional[str] = Field(
        ...,
        description="Recomandation feedback",
        examples=[
            "Why do I have Java in my Python roadmap?"
        ]
    )

class FeedbackResponse(FeedbackBase):
    pass

class FeedbackCreate(FeedbackBase):
    pass
