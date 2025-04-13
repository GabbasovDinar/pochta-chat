from abc import ABC, abstractmethod


class Base(ABC):
    """Base class for all repositories."""

    def __init__(self, model):
        """Initialize the repository."""
        self.model = model

    @abstractmethod
    async def create(self, **kwargs):
        """Create a new instance of the model."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        """Update an existing instance of the model."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        """Delete an existing instance of the model."""
        raise NotImplementedError

    @abstractmethod
    async def get_single(self, **kwargs):
        """Get a single instance of the model."""
        raise NotImplementedError

    async def get_multi(self, order: str = "id", limit: int = 100, offset: int = 0):
        """Get multiple instances of the model."""
        raise NotImplementedError

    async def get_all(self):
        """Get all instances of the model."""
        raise NotImplementedError
