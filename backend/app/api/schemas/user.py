from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    """Token model."""

    access_token: str = Field(..., description="The access token used for authorization.")
    token_type: str = Field("bearer", description="The type of the token, typically 'bearer'.")
    exp: int = Field(
        ..., description="The expiration time of the access token in UNIX timestamp format."
    )

    class Config:
        """Config for the Token model."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "exp": 1683509340,
            }
        }


class RegisterRequest(BaseModel):
    """Input schema for user registration."""

    name: str = Field(..., description="The name of the user.")
    email: EmailStr = Field(..., description="The email address associated with the user.")
    password: str = Field(..., description="The password of the user.")

    class Config:
        """Config for the RegisterRequest model."""

        json_schema_extra = {
            "example": {
                "name": "test",
                "email": "test@test.com",
                "password": "password",
            }
        }


class UserResponse(BaseModel):
    """Output schema for user."""

    id: UUID = Field(..., description="The unique identifier of the user.")
    email: EmailStr = Field(..., description="The email address associated with the user.")
    name: str = Field(..., description="The name of the user.")

    class Config:
        """Config for the UserResponse model."""

        from_attributes = True

        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e8-d701748f0852",
                "email": "test@test.com",
                "name": "test",
            }
        }
