from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.authenticate import oauth2_authenticate
from app.api.dependencies.services import get_user_service
from app.api.schemas.user import RegisterRequest, TokenResponse, UserResponse
from app.models.user import User
from app.services.user import UserService

router = APIRouter(tags=["users"])


@router.post("/register", response_model=UserResponse)
async def register(
    registration_data: RegisterRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Register a new user."""
    try:
        return await user_service.register(
            registration_data.name, registration_data.email, registration_data.password
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Login a user."""
    try:
        return await user_service.login(form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.get("/me", response_model=UserResponse)
async def get_me(
    user: Annotated[User, Depends(oauth2_authenticate)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Get the current user."""
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.get("/", response_model=list[UserResponse])
async def get_users(
    user: Annotated[User, Depends(oauth2_authenticate)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Get all users."""
    try:
        return await user_service.search({})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
