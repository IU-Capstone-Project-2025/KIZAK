from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

from uuid import UUID


class FeedbackStrings(str, Enum):
    TOO_EASY = "too_easy"
    WRONG_SKILLS = "wrong_skills"
    TOO_HARD = "too_hard"
    BAD_AUTHOR = "bad_author"
    UNAVAILABLE = "unavailable"


class FeedbackBase(BaseModel):
    user_id: UUID = Field(
        ...,
        description="Unique identifier of the user who owns the roadmap",
        examples=["123e4567-e89b-12d3-a456-426614174004"]
    )
    node_id: UUID = Field(
        ...,
        description="Unique identifier for the node",
        examples=["123e4567-e89b-12d3-a456-426614174001"]
    )
    reason: FeedbackStrings = Field(
        ...,
        description="Reason for feedback",
        examples=[
            "too_easy",
            "wrong_skills",
            "too_hard",
            "bad_author",
            "unavailable"
        ]
    )


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    pass
