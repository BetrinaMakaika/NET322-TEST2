"""Entry point for the WebSocket live-feed server."""

from __future__ import annotations

import asyncio
import json
import websockets

from wss.broadcaster import Broadcaster
from wss.handler import live


# Shared fake live queue
reading_queue = asyncio.Queue()


async def fake_reading_source(broadcaster):

    """
    TEMPORARY DEMO SOURCE.

    Later you can connect this to:
      - shared DB polling
      - shared queue
      - IPC
    """

    counter = 0

    while True:

        reading = {
            "sensor_id": "temp-01",
            "type": "temperature",
            "value": 20 + counter,
            "timestamp": counter,
        }

        await broadcaster.publish(reading)

        counter += 1

        await asyncio.sleep(3)


async def websocket_handler(
    websocket,
    path,
):

    await live(
        websocket,
        path,
        broadcaster,
    )


async def main() -> None:
    """Boot WebSocket server."""

    global broadcaster

    broadcaster = Broadcaster()

    # Start demo publisher
    asyncio.create_task(
        fake_reading_source(broadcaster)
    )

    server = await websockets.serve(
        websocket_handler,
        "127.0.0.1",
        8765,
    )

    print(
        "WebSocket server running at "
        "ws://127.0.0.1:8765/live"
    )

    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())