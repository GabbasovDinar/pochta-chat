from datetime import datetime

from app.models import Message
from app.models.message import MessageStatus
from app.repositories.message import message_repository
from app.repositories.user import user_repository

from .base_service import Base


class MessageService(Base):
    """Service for Message model operations."""

    async def send(self, user_id: str, chat_id: str, content: str) -> Message:
        """Send a message."""
        user = await user_repository.get_by_id(user_id)
        chat = await self.get_by_id(chat_id)
        if not chat:
            raise Exception("Chat not found")

        if not user.chats.filter(id=chat_id).exists():
            raise Exception("You are not a member of the chat")

        return await self.repository.create(chat_id=chat_id, user_id=user_id, content=content)

    async def mark_message_status(self, message_id: str, status: MessageStatus, **kwargs):
        """Mark a message as sent."""
        message = await message_repository.get_by_id(message_id)
        if not message:
            raise Exception("Message not found")

        await self.repository.update(message, status=status, **kwargs)

    async def mark_sending(self, message_id: str):
        """Mark a message as sending."""
        await self.mark_message_status(message_id, MessageStatus.SENDING)

    async def mark_sent(self, message_id: str):
        """Mark a message as sent."""
        await self.mark_message_status(message_id, MessageStatus.SENT, read_time=datetime.now())

    async def mark_error(self, message_id: str):
        """Mark a message as error."""
        await self.mark_message_status(message_id, MessageStatus.ERROR)

    async def mark_read(self, message_id: str):
        """Mark a message as read."""
        # TODO:
        await self.mark_message_status(message_id, MessageStatus.READ)


message_service = MessageService(repository=message_repository)
