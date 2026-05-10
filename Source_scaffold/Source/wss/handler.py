"""WebSocket connection handler."""

from __future__ import annotations

import json


async def live(
    websocket,
    path: str,
    broadcaster,
) -> None:
    """Handle one WebSocket connection."""

    await broadcaster.register(websocket)

    try:

        async for message in websocket:

            data = json.loads(message)

            if data.get("action") == "subscribe":

                sensors = data.get("sensors", [])

                await broadcaster.set_subscription(
                    websocket,
                    sensors,
                )

                await websocket.send(
                    json.dumps({
                        "status": "subscribed",
                        "sensors": sensors,
                    })
                )

    except Exception as e:

        print(f"WebSocket error: {e}")

    finally:

        await broadcaster.unregister(websocket)