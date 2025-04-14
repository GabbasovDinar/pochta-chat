from app.models import Chat, ChatMembership

from .tortoise import TortoiseRepository


class ChatRepository(TortoiseRepository):
    """Repository for Chat model operations."""

    async def get_all_chats_for_user(self, user_id) -> list[Chat]:
        """Get all chats for a user."""
        memberships = await ChatMembership.filter(user_id=user_id).prefetch_related("chat")
        chats = [membership.chat for membership in memberships]
        return chats

    async def get_membership(self, user_id: str, chat_id: str) -> ChatMembership:
        """Get membership of a user in a chat."""
        return await ChatMembership.get(user_id=user_id, chat_id=chat_id)


chat_repository = ChatRepository(model=Chat)
