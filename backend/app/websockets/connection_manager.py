from fastapi import WebSocket


class ConnectionManager:
    """Connection manager for websockets."""

    def __init__(self):
        """Initialize the connection manager."""
        # Dictionary: key - chat_id, value - dictionary {user_id: WebSocket}
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, chat_id: int, user_id: int, websocket: WebSocket):
        """Connect to a chat."""
        await websocket.accept()
        # Add connection to dictionary
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket

    def disconnect(self, chat_id: int, user_id: int):
        """Disconnect from a chat."""
        if chat_id in self.active_connections:
            self.active_connections[chat_id].pop(user_id, None)
            if not self.active_connections[chat_id]:
                # If there are no connections in the chat, delete the key
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id: int, message: dict):
        """Broadcast a message to all participants of a chat."""
        if chat_id in self.active_connections:
            for _, ws in self.active_connections[chat_id].items():
                await ws.send_json(message)

    async def send_personal(self, chat_id: int, user_id: int, message: dict):
        """Send a personal message to a specific participant of a chat."""
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            await self.active_connections[chat_id][user_id].send_json(message)
