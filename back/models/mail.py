from pydantic import BaseModel, Field
from typing import List, Optional


class EmailModel(BaseModel):
    addresses: List[str] = Field(
        ...,
        description="The list of email addresses",
        example=["user1@example.com", "user2@example.com"]
    )
