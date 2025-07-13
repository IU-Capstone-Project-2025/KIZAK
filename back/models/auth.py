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


class PasswordResetRequestModel(BaseModel):
    mail: str = Field(
        ...,
        description="Mail address of the user",
        example=["user1@example.com", "user2@example.com"]
    )


class PasswordResetConfirmModel(BaseModel):
    new_password: str = Field(
        ...,
        description="New user password to be set",
        examples=["P@ssw0rd!"]
    )

    confirm_new_password: str = Field(
        ...,
        description="Confirmation of the new password (should match 'new_password')",
        examples=["P@ssw0rd!"]
    )
