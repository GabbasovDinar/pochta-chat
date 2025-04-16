from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.dependencies.services import get_chat_service
from app.api.dependencies.websocket import get_connection_manager
from app.api.schemas.websocket import WebSocketMessage
from app.services.chat import ChatService
from app.utils import jwt_token
from app.utils.connection_manager import ConnectionManager

router = APIRouter(tags=["websocket"])


@router.websocket("/connection")
async def websocket_connection(
    websocket: WebSocket,
    chat_service: ChatService = Depends(get_chat_service),
    connection_manager: ConnectionManager = Depends(get_connection_manager),
):
    """Accept a WebSocket connection and registers it under the given user_id.

    Incoming JSON message should match the following structure:

        {
            "action": "create" | "read",
            "chat_id": "string (required for 'create' and 'read')",
            "content": "string (required for 'create')",
            "message_id": "string (optional, for idempotency)"
        }

    """
    token = websocket.query_params.get("token")
    if not token:
        print("no token!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        await websocket.close(code=403)
        return

    try:
        payload = jwt_token.verify(token)
    except Exception:
        print("Invalid token!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        await websocket.close(code=403)
        return

    user = await chat_service.user_service.browse(payload.get("sub"))
    if not user:
        await websocket.close(code=403)
        print("not user!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return

    await connection_manager.connect(str(user.id), websocket)

    try:
        while True:
            data = await websocket.receive_json()
            try:
                WebSocketMessage.parse_obj(data)
            except Exception:  # pylint: disable=broad-exception-caught
                continue

            await chat_service._websocket_callback(user, data, connection_manager)

    except WebSocketDisconnect as e:
        print("WebSocketDisconnect!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", e)
        connection_manager.disconnect(str(user.id), websocket)
