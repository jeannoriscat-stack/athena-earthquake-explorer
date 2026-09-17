from datetime import datetime, timedelta, timezone

import httpx
from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, TextContent

mcp = MCPServer("Earthquake Activity Explorer")

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

WIDGET_URI = "ui://widget/earthquake-explorer.html"

with open("widget.html", "r", encoding="utf-8") as f:
    WIDGET_HTML = f.read()


@mcp.resource(
    WIDGET_URI,
    name="Earthquake Activity Explorer",
    mime_type="text/html+skybridge",
    meta={
        "openai/widgetPrefersBorder": True,
    },
)
def earthquake_widget() -> str:
    return WIDGET_HTML


@mcp.tool(
    meta={
        "openai/outputTemplate": WIDGET_URI,
        "openai/widgetAccessible": True,
        "openai/toolInvocation/invoking": "Retrieving earthquake data...",
        "openai/toolInvocation/invoked": "Earthquake data loaded",
    }
)

async def get_earthquakes(
    min_magnitude: float = 2.5,
    days: int = 1,
    limit: int = 50,
) -> dict:
    """Get recent real earthquake data from the USGS."""

    days = max(1, min(days, 30))
    limit = max(1, min(limit, 100))

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": min_magnitude,
        "orderby": "time",
        "limit": limit,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(USGS_URL, params=params)
        response.raise_for_status()
        data = response.json()

    earthquakes = []

    for feature in data.get("features", []):
        p = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [])

        event_time = p.get("time")
        if event_time:
            event_time = datetime.fromtimestamp(
                event_time / 1000, tz=timezone.utc
            ).isoformat()

        earthquakes.append({
            "id": feature.get("id"),
            "magnitude": p.get("mag"),
            "place": p.get("place"),
            "time": event_time,
            "depth_km": coords[2] if len(coords) > 2 else None,
            "longitude": coords[0] if len(coords) > 0 else None,
            "latitude": coords[1] if len(coords) > 1 else None,
            "usgs_url": p.get("url"),
        })

    result = {
        "source": "USGS Earthquake Hazards Program",
        "count": len(earthquakes),
        "filters": {
            "min_magnitude": min_magnitude,
            "days": days,
        },
        "earthquakes": earthquakes,
    }

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"{len(earthquakes)} earthquakes retrieved from USGS."
        )
    ],
        structuredContent=result,
        _meta={
            "openai/outputTemplate": WIDGET_URI
        }
    )


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        ),
    )