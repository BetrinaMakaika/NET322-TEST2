"""Tracks connected WebSocket clients and dispatches readings."""

from __future__ import annotations

import asyncio
import json


class Broadcaster:
    """Fan-out broadcaster for live readings."""

    def __init__(self) -> None:

        # websocket -> subscription set
        self.clients = {}

    async def register(self, websocket) -> None:
        """Register a connected client."""

        self.clients[websocket] = set()

        print("WebSocket client connected")

    async def unregister(self, websocket) -> None:
        """Remove disconnected client."""

        self.clients.pop(websocket, None)

        print("WebSocket client disconnected")

    async def set_subscription(
        self,
        websocket,
        sensor_ids,
    ) -> None:
        """Update sensor filter."""

        self.clients[websocket] = set(sensor_ids)

    async def publish(self, reading) -> None:
        """Broadcast reading to matching clients."""

        if not self.clients:
            return

        message = json.dumps({
            "sensor_id": reading["sensor_id"],
            "type": reading["type"],
            "value": reading["value"],
            "timestamp": reading["timestamp"],
        })

        disconnected = []

        async def send(client):

            try:

                subscriptions = self.clients[client]

                # no filter = receive all
                if (
                    not subscriptions or
                    reading["sensor_id"] in subscriptions
                ):

                    await asyncio.wait_for(
                        client.send(message),
                        timeout=2,
                    )

            except Exception:
                disconnected.append(client)

        await asyncio.gather(
            *(send(client) for client in self.clients)
        )

        for client in disconnected:
            await self.unregister(client)