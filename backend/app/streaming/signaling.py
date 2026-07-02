from app.streaming.manager import manager


async def handle_message(sender_id: str, message: dict):
    """
    Handle all signaling messages.

    Every incoming JSON must contain:

    {
        "target": "...",
        ...
    }

    The backend simply forwards the message
    to the requested target.
    """

    target = message.get("target")

    if not target:

        await manager.send_to(
            sender_id,
            {
                "type": "error",
                "message": "Missing target field."
            }
        )

        return

    await manager.send_to(target, message)