# Earthquake Activity Explorer

Earthquake Activity Explorer is an interactive Athena AI application that explores recent earthquake activity using real public data from the USGS Earthquake Hazards Program.

## Architecture

Athena AI Agent → MCP Server (Python) → USGS Earthquake API → Interactive Athena Widget

## Features

- Retrieves real earthquake data from the USGS
- Filters earthquakes by minimum magnitude
- Filters earthquakes by time range
- Displays magnitude, place, depth, and event time
- Uses MCP to expose earthquake data to Athena AI
- Renders an interactive widget directly inside Athena

## Technologies

- Python
- Model Context Protocol (MCP)
- Athena AI
- USGS Earthquake Hazards Program API
- HTML / CSS / JavaScript
- httpx
- Git / GitHub

## Run Locally

Install the dependencies:

```powershell
py -m pip install "mcp[cli]" httpx