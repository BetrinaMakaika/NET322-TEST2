from __future__ import annotations

import uuid
import json

from aiohttp import web

from server.serialization import negotiate, serialize

storage = None


async def list_sensors(request):

    sensors = await storage.list_sensors()

    media_type = negotiate(request)

    body = serialize(sensors, media_type)

    return web.Response(
        body=body,
        content_type=media_type
    )


async def get_readings(request):

    sensor_id = request.match_info["id"]

    from_ts = request.query.get("from")
    to_ts = request.query.get("to")

    readings = await storage.get_readings(
        sensor_id,
        float(from_ts) if from_ts else None,
        float(to_ts) if to_ts else None,
    )

    media_type = negotiate(request)

    body = serialize(readings, media_type)

    return web.Response(
        body=body,
        content_type=media_type
    )


async def register_sensor(request):

    data = await request.json()

    await storage.add_sensor(data)

    return web.Response(
        status=201,
        text="Sensor registered"
    )


async def delete_sensor(request):

    sensor_id = request.match_info["id"]

    await storage.remove_sensor(sensor_id)

    return web.Response(status=204)


@web.middleware
async def session_cookie_middleware(request, handler):

    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())

    response = await handler(request)

    response.set_cookie(
        "session_id",
        session_id
    )

    return response


def build_app(shared_storage):

    global storage

    storage = shared_storage

    app = web.Application(
        middlewares=[session_cookie_middleware]
    )

    app.router.add_get("/sensors", list_sensors)

    app.router.add_get(
        "/sensors/{id}/readings",
        get_readings
    )

    app.router.add_post(
        "/sensors",
        register_sensor
    )

    app.router.add_delete(
        "/sensors/{id}",
        delete_sensor
    )

    return app