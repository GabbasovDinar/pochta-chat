from .base import Base


class ChatMembershipService(Base):
    """Service for ChatMembership model operations."""

    async def leave(self, chat_id: str, user_id: str) -> bool:
        """Leave a chat."""
        membership = await self.search({"user_id": user_id, "chat_id": chat_id})
        if membership:
            await self.delete(membership[0])
        return True
