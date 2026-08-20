# WebSocket Echo

A simple WebSocket echo server built with FastAPI.

<img width="2560" height="1440" alt="2026-08-21_01-39-48" src="https://github.com/user-attachments/assets/d4a2d80c-049d-49ff-9e9a-2aa1bda4bd72" />

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
