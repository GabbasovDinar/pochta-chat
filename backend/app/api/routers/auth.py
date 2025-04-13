from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.services import user_service

router = APIRouter(prefix="/auth")


# TODO: add response shemas


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login a user."""
    try:
        return await user_service.login(form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


# @router.post("/refresh")
# async def refresh_token(refresh_token: Annotated[str, Body(..., embed=True)]):
#     """Refresh a token."""
#     # TODO: refresh token
