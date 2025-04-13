import logging

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise as tortoise_register

from app.core.config import settings

_logger = logging.getLogger(__name__)


DATABASE_URL = settings.get_db_url()

# TODO: use aerich.models for migration without auto generatation schemas

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        },
    },
}


def register_tortoise(app):
    """Register Tortoise ORM with a FastAPI app.

    This function integrates Tortoise ORM with the provided FastAPI application.
    It sets up the database connections, registers the models, and adds exception
    handlers for database-related errors.

    Args:
        app: The FastAPI application instance.

    Raises:
        Exception: If an error occurs during the registration process.

    """
    try:
        _logger.info("Starting Tortoise ORM registration.")
        tortoise_register(
            app,
            config=TORTOISE_ORM,
            generate_schemas=True,
            add_exception_handlers=True,
        )
        _logger.info("Tortoise ORM registered successfully.")
    except Exception as e:
        _logger.error(f"Failed to register Tortoise ORM: {e}")
        raise e


async def init_db():
    """Initialize the database connection using Tortoise ORM."""
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()


async def close_db():
    """Close the database connection using Tortoise ORM."""
    await Tortoise.close_connections()
