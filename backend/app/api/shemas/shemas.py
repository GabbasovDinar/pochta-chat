from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Chat, ChatMembership, Message, User


class Login(BaseModel):
    """Login model."""

    email: str = Field(..., description="The email of the user.")
    password: str = Field(..., description="The password of the user.")


class Token(BaseModel):
    """Token model."""

    access_token: str = Field(..., description="The access token used for authorization.")
    token_type: str = Field(
        ..., description="The type of the token, typically 'bearer'.", default="bearer"
    )
    exp: int = Field(
        ..., description="The expiration time of the access token in UNIX timestamp format."
    )
    refresh_token: str | None = Field(
        None,
        description="The refresh token used to obtain a new access "
        "token when the current one expires.",
    )

    class Config:
        """Config for the Token model."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "exp": 1683509340,
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }


UserOut = pydantic_model_creator(User, name="User", exclude=("hashed_password",))
UserIn = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("hashed_password",)
)


ChatOut = pydantic_model_creator(
    Chat,
    name="Chat",
)
ChatIn = pydantic_model_creator(
    Chat,
    name="ChatIn",
    exclude_readonly=True,
)


ChatMembershipOut = pydantic_model_creator(
    ChatMembership,
    name="ChatMembership",
)
ChatMembershipIn = pydantic_model_creator(
    ChatMembership,
    name="ChatMembershipIn",
    exclude_readonly=True,
)


MessageOut = pydantic_model_creator(
    Message,
    name="Message",
)
MessageIn = pydantic_model_creator(
    Message,
    name="MessageIn",
    exclude_readonly=True,
)
