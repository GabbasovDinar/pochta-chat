from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class WebSocketMessageActionEnum(str, Enum):
    """WebSocket message action enum."""

    SEND = "send"
    READ = "read"


class WebSocketMessage(BaseModel):
    """WebSocket message model."""

    action: WebSocketMessageActionEnum = Field(..., description="The action to perform.")
    chat_id: str | None = Field(None, description="The unique identifier of the chat.")
    content: str | None = Field(None, description="The content of the message.")
    message_id: UUID | None = Field(
        None, description="The unique identifier of the message template."
    )

    class Config:
        """Config for the WebSocketMessage model."""

        json_schema_extra = {
            "example": {
                "action": "send",
                "chat_id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
                "content": "Hello, world!",
                "message_id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
            }
        }
