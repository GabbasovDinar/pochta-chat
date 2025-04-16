from enum import Enum
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class WebSocketMessageActionEnum(str, Enum):
    """WebSocket message action enum."""

    CREATE = "create"
    READ = "read"


class WebSocketMessage(BaseModel):
    """WebSocket message model."""

    action: WebSocketMessageActionEnum = Field(..., description="The action to perform.")
    chat_id: UUID = Field(..., description="The unique identifier of the chat.")
    content: str | None = Field(None, description="The content of the message.")
    message_id: UUID | None = Field(None, description="The unique identifier of the message.")

    @model_validator(mode="after")
    def check_message_id_for_read(self) -> Self:
        action = self.action
        message_id = self.message_id
        if action == WebSocketMessageActionEnum.READ and message_id is None:
            raise ValueError("message_id is required when action equals 'read'")
        return self

    class Config:
        """Config for the WebSocketMessage model."""

        json_schema_extra = {
            "example": {
                "action": "create",
                "chat_id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
                "content": "Hello, world!",
                "message_id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
            }
        }
