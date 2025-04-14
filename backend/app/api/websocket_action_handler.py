from fastapi import WebSocket

from app.services.chat import chat_service
from app.services.message import message_service
from app.utils.connection_manager import manager


class WebSocketActionHandler:
    """Handle WebSocket actions."""

    def __init__(self, websocket: WebSocket, user_id: str):
        """Initialize the WebSocketActionHandler."""
        self.websocket = websocket
        self.user_id = user_id

    async def send(self, data: dict) -> None:
        """Send a message."""
        chat_id = data.get("chat_id")
        if not chat_id:
            return await self.websocket.send_json({"error": "Invalid send event data"})

        try:
            message = await chat_service.send_message(self.user_id, chat_id, data.get("content"))
        except Exception as e:  # pylint: disable=broad-exception-caught
            return await self.websocket.send_json({"error": str(e)})

        recipient_ids = await chat_service.get_member_ids(chat_id)
        message_payload = {
            "type": "message",
            "id": str(message.id),
            "chat_id": chat_id,
            "user_id": self.user_id,
            "content": data.get("content"),
            "timestamp": message.created_at.isoformat(),
            "status": message.status,
        }
        await manager.broadcast(message_payload, recipient_ids)

    async def read(self, data: dict) -> None:
        """Mark a message as read."""
        message_id = data.get("message_id")
        if not message_id:
            return await self.websocket.send_json({"error": "Invalid read event data"})

        message = await message_service.mark_read(message_id=message_id)
        if not message:
            return await self.websocket.send_json({"error": "Message not found"})

        notify_payload = {
            "type": "notification",
            "chat_id": message.chat_id,
            "message_id": str(message.id),
            "status": message.status,
        }
        await manager.send_personal_message(notify_payload, str(message.user_id))

    async def process(self, data: dict) -> None:
        """Process an action."""
        action = data.get("action")
        if not action:
            return await self.websocket.send_json({"error": "Invalid action"})

        if not hasattr(self, action):
            return await self.websocket.send_json({"error": "Invalid action"})

        return await getattr(self, action)(data)
