"""Single-sensor simulation logic."""

from __future__ import annotations

import asyncio
import random
import struct
import time

from proto.telemetry_pb2 import Reading


class SensorSimulator:
    """Simulates one sensor pushing readings."""

    def __init__(
        self,
        sensor_id: str,
        sensor_type: str,
        interval_seconds: float,
        host: str,
        port: int,
    ) -> None:

        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.interval = interval_seconds
        self.host = host
        self.port = port

    async def run(self) -> None:
        """Connect and continuously send readings."""

        backoff = 3

        while True:

            try:

                print(
                    f"[{self.sensor_id}] "
                    f"Connecting to {self.host}:{self.port}"
                )

                reader, writer = await asyncio.open_connection(
                    self.host,
                    self.port,
                )

                print(f"[{self.sensor_id}] Connected")

                while True:

                    reading = self._generate_reading()

                    payload = reading.SerializeToString()

                    frame = struct.pack(">I", len(payload)) + payload

                    writer.write(frame)

                    await writer.drain()

                    print(
                        f"[{self.sensor_id}] "
                        f"Sent value={reading.value}"
                    )

                    await asyncio.sleep(self.interval)

            except Exception as e:

                print(
                    f"[{self.sensor_id}] "
                    f"Connection error: {e}"
                )

                print(
                    f"[{self.sensor_id}] "
                    f"Retrying in {backoff} seconds..."
                )

                await asyncio.sleep(backoff)

    def _generate_reading(self):

        reading = Reading()

        reading.sensor_id = self.sensor_id

        reading.type = self.sensor_type

        if self.sensor_type == "temperature":
            value = random.uniform(18, 35)

        elif self.sensor_type == "humidity":
            value = random.uniform(40, 90)

        elif self.sensor_type == "soil_moisture":
            value = random.uniform(20, 80)

        elif self.sensor_type == "light":
            value = random.uniform(100, 1000)

        else:
            value = 0

        reading.value = round(value, 2)

        reading.timestamp = int(time.time())

        return reading