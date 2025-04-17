from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authenticate import oauth2_authenticate
from app.api.dependencies.services import get_chat_service
from app.api.schemas.chat import (
    ChatActionResponse,
    ChatHistoryResponse,
    ChatResponse,
    CreateChatRequest,
)
from app.models.user import User
from app.services.chat import ChatService

router = APIRouter(tags=["chats"])


@router.post("/join/{chat_id}", response_model=ChatActionResponse)
async def join(
    chat_id: UUID,
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Join a chat."""
    try:
        result = await chat_service.join(chat_id, str(user.id))
        return {"msg": "Successfully joined the chat", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/leave/{chat_id}", response_model=ChatActionResponse)
async def leave(
    chat_id: UUID,
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Leave a chat."""
    try:
        result = await chat_service.leave(chat_id, str(user.id))
        return {"msg": "Successfully left the chat", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/history/{chat_id}", response_model=ChatHistoryResponse)
async def get_message_history(
    chat_id: UUID,
    limit: int = 50,
    offset: int = 0,
    order: str = "created_at",
    user: Annotated[User, Depends(oauth2_authenticate)] = None,
    chat_service: Annotated[ChatService, Depends(get_chat_service)] = None,
):
    """Get message history."""
    try:
        result = await chat_service.get_history(chat_id, order, limit, offset)
        return {"msg": "Successfully got message history", "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/group", response_model=list[ChatResponse])
async def get_group_chats(
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Get group chats."""
    try:
        return await chat_service.get_group_chats(str(user.id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/", response_model=ChatResponse)
async def create_chat(
    data: CreateChatRequest,
    user: Annotated[User, Depends(oauth2_authenticate)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    """Create a chat."""
    try:
        user_ids = data.user_ids
        if str(user.id) not in user_ids:
            user_ids.append(user.id)

        chat = await chat_service.action_create(
            user_ids=user_ids, chat_type=data.chat_type, name=data.name
        )
        return chat
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
