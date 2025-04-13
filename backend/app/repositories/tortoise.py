from tortoise.exceptions import DoesNotExist

from .base import Base


class TortoiseRepository(Base):
    """Repository for Tortoise model operations."""

    async def create(self, **kwargs):
        """Create a new instance of the model."""
        instance = await self.model.create(**kwargs)
        return instance

    async def update(self, instance, **kwargs):
        """Update an existing instance of the model."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await instance.save()
        return instance

    async def delete(self, **kwargs):
        """Delete an existing instance of the model."""
        deletion_count = await self.model.filter(**kwargs).delete()
        return deletion_count

    async def get_single(self, **kwargs):
        """Get a single instance of the model."""
        try:
            instance = await self.model.get(**kwargs)
            return instance
        except DoesNotExist:
            return None

    async def get_multi(self, order: str = "id", limit: int = 100, offset: int = 0):
        """Get multiple instances of the model."""
        instances = await self.model.all().order_by(order).offset(offset).limit(limit)
        return instances

    async def get_all(self):
        """Get all instances of the model."""
        instances = await self.model.all()
        return instances

    async def get_by_id(self, model_id: str):
        """Get an instance of the model by its ID."""
        return await self.model.get_or_none(id=model_id)
