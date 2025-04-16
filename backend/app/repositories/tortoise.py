from .base import Base


class TortoiseRepository(Base):
    """Repository for Tortoise model operations."""

    PREFETCH_FIELDS = []

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

    async def delete(self, instance):
        """Delete an existing instance of the model."""
        await instance.delete()
        return True

    async def search(
        self,
        filter: dict,
        order: str = "id",
        limit: int = 1000,
        offset: int = 0,
        prefetch_fields: list[str] = [],
    ):
        """Search for instances of the model."""
        if filter:
            query = self.model.filter(**filter)
        else:
            query = self.model.all()

        query = query.order_by(order).offset(offset).limit(limit)
        prefetch_fields = prefetch_fields or self.PREFETCH_FIELDS
        if prefetch_fields:
            query = query.prefetch_related(*prefetch_fields)
        return await query

    async def browse(self, id: str, prefetch_fields: list[str] = []):
        """Browse for instances of the model."""
        query = self.model.get_or_none(id=id)
        prefetch_fields = prefetch_fields or self.PREFETCH_FIELDS
        if prefetch_fields:
            query = query.prefetch_related(*prefetch_fields)
        return await query

    async def exists(self, filter: dict):
        """Check if an instance of the model exists."""
        return await self.model.exists(**filter)
