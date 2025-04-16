from app.models import ChatMembership

from .tortoise import TortoiseRepository


class ChatMembershipRepository(TortoiseRepository):
    """Repository for ChatMembership model operations."""

    PREFETCH_FIELDS = ["user", "chat"]


chat_membership_repository = ChatMembershipRepository(model=ChatMembership)
