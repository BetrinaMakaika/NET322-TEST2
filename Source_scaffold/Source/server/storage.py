from __future__ import annotations

from typing import Iterable, Optional


class MemoryStorage:

    def __init__(self):

        self.sensors = {}
        self.readings = []

    async def add_sensor(self, sensor) -> None:

        self.sensors[sensor["id"]] = sensor

    async def remove_sensor(self, sensor_id: str) -> None:

        self.sensors.pop(sensor_id, None)

    async def list_sensors(self) -> Iterable:

        return list(self.sensors.values())

    async def add_reading(self, reading) -> None:

        self.readings.append({
            "sensor_id": reading.sensor_id,
            "type": reading.type,
            "value": reading.value,
            "timestamp": reading.timestamp,
        })

    async def get_readings(
        self,
        sensor_id: str,
        from_ts: Optional[float] = None,
        to_ts: Optional[float] = None,
    ) -> Iterable:

        results = []

        for r in self.readings:

            if r["sensor_id"] != sensor_id:
                continue

            if from_ts and r["timestamp"] < from_ts:
                continue

            if to_ts and r["timestamp"] > to_ts:
                continue

            results.append(r)

        return results