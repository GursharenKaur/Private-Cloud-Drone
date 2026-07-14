from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
)

from app.database.database import SessionLocal

from app.core.security import (
    authenticate_device_token,
    authenticate_user_token,
    authorize_device,
)

from app.streaming.manager import manager
from app.streaming.signaling import handle_message
from app.core.device_capabilities import DeviceCapability

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
):
    """
    Authenticated WebSocket endpoint.

    Dashboard:
        /ws/dashboard?token=<user_jwt>

    Camera:
        /ws/phone_001?token=<device_jwt>
    """

    print("\n===================================")
    print("NEW WEBSOCKET CONNECTION")
    print("Client ID :", client_id)
    print("===================================\n")

    token = websocket.query_params.get("token")

    if not token:

        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing authentication token",
        )

        return

    db = SessionLocal()

    current_device = None

    try:

        if client_id == "dashboard":

            current_user = authenticate_user_token(
                token=token,
                db=db,
            )

            role = "dashboard"

            print(
                f"✅ Dashboard authenticated: {current_user.email}"
            )

        else:

            current_device = authenticate_device_token(
                token=token,
                db=db,
            )

            print("DeviceCapability module:", DeviceCapability.__module__)
            print("DeviceCapability members:", list(DeviceCapability))
            print("DeviceCapability dict:", DeviceCapability.__dict__.keys())
            current_device = authorize_device(
                current_device,
                capability=DeviceCapability.VIDEO_STREAM,
            )

            role = "camera"

            print(
                f"✅ Camera authenticated: {current_device.device_uuid}"
            )

    except HTTPException as e:

        db.close()

        print(f"❌ Authentication failed: {e.detail}")

        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason=e.detail,
        )

        return

    await manager.connect(
        websocket=websocket,
        client_id=client_id,
        role=role,
        device=current_device,
    )

    manager.list_clients()

    db.close()

    try:

        while True:

            message = await websocket.receive_json()

            print(f"[{client_id}] -> {message}")

            await handle_message(
                client_id,
                message,
            )

    except WebSocketDisconnect:

        print(f"❌ {client_id} disconnected")

        manager.disconnect(client_id)

        manager.list_clients()