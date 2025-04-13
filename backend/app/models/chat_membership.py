from tortoise import fields

from .base import Base


class ChatMembership(Base):
    """Chat model representing a private or group chat."""

    user = fields.ForeignKeyField("models.User", related_name="chats", on_delete=fields.CASCADE)
    chat = fields.ForeignKeyField("models.Chat", related_name="members", on_delete=fields.CASCADE)
