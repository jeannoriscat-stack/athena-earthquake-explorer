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

## Demo

A short demonstration video shows the Earthquake Activity Explorer running in Athena AI, retrieving live USGS earthquake data and updating the widget using different magnitude and time-range filters.

[View the demonstration video](./earthquake-activity-explorer-demo.mp4)

## Run Locally

### 1. Clone the repository

```powershell
git clone https://github.com/jeannoriscat-stack/athena-earthquake-explorer.git
cd athena-earthquake-explorer
```

### 2. Install the dependencies

```powershell
py -m pip install "mcp[cli]" httpx
```

### 3. Start the MCP server

```powershell
py server.py
```

The MCP server runs locally on:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

### 4. Create a Cloudflare Quick Tunnel

Open a second terminal and run:

```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```

Cloudflare will generate a temporary public URL similar to:

```text
https://your-random-url.trycloudflare.com
```

Keep this terminal running.

### 5. Connect Athena AI

From the main Athena AI Agent page:

1. Click **Edit Agent**
2. Open **Capabilities**
3. Locate the **MCP** configuration
4. Enter the Cloudflare URL followed by `/mcp` in **MCP Server URL**
5. Set **MCP Authorization** to **No Auth**

Example:

```text
https://your-random-url.trycloudflare.com/mcp
```

Update the agent configuration.

### 6. Test the application

Once connected, the Athena AI agent can call the MCP server, retrieve live earthquake data from the USGS Earthquake Hazards Program API, and render the interactive Earthquake Activity Explorer widget.

Use the widget controls to change the minimum magnitude and time range, then retrieve the earthquake data.

> **Note:** Cloudflare Quick Tunnel URLs are temporary. A new URL may be generated when the tunnel is restarted.