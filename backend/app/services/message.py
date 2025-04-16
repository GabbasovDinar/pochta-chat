from app.models import Message

from .base import Base


class MessageService(Base):
    """Service for Message model operations."""

    def _prepare_websocket_payload(self, message: Message) -> dict:
        """Prepare a payload for a websocket message."""
        return {
            "id": str(message.id),
            "content": message.content,
            "status": message.status,
            "user_id": str(message.user_id),
            "timestamp": message.created_at.isoformat(),
            "chat_id": str(message.chat_id),
        }
