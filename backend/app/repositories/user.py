from tortoise.exceptions import DoesNotExist

from app.models import User

from .tortoise import TortoiseRepository


class UserRepository(TortoiseRepository):
    """Repository for User model operations."""

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        try:
            user = await self.get_single(email=email)
            return user
        except DoesNotExist:
            return None


user_repository = UserRepository(model=User)
