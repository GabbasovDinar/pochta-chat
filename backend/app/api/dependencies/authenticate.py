from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, OAuth2PasswordBearer

from app.api.dependencies.services import get_user_service
from app.services.user import UserService
from app.utils.jwt import jwt_token

security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def oauth2_authenticate(
    token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)
):
    """Authenticate a user using OAuth2 authentication."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_token.verify(token, credentials_exception)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    user = await user_service.browse(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
