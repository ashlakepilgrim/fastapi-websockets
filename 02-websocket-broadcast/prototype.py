from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

from utils.logs import logger

app = FastAPI()

html = """
    <html>
        <head>
            <title>WebSocket Broadcast</title>
        </head>
        <body>
            <h1>WebSocket Broadcast</h1>
            <form onsubmit="sendMessage(event)">
                <input id="input-box" type="text" />
                <button>Send</button>
            </form>
            <hr>
            <h3>Logs</h3>
            <div id="messages"></div>
            <script>
                const uuid = self.crypto.randomUUID();
                var websocket_url = `ws://localhost:8000/ws?client_id=${uuid}`
                const ws = new WebSocket(websocket_url);
                ws.onmessage = function(event) {
                    var messages = document.getElementById("messages");
                    var message = document.createElement("p");
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                }
                function sendMessage(event) {
                    event.preventDefault();
                    var input = document.getElementById("input-box");
                    ws.send(input.value);
                    input.value = '';
                }
            </script>
        </body>
    </html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

@app.get("/", response_class=HTMLResponse)
async def get_root():
    logger.info("GET / CALLED")
    return html

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.info("GET /ws CALLED")
    await manager.connect(websocket)
    await manager.broadcast(f"Client {client_id} joined the chat!")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client [{client_id}]: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat!")