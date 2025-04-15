from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.services import get_user_service
from app.api.schemas.user import RegisterIn, Token
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=Token)
async def register(
    registration_data: RegisterIn,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Register a new user."""
    try:
        return await user_service.register(
            registration_data.username, registration_data.email, registration_data.password
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Login a user."""
    try:
        return await user_service.login(form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
