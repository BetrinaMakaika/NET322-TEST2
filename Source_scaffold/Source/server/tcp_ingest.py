from __future__ import annotations

import asyncio
import struct

from proto.telemetry_pb2 import Reading

storage = None


async def handle_sensor(reader, writer):

    addr = writer.get_extra_info("peername")

    print(f"Sensor connected: {addr}")

    try:

        while True:

            header = await reader.readexactly(4)

            length = struct.unpack(">I", header)[0]

            payload = await reader.readexactly(length)

            reading = Reading()

            reading.ParseFromString(payload)

            await storage.add_reading(reading)

            print(
                f"Received {reading.sensor_id} "
                f"{reading.value}"
            )

    except asyncio.IncompleteReadError:

        print(f"Sensor disconnected: {addr}")

    except Exception as e:

        print(f"Malformed message: {e}")

    finally:

        writer.close()

        await writer.wait_closed()


async def start_tcp_server(
    host,
    port,
    shared_storage,
):

    global storage

    storage = shared_storage

    return await asyncio.start_server(
        handle_sensor,
        host,
        port,
    )