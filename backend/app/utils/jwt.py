from datetime import datetime, timedelta
from typing import Any

import jwt

from app.core.config import settings


class JWTToken:
    """JWT token utilities for authentication and token generation."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
        refresh_token_expire_days,
    ):
        """Initialize the JWT token utilities."""
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def verify(self, token: str, credentials_exception: Exception | None = None):
        """Verify a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            sub = payload.get("sub")
            if sub is None:
                raise credentials_exception
            return payload
        except jwt.ExpiredSignatureError as error:
            raise Exception("Token has expired.") from error
        except jwt.InvalidSignatureError as error:
            raise Exception("Invalid token signature.") from error
        except jwt.InvalidTokenError as error:
            raise Exception("Invalid token.") from error

    def generate(self, data: dict[str, Any] | None) -> dict[str, Any]:
        """Generate a JWT token."""
        now = datetime.utcnow()
        exp = now + timedelta(minutes=self.access_token_expire_minutes)

        access_token = self._generate_token(data, exp)
        refresh_token = self._generate_token(
            data, now + timedelta(days=self.refresh_token_expire_days)
        )

        return {
            "access_token": access_token,
            "exp": int(exp.timestamp()),
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }

    def _generate_token(self, data: dict[str, Any], expire) -> str:
        """Generate a JWT token."""
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token


jwt_token = JWTToken(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    refresh_token_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
)
