from app.models import Message

from .tortoise import TortoiseRepository


class MessageRepository(TortoiseRepository):
    """Repository for Message model operations."""

    async def get_messages_by_chat(
        self, chat_id, limit: int = 50, offset: int = 0
    ) -> list[Message]:
        """Get messages for a given chat, ordered by creation time."""
        messages = (
            await self.model.filter(chat_id=chat_id)
            .order_by("created_at")
            .offset(offset)
            .limit(limit)
            .prefetch_related("user")
        )
        return messages


message_repository = MessageRepository(model=Message)
