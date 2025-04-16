class Base:
    """Base class for all services."""

    def __init__(self, repository):
        """Initialize the service."""
        self.repository = repository

    async def create(self, **kwargs):
        """Create a new instance of the model."""
        return await self.repository.create(**kwargs)

    async def update(self, instance, **kwargs):
        """Update an existing instance of the model."""
        return await self.repository.update(instance, **kwargs)

    async def delete(self, instance):
        """Delete an existing instance of the model."""
        return await self.repository.delete(instance)

    async def search(self, filter: dict, order: str = "id", limit: int = 1000, offset: int = 0):
        """Search for instances of the model."""
        return await self.repository.search(filter, order, limit, offset)

    async def browse(self, id: str):
        """Browse for instances of the model."""
        return await self.repository.browse(id)

    async def exists(self, filter: dict):
        """Check if an instance of the model exists."""
        return await self.repository.exists(filter)
