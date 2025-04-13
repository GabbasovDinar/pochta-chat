from enum import Enum
from uuid import uuid4

from tortoise import fields

from .base import Base


class MessageStatus(str, Enum):
    """Enum representing the status of a message."""

    SENDING = "sending"
    SENT = "sent"
    ERROR = "error"
    READ = "read"


class Message(Base):
    """Message model representing a message in a chat."""

    uuid = fields.UUIDField(unique=True, default=uuid4)
    content = fields.TextField()
    status = fields.CharEnumField(MessageStatus, max_length=20, default=MessageStatus.SENDING)
    read_time = fields.DatetimeField(null=True)

    chat = fields.ForeignKeyField("models.Chat", related_name="messages", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField(
        "models.User", related_name="sent_messages", on_delete=fields.CASCADE
    )
