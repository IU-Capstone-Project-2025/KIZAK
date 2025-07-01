from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
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

