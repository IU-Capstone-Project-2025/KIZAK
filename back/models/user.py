from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserSkill(BaseModel):
    """Schema for a user's individual skill entry."""
    skill: str = Field(
        ...,
        description="Name of the skill",
        examples=["Python", "Data Analysis"]
    )
    skill_level: Optional[str] = Field(
        None,
        description="Proficiency level of the skill",
        examples=["Beginner", "Intermediate", "Advanced"]
    )
    is_goal: bool = Field(
        ...,
        description="Indicates if this skill is a target goal for the user",
        examples=[True, False]
    )


class UserPasssword(BaseModel):
    login: str = Field(
        ...,
        description="Login identifier for the user",
        examples=["johndoe", "user123"]
    )
    password: str = Field(
        ...,
        description="User password (hashed or plain depending on security policy)",
        examples=["P@ssw0rd!"]
    )


class UserBase(BaseModel):
    """Base schema for user data shared between create and response operations."""
    login: str = Field(
        ...,
        description="Unique login identifier for the user",
        examples=["johndoe", "user123"]
    )
    password: str = Field(
        ...,
        description="User password (hashed or plain depending on security policy)",
        examples=["P@ssw0rd!"],
    )
    background: str = Field(
        ...,
        description="Background information about the user",
        examples=["5 years experience in software development"]
    )
    education: str = Field(
        ...,
        description="Education details of the user",
        examples=["Bachelor's in Computer Science"]
    )
    goals: str = Field(
        ...,
        description="User's professional or career goals",
        examples=["Become a senior data engineer"]
    )
    goal_vacancy: str = Field(
        ...,
        description="Desired job vacancy or role the user aims for",
        examples=["Data Engineer"]
    )
    skills: List[UserSkill] = Field(
        ...,
        description="List of user's skills with levels and goal flags",
        examples=[
            [
                {"skill": "Python", "skill_level": "Intermediate", "is_goal": False},
                {"skill": "Machine Learning", "skill_level": "Beginner", "is_goal": True}
            ]
        ]
    )


class UserCreate(UserBase):
    """Schema for creating a new user. Inherits all fields from UserBase."""
    pass


class UserResponse(UserBase):
    """Schema for user data returned in responses, includes system-generated fields."""
    user_id: UUID = Field(
        ...,
        description="Unique identifier for the user",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    creation_date: datetime = Field(
        ...,
        description="Timestamp when the user was created",
        examples=["2025-06-24T15:30:00Z"]
    )


class UserUpdate(BaseModel):
    """Schema for updating existing user data; all fields optional except user_id."""
    user_id: UUID = Field(
        ...,
        description="Unique identifier of the user to update",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    login: Optional[str] = Field(
        None,
        description="(Optional) New login for the user",
        examples=["newusername"]
    )
    password: Optional[str] = Field(
        None,
        description="(Optional) Updated password (hashed or plain depending on policy)",
        examples=["N3wP@ssw0rd"]
    )
    background: Optional[str] = Field(
        None,
        description="(Optional) Updated background information",
        examples=["6 years experience in backend development"]
    )
    education: Optional[str] = Field(
        None,
        description="(Optional) Updated education details",
        examples=["Master's in Data Science"]
    )
    goals: Optional[str] = Field(
        None,
        description="(Optional) Updated career goals",
        examples=["Lead a data engineering team"]
    )
    goal_vacancy: Optional[str] = Field(
        None,
        description="(Optional) Updated desired vacancy or role",
        examples=["Senior Data Engineer"]
    )
    skills: Optional[List[UserSkill]] = Field(
        None,
        description="(Optional) Updated list of user's skills; replaces existing skills if provided",
        examples=[
            [
                {"skill": "Go", "skill_level": "Beginner", "is_goal": True},
                {"skill": "Docker", "skill_level": "Intermediate", "is_goal": False}
            ]
        ]
    )
