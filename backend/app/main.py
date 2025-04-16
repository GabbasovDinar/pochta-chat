import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_router, websocket_router
from app.core.config import settings
from app.core.database import register_tortoise

_logger = logging.getLogger(__name__)

# create FastAPI app
app = FastAPI(
    title="Pochta-Chat API",
    description="Pochta-Chat API Service for sending and receiving messages.",
    version="1.0.0",
)

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include API router with a prefix for versioning
app.include_router(api_router, prefix="/api/v1")
app.include_router(websocket_router)

# register Tortoise ORM with FastAPI
register_tortoise(app)


@app.get("/ping", tags=["healthcheck"])
def ping():
    """Healthcheck endpoint."""
    return {"message": "pong"}


@app.on_event("startup")
async def startup_event():
    """Startup event."""
    _logger.info("Starting up Pochta-Chat API")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event."""
    _logger.info("Shutting down Pochta-Chat API")
