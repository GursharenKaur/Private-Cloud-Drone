from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    """
    Stores every connected client.

    Example:

    {
        "phone_001": {
            "role": "camera",
            "websocket": <WebSocket>
        },

        "dashboard": {
            "role": "dashboard",
            "websocket": <WebSocket>
        }
    }
    """

    def __init__(self):
        self.active_connections: Dict[str, dict] = {}

    async def connect(
        self,
        websocket: WebSocket,
        client_id: str,
        role: str,
        device=None,
    ):
        """
        Accept a new websocket connection.
        """

        await websocket.accept()

        self.active_connections[client_id] = {
            "role": role,
            "websocket": websocket,
            "device": device,
        }

        print(f"✅ {client_id} connected as {role}")

    def disconnect(self, client_id: str):
        """
        Remove a disconnected client.
        """

        if client_id in self.active_connections:

            role = self.active_connections[client_id]["role"]

            del self.active_connections[client_id]

            print(f"❌ {client_id} ({role}) disconnected")

    def get_websocket(self, client_id: str):
        """
        Return websocket of one client.
        """

        client = self.active_connections.get(client_id)

        if client:

            return client["websocket"]

        return None

    async def send_to(self, client_id: str, message: dict):
        """
        Send JSON to one client.
        """

        websocket = self.get_websocket(client_id)

        if websocket:

            await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """
        Send JSON to every connected client.
        """

        for client in self.active_connections.values():

            await client["websocket"].send_json(message)

    def list_clients(self):
        """
        Print all connected clients.
        """

        print("\n========== CONNECTED CLIENTS ==========")

        for client_id, client in self.active_connections.items():

            print(
                f"{client_id} -> {client['role']}"
            )

        print("=======================================\n")


manager = ConnectionManager()