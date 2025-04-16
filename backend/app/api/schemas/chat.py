from uuid import UUID

from pydantic import BaseModel, Field

from app.models.chat import ChatType

from .chat_membership import ChatMembershipOut
from .message import MessageOut


class CreateChatRequest(BaseModel):
    """Input schema for creating a private chat."""

    chat_type: ChatType = Field(..., description="The type of the chat.")
    user_ids: list[UUID] = Field(..., description="The unique identifiers of the users.")
    name: str = Field(None, description="The name of the chat.")

    class Config:
        """Config for the CreatePrivateChatIn model."""

        json_schema_extra = {
            "example": {
                "chat_type": "group",
                "user_ids": [
                    "d290f1ee-6c54-4b01-90e6-d701748f0852",
                    "d290f1ee-6c54-4b01-90e6-d701748f0855",
                ],
                "name": "Group chat",
            }
        }


class ChatResponse(BaseModel):
    """Response schema for retrieving chat list."""

    id: UUID = Field(..., description="The unique identifier of the chat.")
    name: str = Field(..., description="The name of the chat.")
    chat_type: ChatType = Field(..., description="The type of the chat.")
    memberships: list[ChatMembershipOut] = Field(..., description="The memberships of the chat.")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e8-d701748f0852",
                "name": "Private chat with John",
                "chat_type": "private",
                "memberships": [
                    {
                        "id": "623b45e9-df9f-4b01-90a8-e1c7cf123456",
                        "user_id": "d290f1ee-6c54-4b01-90e8-d701748f0852",
                    }
                ],
            }
        }


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


class ChatHistoryResponse(BaseModel):
    """Response schema for chat message history."""

    msg: str
    result: list[MessageOut]
