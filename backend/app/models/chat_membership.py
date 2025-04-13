from tortoise import fields

from .base import Base


class ChatMembership(Base):
    """Chat membership model representing a user's membership in a chat."""

    user = fields.ForeignKeyField("models.User", related_name="chats", on_delete=fields.CASCADE)
    chat = fields.ForeignKeyField("models.Chat", related_name="members", on_delete=fields.CASCADE)

    class Meta:
        """Meta class for ChatMembership model."""

        unique_together = (("user", "chat"),)
