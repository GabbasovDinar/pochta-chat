from app.services.chat import ChatService, chat_service
from app.services.message import MessageService, message_service
from app.services.user import UserService, user_service


def get_user_service() -> UserService:
    """Dependency function to retrieve the UserService instance.

    Returns:
        UserService: A shared instance of the UserService.

    """
    return user_service


def get_chat_service() -> ChatService:
    """Dependency function to retrieve the ChatService instance.

    Returns:
        ChatService: A shared instance of the ChatService.

    """
    return chat_service


def get_message_service() -> MessageService:
    """Dependency function to retrieve the MessageService instance.

    Returns:
        MessageService: A shared instance of the MessageService.

    """
    return message_service
