from __future__ import annotations

import json
import yaml
import xml.etree.ElementTree as ET

from aiohttp import web


def negotiate(request: web.Request) -> str:

    accept = request.headers.get("Accept", "")

    if "application/xml" in accept:
        return "application/xml"

    if (
        "application/yaml" in accept or
        "text/yaml" in accept
    ):
        return "application/yaml"

    return "application/json"


def serialize(payload, media_type: str) -> bytes:

    if media_type == "application/json":
        return json.dumps(payload).encode()

    if media_type == "application/yaml":
        return yaml.dump(payload).encode()

    if media_type == "application/xml":

        root = ET.Element("response")

        if isinstance(payload, list):

            for item in payload:

                child = ET.SubElement(root, "item")

                for k, v in item.items():

                    elem = ET.SubElement(child, k)
                    elem.text = str(v)

        else:

            for k, v in payload.items():

                elem = ET.SubElement(root, k)
                elem.text = str(v)

        return ET.tostring(root)

    return json.dumps(payload).encode()