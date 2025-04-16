from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MessageOut(BaseModel):
    """Response schema representing a chat message."""

    id: UUID = Field(..., description="The unique identifier of the message.")
    chat_id: UUID = Field(..., description="The unique identifier of the chat.")
    user_id: UUID = Field(..., description="The unique identifier of the user.")
    content: str = Field(..., description="The content of the message.")
    created_at: datetime = Field(..., description="The creation date of the message.")
    status: str = Field(..., description="The status of the message.")

    class Config:
        """Config for the MessageOut model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701788f0851",
                "chat_id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
                "user_id": "d290f1ee-6c54-4b01-90e6-d701748f0853",
                "content": "Hello, world!",
                "created_at": "2021-01-01 00:00:00",
                "status": "sent",
            }
        }
