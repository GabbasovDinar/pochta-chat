from app.core.security import security
from app.models import User
from app.utils.jwt import jwt_token

from .base import Base


class UserService(Base):
    """Service for User model operations."""

    async def create(self, name: str, email: str, password: str, **kwargs) -> User:
        """Create a new user."""
        # Override to hash password
        hashed_password = security.hash(password)
        user = await super().create(name=name, email=email, password_hash=hashed_password, **kwargs)
        return user

    async def authenticate(self, email: str, password: str) -> User | None:
        """Authenticate a user."""
        user = await self.search({"email": email})
        if not user:
            raise Exception("User not found")

        user = user[0]
        is_valid = security.verify(password, user.password_hash)
        if not is_valid:
            raise Exception("Invalid password")

        return user

    async def register(self, username: str, email: str, password: str) -> User:
        """Register a new user."""
        user = await self.search({"email": email})
        if user:
            raise Exception("User already exists")

        return await self.create(**{
            "name": username,
            "email": email,
            "password": password,
        })

    async def login(self, email: str, password: str) -> str:
        """Login a user."""
        user = await self.authenticate(email, password)
        if not user:
            raise Exception("Incorrect username or password")

        return jwt_token.generate({"sub": str(user.id)})
