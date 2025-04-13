from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.authenticate import oauth2_authenticate
from app.models.user import User

router = APIRouter()


@router.get("/history/{chat_id}")
async def get_message_history(
    chat_id: str,
    limit: int = 50,
    offset: int = 0,
    user: Annotated[User, Depends(oauth2_authenticate)] = None,
):
    """Get message history."""
    # TODO:
