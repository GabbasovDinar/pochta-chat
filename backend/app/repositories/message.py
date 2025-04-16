from app.models import Message

from .tortoise import TortoiseRepository


class MessageRepository(TortoiseRepository):
    """Repository for Message model operations."""

    PREFETCH_FIELDS = ["user", "chat"]


message_repository = MessageRepository(model=Message)
