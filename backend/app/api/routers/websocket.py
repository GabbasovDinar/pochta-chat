from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils import jwt_token
from app.utils.connection_manager import manager
from backend.app.api.websocket_action_handler import WebSocketActionHandler

router = APIRouter(tags=["websocket"])


@router.websocket("/connection")
async def websocket_connection(websocket: WebSocket):
    """Accept a WebSocket connection and registers it under the given user_id."""
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt_token.verify(token)
    except Exception:  # pylint: disable=broad-exception-caught
        await websocket.close(code=1008)
        return

    user_id = payload.get("sub")
    if user_id is None:
        await websocket.close(code=1008)
        return

    await manager.connect(user_id, websocket)
    action_handler = WebSocketActionHandler(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if not action:
                await websocket.send_json({"error": "No action provided"})
                continue

            await action_handler.process(data)

    except WebSocketDisconnect:
        manager.disconnect(int(user_id), websocket)
