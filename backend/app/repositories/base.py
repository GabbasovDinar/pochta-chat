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
    async def update(self, instance, **kwargs):
        """Update an existing instance of the model."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instance):
        """Delete an existing instance of the model."""
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        filter: dict,
        order: str = "id",
        limit: int = 1000,
        offset: int = 0,
        prefetch_fields: list[str] = [],
    ):
        """Search for instances of the model."""
        raise NotImplementedError

    @abstractmethod
    async def browse(self, id: str, prefetch_fields: list[str] = []):
        """Browse for instances of the model."""
        raise NotImplementedError

    @abstractmethod
    async def exists(self, filter: dict):
        """Check if an instance of the model exists."""
        raise NotImplementedError
