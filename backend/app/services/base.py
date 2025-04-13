from abc import ABC, abstractmethod


class Base(ABC):
    """Base class for all services."""

    def __init__(self, repository):
        """Initialize the service."""
        self.repository = repository

    @abstractmethod
    async def create(self, **kwargs):
        """Create a new instance of the model."""
        return await self.repository.create(data=kwargs)

    @abstractmethod
    async def update(self, instance, **kwargs):
        """Update an existing instance of the model."""
        return await self.repository.update(instance, data=kwargs)

    @abstractmethod
    async def delete(self, **kwargs):
        """Delete an existing instance of the model."""
        return await self.repository.delete(data=kwargs)

    @abstractmethod
    async def get_single(self, **kwargs):
        """Get a single instance of the model."""
        return await self.repository.get_single(data=kwargs)

    @abstractmethod
    async def get_multi(self, order: str = "id", limit: int = 100, offset: int = 0):
        """Get multiple instances of the model."""
        return await self.repository.get_multi(order=order, limit=limit, offset=offset)

    @abstractmethod
    async def get_all(self):
        """Get all instances of the model."""
        return await self.repository.get_all()

    @abstractmethod
    async def get_by_id(self, model_id: str):
        """Get an instance of the model by its ID."""
        return await self.repository.get_by_id(model_id)
