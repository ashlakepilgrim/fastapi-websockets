# WebSocket Broadcast

A simple multi-client WebSocket broadcast server built with FastAPI.

## Features

- FastAPI WebSocket endpoint
- Multiple simultaneous clients
- Broadcast messages to all connected clients
- Unique client IDs
- Active client list
- Server-rendered HTML using Jinja2
- Static CSS and JavaScript
- Application logging
- HTTP and WebSocket tests with pytest

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Run Prototype

```bash
uvicorn prototype:app --reload
```

## Run Tests

```bash
PYTHONPATH=. pytest -v
```
