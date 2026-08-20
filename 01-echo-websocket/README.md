# Echo WebSocket

A simple WebSocket echo server built with FastAPI.

## Features

- Server-rendered HTML using Jinja2
- Static CSS and JavaScript
- WebSocket connection using FastAPI
- Echoes client messages back to the same client
- Basic application logging
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
