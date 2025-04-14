from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, OAuth2PasswordBearer

from app.repositories.user import user_repository
from app.utils.jwt import jwt_token

security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def oauth2_authenticate(token: str = Depends(oauth2_scheme)):
    """Authenticate a user using OAuth2 authentication."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt_token.verify(token, credentials_exception)

    user = await user_repository.get_by_id(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
