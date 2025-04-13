# ruff: noqa: F821

from tortoise import fields

from .base import Base


class User(Base):
    """User model with hashed password for authentication."""

    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)

    sent_messages: fields.ReverseRelation["Message"]
    chats: fields.ReverseRelation["ChatMembership"]
