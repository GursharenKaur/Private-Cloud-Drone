from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    status,
    HTTPException,
)

from app.database.database import SessionLocal

from app.core.security import (
    authenticate_device_token,
    authenticate_user_token,
)

from app.streaming.manager import manager
from app.streaming.signaling import handle_message

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
):
    """
    Generic websocket endpoint.

    Camera:
        /ws/phone_001?token=<device_jwt>

    Dashboard:
        /ws/dashboard?token=<user_jwt>
    """

    print("🔥 WebSocket endpoint reached")

    print("Query params:", websocket.query_params)

    token = websocket.query_params.get("token")

    print("Token:", token)

    if not token:

        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing authentication token",
        )

        return

    db = SessionLocal()

    current_device = None

    try:

        # ---------------------------------------
        # Dashboard Authentication (User JWT)
        # ---------------------------------------

        if client_id == "dashboard":

            authenticate_user_token(
                token=token,
                db=db,
            )

            role = "dashboard"

        # ---------------------------------------
        # Device Authentication (Device JWT)
        # ---------------------------------------

        else:

            current_device = authenticate_device_token(
                token=token,
                db=db,
            )

            role = "camera"

    except HTTPException as e:

        print("Authentication failed:", e.detail)

        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason=e.detail,
        )

        return

    finally:

        db.close()

    await manager.connect(
        websocket=websocket,
        client_id=client_id,
        role=role,
        device=current_device,
    )

    manager.list_clients()

    try:

        while True:

            data = await websocket.receive_json()

            print(f"[{client_id}] -> {data}")

            await handle_message(
                client_id,
                data,
            )

    except WebSocketDisconnect:

        manager.disconnect(client_id)

        manager.list_clients()