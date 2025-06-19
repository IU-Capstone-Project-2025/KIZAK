from datetime import date
from typing import List, Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    COURSE = "Course"
    ARTICLE = "Article"


class ResourceBase(BaseModel):
    resource_type: ResourceType = Field(
        ...,
        description="Type of resource (e.g. 'Course' or 'Article')",
        example="Course")
    title: str
    summary: str
    content: str
    level: str
    price: float
    language: str
    duration_hours: int
    platform: str
    rating: float
    published_date: date
    certificate_available: bool
    skills_covered: List[str]


class ResourceResponse(ResourceBase):
    resource_id: UUID
    summary_vector: Optional[List[float]] = None
    skills_covered_vector: Optional[List[List[float]]] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    resource_id: UUID
    resource_type: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    level: Optional[str] = None
    price: Optional[float] = None
    language: Optional[str] = None
    duration_hours: Optional[int] = None
    platform: Optional[str] = None
    rating: Optional[float] = None
    published_date: Optional[date] = None
    certificate_available: Optional[bool] = None
    skills_covered: Optional[List[str]] = None
