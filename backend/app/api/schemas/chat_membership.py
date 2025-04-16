from uuid import UUID

from pydantic import BaseModel, Field


class ChatMembershipOut(BaseModel):
    """Response schema representing a chat message."""

    id: UUID = Field(..., description="The unique identifier of the message.")
    user_id: UUID = Field(..., description="The unique identifier of the user.")

    class Config:
        """Config for the MessageOut model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701788f0851",
                "user_id": "d290f1ee-6c54-4b01-90e6-d701748f0853",
            }
        }
