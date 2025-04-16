from app.models import Chat

from .tortoise import TortoiseRepository


class ChatRepository(TortoiseRepository):
    """Repository for Chat model operations."""

    PREFETCH_FIELDS = ["messages", "messages__user", "memberships", "memberships__user"]


chat_repository = ChatRepository(model=Chat)
