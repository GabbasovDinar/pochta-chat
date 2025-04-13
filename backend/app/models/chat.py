# ruff: noqa: F821

from enum import Enum

from tortoise import fields

from .base import Base


class ChatType(str, Enum):
    """Enum representing the type of chat."""

    GROUP = "group"
    PRIVATE = "private"


class Chat(Base):
    """Chat channel (either private or group chat)."""

    name = fields.CharField(max_length=255, null=True)
    chat_type = fields.CharEnumField(ChatType, default=ChatType.GROUP)

    messages: fields.ReverseRelation["Message"]
    memberships: fields.ReverseRelation["ChatMembership"]
