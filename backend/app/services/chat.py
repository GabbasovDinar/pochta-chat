from app.repositories.chat import chat_repository
from app.repositories.message import message_repository
from app.repositories.user import user_repository

from .base_service import Base


class ChatService(Base):
    """Service for Chat model operations."""

    async def join(self, chat_id: str, user_id: str) -> bool:
        """Join a chat."""
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise Exception("User not found")

        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        if chat.chat_type == "private":
            raise Exception("Cannot join a private chat")

        # check if user is already a member
        if user.chats.filter(id=chat_id).exists():
            raise Exception("User is already a member of the chat")

        # create membership
        user.chats.add(chat)
        await user.save()

        return True

    async def leave(self, chat_id: str, user_id: str) -> bool:
        """Leave a chat."""
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise Exception("User not found")

        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        if not user.chats.filter(id=chat_id).exists():
            raise Exception("User is not a member of the chat")

        user.chats.remove(chat)
        await user.save()

        return True

    async def get_members(self, chat_id: str) -> list:
        """Get members of a chat."""
        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        return [membership.user for membership in chat.memberships]

    async def get_history(self, chat_id: str, user_id: str, limit: int = 50, offset: int = 0):
        """Get history of a chat."""
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise Exception("User not found")

        if not user.chats.filter(id=chat_id).exists():
            raise Exception("User is not a member of the chat")

        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        return await message_repository.get_messages_by_chat(chat_id, limit, offset)


chat_service = ChatService(repository=chat_repository)
