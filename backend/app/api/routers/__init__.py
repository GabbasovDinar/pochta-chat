from fastapi import APIRouter

from .chat import router as chat_router
from .user import router as user_router
from .websocket import router as ws_router

# http routers
api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(chat_router, prefix="/chats", tags=["chats"])

# websocket router
websocket_router = APIRouter()
websocket_router.include_router(ws_router, prefix="/websocket", tags=["websocket"])

__all__ = ["api_router", "websocket_router"]
