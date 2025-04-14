from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .user import UserOut


class ChatActionResponse(BaseModel):
    """Response schema for chat join/leave actions."""

    msg: str
    result: bool

    class Config:
        """Config for the ChatActionResponse model."""

        json_schema_extra = {
            "example": {
                "msg": "Successfully joined the chat",
                "result": True,
            }
        }


class ChatActionRequest(BaseModel):
    """Input schema for chat join/leave actions."""

    chat_id: UUID = Field(..., description="The unique identifier of the chat.")

    class Config:
        """Config for the ChatActionRequest model."""

        json_schema_extra = {
            "example": {
                "chat_id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
            }
        }


class MessageOut(BaseModel):
    """Response schema representing a chat message."""

    id: str
    chat_id: str
    user_id: str
    content: str
    created_at: datetime
    status: str

    class Config:
        """Config for the MessageOut model."""

        orm_mode = True
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


class ChatHistoryResponse(BaseModel):
    """Response schema for chat message history."""

    msg: str
    result: list[MessageOut]


class ChatMembersResponse(BaseModel):
    """Response schema for retrieving chat members."""

    msg: str
    result: list[UserOut]
