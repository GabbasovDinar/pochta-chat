from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections for different users or chat groups."""

    def __init__(self):
        """Initialize the connection manager."""
        # Dictionary mapping user_id -> list of active WebSocket connections
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """Accept a WebSocket connection and registers it under the given user_id."""
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        """Remove a WebSocket connection from the active connections for the specified user."""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message, user_id: str):
        """Send a JSON message to a specific user (to all of their connections)."""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

    async def broadcast(self, message, user_ids: list[str]):
        """Broadcast a message to a list of users."""
        for uid in user_ids:
            await self.send_personal_message(message, uid)


manager = ConnectionManager()
