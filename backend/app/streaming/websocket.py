from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.streaming.signaling import handle_message

from app.streaming.manager import manager

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    Generic websocket endpoint.

    Examples:
        ws://localhost:8000/ws/phone_001
        ws://localhost:8000/ws/dashboard
    """
    print("🔥 WebSocket endpoint reached")
    role = "camera"

    await manager.connect(
        websocket,
        client_id,
        role
    )

    try:
        while True:

            data = await websocket.receive_json()

            print(f"[{client_id}] -> {data}")

            await handle_message(client_id, data)

    except WebSocketDisconnect:

        manager.disconnect(client_id)