from uuid import uuid4

from tortoise import fields, models


class Base(models.Model):
    """Base model."""

    id = fields.UUIDField(primary_key=True, default=uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta class for BaseModel."""

        abstract = True

    def __str__(self):
        """Represent the model as a string."""
        return f"{self.__class__.__name__}({self.id})"
