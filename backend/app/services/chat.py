from app.models import Chat, Message, MessageStatus, User
from app.models.chat import ChatType
from app.repositories.chat import ChatRepository

from .base import Base
from .chat_membership import ChatMembershipService
from .message import MessageService
from .user import UserService


class ChatService(Base):
    """Service for Chat model operations."""

    def __init__(
        self,
        repository: ChatRepository,
        message_service: MessageService,
        chat_membership_service: ChatMembershipService,
        user_service: UserService,
    ):
        self.repository = repository
        self.message_service = message_service
        self.chat_membership_service = chat_membership_service
        self.user_service = user_service

    async def ensure_exists(self, chat_id: str) -> Chat:
        """Ensure that a chat exists."""
        chat = await self.browse(chat_id)
        if not chat:
            raise Exception("Chat not found.")
        return chat

    async def join(self, chat_id: str, user_id: str) -> bool:
        """Join a chat."""
        chat = await self.ensure_exists(chat_id)
        if chat.chat_type == ChatType.PRIVATE:
            raise Exception("Cannot join a private chat.")

        await self.chat_membership_service.create(user_id=user_id, chat_id=chat_id)
        return True

    async def leave(self, chat_id: str, user_id: str) -> bool:
        """Leave a chat."""
        return await self.chat_membership_service.leave(chat_id, user_id)

    async def get_history(
        self, chat_id: str, order: str = "created_at", limit: int = 100, offset: int = 0
    ):
        """Get history of a chat."""
        await self.ensure_exists(chat_id)
        return await self.message_service.search({"chat_id": chat_id})

    async def get_group_chats(self, user_id: str) -> list[Chat]:
        """Get all group chats of a user."""
        return await self.search({"chat_type": ChatType.GROUP})

    async def action_create(self, user_ids: list[str], chat_type: ChatType, name: str) -> Chat:
        """Action to create a chat."""
        if chat_type == ChatType.PRIVATE:
            # don't create new private chat if it already exists
            chat = await self.get_private_chat(user_ids)
            if chat:
                return chat

        # create new chat
        chat = await self.create(chat_type=chat_type, name=name or ChatType.PRIVATE)
        # create chat memberships
        for user_id in user_ids:
            await self.chat_membership_service.create(user_id=user_id, chat_id=chat.id)

        return await self.browse(chat.id)

    async def get_private_chat(self, user_ids: list[str]) -> Chat | None:
        """Get a private chat between chat users."""
        chats = await self.search({"chat_type": ChatType.PRIVATE})

        target = set([str(user_id) for user_id in user_ids])
        for chat in chats:
            members = {str(m.user.id) for m in chat.memberships}
            if members == target:
                return chat
        return None

    async def get_users(self, chat_id: str) -> list[User]:
        """Get users of a chat."""
        memberships = await self.chat_membership_service.search({"chat_id": chat_id})
        return [membership.user for membership in memberships]

    async def _websocket_callback(self, current_user, data, connection):
        """WebSocket callback."""
        chat_id = data["chat_id"]
        await self.ensure_exists(chat_id)

        action = data["action"]
        if action == "create":
            message = await self.message_service.create(**{
                "chat_id": chat_id,
                "user_id": current_user.id,
                "content": data["content"],
                "status": MessageStatus.SENT,
            })
        elif action == "read":
            message = await self.message_mark_read(data["message_id"], current_user)
        else:
            raise Exception("Invalid action")

        user_ids = await self._prepare_callback_user_ids(current_user, data)
        payload = self.message_service._prepare_websocket_payload(message)
        await connection.broadcast(payload, user_ids)
        return True

    async def _prepare_callback_user_ids(self, current_user, data) -> list[str]:
        """Prepare users for callback."""
        action = data["action"]
        if action == "read":
            return [str(current_user.id)]

        users = await self.get_users(data["chat_id"])
        return [str(user.id) for user in users]

    async def message_mark_read(self, message_id: str, user: User) -> Message:
        """Mark a message as read."""
        message = await self.message_service.browse(message_id)
        if not message:
            raise Exception("Message not found")

        membership = await self.chat_membership_service.search({
            "user_id": user.id,
            "chat_id": message.chat_id,
        })
        if not membership:
            raise Exception("User is not a member of the chat")

        membership = membership[0]

        await self.chat_membership_service.update(
            membership, **{"last_read_time": message.created_at}
        )

        memberships = await self.chat_membership_service.search({"chat_id": message.chat_id})
        all_read = True
        for membership in memberships:
            if membership.last_read_time is None or membership.last_read_time < message.created_at:
                all_read = False
                break

        if all_read:
            await self.update(message, **{"status": MessageStatus.READ})

        return message
