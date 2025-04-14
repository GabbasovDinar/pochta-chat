from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authenticate import oauth2_authenticate
from app.api.dependencies.services import get_chat_service
from app.models.user import User
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/join/{chat_id}")
async def join_chat(
    chat_id: Annotated[str, ...],
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Join a chat."""
    try:
        result = await chat_service.join(chat_id, str(user.id))
        return {"msg": "Successfully joined the chat", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/leave/{chat_id}")
async def leave_chat(
    chat_id: str,
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Leave a chat."""
    try:
        result = await chat_service.leave(chat_id, str(user.id))
        return {"msg": "Successfully left the chat", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/history/{chat_id}")
async def get_message_history(
    chat_id: Annotated[str, ...],
    limit: int = 50,
    offset: int = 0,
    user: Annotated[User, Depends(oauth2_authenticate)] = None,
    chat_service: Annotated[ChatService, Depends(get_chat_service)] = None,
):
    """Get message history."""
    try:
        result = await chat_service.get_history(chat_id, str(user.id), limit, offset)
        return {"msg": "Successfully got message history", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/members/{chat_id}")
async def get_chat_members(
    chat_id: Annotated[str, ...],
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Get chat members."""
    try:
        result = await chat_service.get_members(chat_id)
        return {"msg": "Successfully got chat members", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
