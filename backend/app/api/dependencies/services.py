from fastapi import Depends

from app.repositories.chat import chat_repository
from app.repositories.chat_membership import chat_membership_repository
from app.repositories.message import message_repository
from app.repositories.user import user_repository
from app.services.chat import ChatService
from app.services.chat_membership import ChatMembershipService
from app.services.message import MessageService
from app.services.user import UserService


def get_user_service() -> UserService:
    """Dependency function to retrieve the UserService instance.

    Returns:
        UserService: A shared instance of the UserService.

    """
    return UserService(repository=user_repository)


def get_chat_membership_service() -> ChatMembershipService:
    """Dependency function to retrieve the ChatMembershipService instance.

    Returns:
        ChatMembershipService: A shared instance of the ChatMembershipService.

    """
    return ChatMembershipService(repository=chat_membership_repository)


def get_message_service() -> MessageService:
    """Dependency function to retrieve the MessageService instance.

    Returns:
        MessageService: A shared instance of the MessageService.

    """
    return MessageService(repository=message_repository)


def get_chat_service(
    user_service: UserService = Depends(get_user_service),
    chat_membership_service: ChatMembershipService = Depends(get_chat_membership_service),
    message_service: MessageService = Depends(get_message_service),
) -> ChatService:
    """Dependency function to retrieve the ChatService instance.

    Returns:
        ChatService: A shared instance of the ChatService.

    """
    return ChatService(
        repository=chat_repository,
        user_service=user_service,
        chat_membership_service=chat_membership_service,
        message_service=message_service,
    )
