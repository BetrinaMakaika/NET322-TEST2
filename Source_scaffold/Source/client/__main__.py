"""Entry point for the sensor simulator."""

from __future__ import annotations

import argparse
import asyncio
import yaml

from client.simulator import SensorSimulator


async def main() -> None:
    """Load config and start all sensors."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        required=True,
    )

    args = parser.parse_args()

    with open(args.config, "r") as f:

        config = yaml.safe_load(f)

    server_host = config["server"]["host"]

    server_port = config["server"]["port"]

    tasks = []

    for sensor in config["sensors"]:

        simulator = SensorSimulator(
            sensor_id=sensor["id"],
            sensor_type=sensor["type"],
            interval_seconds=sensor["interval_seconds"],
            host=server_host,
            port=server_port,
        )

        tasks.append(
            asyncio.create_task(simulator.run())
        )

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())