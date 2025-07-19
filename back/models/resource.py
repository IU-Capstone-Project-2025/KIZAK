from datetime import date
from typing import List, Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    COURSE = "Course"
    ARTICLE = "Article"


class ResourceLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ALL = "All Levels"


class ResourceBase(BaseModel):
    resource_type: ResourceType = Field(
        ...,
        description="Type of resource (e.g. 'Course' or 'Article')",
        examples=["Course", "Article"])
    title: str = Field(
        ...,
        description="Title of resource",
        examples=["Python OOP"]
    )
    summary: str = Field(
        ...,
        description="Short summary of resource",
        examples=["Basics of OOP for Python"]
    )
    content: str = Field(
        ...,
        description="""
        URL to course (in Case of Course resource type)
        or .md content (in case of Article resource type)
        """,
        examples=["https://stepik.org/course/98974/promo?search=7287873917"]
    )
    level: ResourceLevel = Field(
        ...,
        description="Difficulty levelof resource",
        examples=["Beginner", "Intermediate", "Advanced", "All Levels"]
    )
    price: float = Field(
        ...,
        description="Price of the resource",
        examples=[0, 15.5]
    )
    language: str = Field(
        ...,
        description="Language of resource",
        examples=["Russian", "English"]
    )
    duration_hours: Optional[int] = Field(
        None,
        description="Time, needed to finish the resource",
        examples=[10, 1]
    )
    platform: str = Field(
        ...,
        description="Origin platform of a resource",
        examples=["KIZAK", "Stepik"]
    )
    rating: float = Field(
        ...,
        description="Rating of the resource",
        examples=[0, 5, 3.5]
    )
    published_date: Optional[date] = Field(
        None,
        description="Date of resource creation",
        examples=["2015-05-01"]
    )
    certificate_available: bool = Field(
        ...,
        description="True if resource provide certificate after completion",
        examples=[True, False]
    )
    skills_covered: List[str] = Field(
        ...,
        description="List of covered skills",
        examples=[["Python", "OOP"]]
    )


class ResourceResponse(ResourceBase):
    resource_id: UUID = Field(
        ...,
        description="Unique identifier for the resource",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    resource_id: UUID = Field(
        ...,
        description="Unique identifier for the resource to be updated",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    resource_type: Optional[str] = Field(
        None,
        description="Updated type of resource (e.g. 'Course' or 'Article')",
        examples=["Course", "Article"]
    )
    title: Optional[str] = Field(
        None,
        description="Updated title of resource",
        examples=["Advanced Python"]
    )
    summary: Optional[str] = Field(
        None,
        description="Updated short summary of resource",
        examples=["Covers advanced topics in Python OOP"]
    )
    content: Optional[str] = Field(
        None,
        description="""Updated URL (for courses)
        or markdown content (for articles)""",
        examples=["https://example.com/advanced-course", "# Updated content"]
    )
    level: Optional[str] = Field(
        None,
        description="Updated difficulty level of resource",
        examples=["Advanced"]
    )
    price: Optional[float] = Field(
        None,
        description="Updated price of the resource",
        examples=[25.0]
    )
    language: Optional[str] = Field(
        None,
        description="Updated language of resource",
        examples=["English"]
    )
    duration_hours: Optional[int] = Field(
        None,
        description="Updated estimated duration to complete the resource",
        examples=[5]
    )
    platform: Optional[str] = Field(
        None,
        description="Updated origin platform of a resource",
        examples=["Coursera"]
    )
    rating: Optional[float] = Field(
        None,
        description="Updated rating of the resource",
        examples=[4.7]
    )
    published_date: Optional[date] = Field(
        None,
        description="Updated date of resource publication",
        examples=["2023-09-01"]
    )
    certificate_available: Optional[bool] = Field(
        None,
        description="Updated certificate availability after completion",
        examples=[True]
    )
    skills_covered: Optional[List[str]] = Field(
        None,
        description="Updated list of skills covered by the resource",
        examples=[["Decorators", "Generators"]]
    )

class ResourceSend(BaseModel):
    resource_id: UUID
    title: str
    description: str
    skills: List[str]
