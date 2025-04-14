from app.models import ChatMembership, Message, MessageStatus
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

    async def send_message(self, user_id: str, chat_id: str, content: str) -> Message:
        """Send a message."""
        user = await user_repository.get_by_id(user_id)
        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        if not user.chats.filter(id=chat_id).exists():
            raise Exception("You are not a member of the chat")

        return await message_repository.create(
            chat_id=chat_id, user_id=user_id, content=content, status=MessageStatus.SENT
        )

    async def mark_read_message(self, chat_id: str, message_id: str, user_id: str) -> Message:
        """Mark a message as read by the current user."""
        user = await user_repository.get_by_id(user_id)
        if not user.chats.filter(id=chat_id).exists():
            raise Exception("User is not a member of the chat")

        message = await message_repository.get_by_id(message_id)
        if not message or str(message.chat_id) != chat_id:
            raise Exception("Message not found in this chat")

        membership = await self.get_membership(user_id, chat_id)
        if membership:
            membership.last_read_time = message.created_at
            await membership.save()

        if str(message.user_id) == user_id:
            return None

        member_ids = await self.get_member_ids(chat_id)
        recipients = [member_id for member_id in member_ids if member_id != message.user_id]

        if all(recipient.last_read_time > message.created_at for recipient in recipients):
            message.status = MessageStatus.READ
            await message.save()

        return message

    async def get_membership(self, user_id: str, chat_id: str) -> ChatMembership:
        """Get membership of a user in a chat."""
        return await self.repository.get_membership(user_id, chat_id)

    async def get_member_ids(self, chat_id: str) -> list:
        """Get members of a chat."""
        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        return [str(membership.user_id) for membership in chat.memberships]

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
