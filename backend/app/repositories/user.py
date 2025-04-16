from app.models import User

from .tortoise import TortoiseRepository


class UserRepository(TortoiseRepository):
    """Repository for User model operations."""

    PREFETCH_FIELDS = ["chat_memberships__chat"]


user_repository = UserRepository(model=User)
