from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import authenticate_device_token
from app.database.database import SessionLocal

from app.streaming.manager import manager
from app.streaming.signaling import handle_message

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
    print("Query params:", websocket.query_params)

    token = websocket.query_params.get("token")

    print("Token:", token)
    if not token:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing device token",
        )
        return

    db = SessionLocal()

    try:
        current_device = authenticate_device_token(
            token=token,
            db=db,
        )

    except HTTPException as e:
        print("Authentication failed:", e.detail)

        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason=e.detail,
        )
        return

    finally:
        db.close()

    role = "camera"

    await manager.connect(
        websocket=websocket,
        client_id=client_id,
        role=role,
        device=current_device,
    )

    try:
        while True:

            data = await websocket.receive_json()

            print(f"[{client_id}] -> {data}")

            await handle_message(client_id, data)

    except WebSocketDisconnect:

        manager.disconnect(client_id)