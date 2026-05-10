from __future__ import annotations

import asyncio

from aiohttp import web

from server.storage import MemoryStorage
from server.rest_api import build_app
from server.tcp_ingest import start_tcp_server


async def main():

    storage = MemoryStorage()

    tcp_server = await start_tcp_server(
        "127.0.0.1",
        9000,
        storage,
    )

    app = build_app(storage)

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        "127.0.0.1",
        8000,
    )

    await site.start()

    print("REST API running on http://127.0.0.1:8000")

    print("TCP ingest running on 127.0.0.1:9000")

    async with tcp_server:
        await tcp_server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())