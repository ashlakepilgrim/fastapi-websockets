from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from utils.logs import logger
from utils.websockets import ConnectionManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger.info("SERVER STARTED")
logger.info("LOADED TEMPLATES & STATIC FILES")

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    try:
        logger.info("GET / CALLED")
        logger.info("RENDERED index.html SUCCESSFULLY")
        return templates.TemplateResponse(
            request=request,
            name="index.html"
        )
    except Exception:
        logger.exception("FAILED TO RENDER INDEX PAGE")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.info("GET /ws CALLED")
    logger.info(f"ACTIVE CONNECTIONS={len(manager.active_connections)}")
    logger.info(f"AWAITING WEBSOCKET CONNECTION | client_id={client_id}")
    await manager.connect(websocket)
    logger.info(f"CLIENT {client_id} CONNECTED")
    await manager.broadcast(f"Client {client_id} joined the chat!")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"MESSAGE RECEIVED | ACTIVE CONNECTIONS={len(manager.active_connections)} | message={data}")
            await manager.broadcast(f"Client [{client_id}]: {data}")
            logger.info(f"MESSAGE BROADCASTED | ACTIVE CONNECTIONS={len(manager.active_connections)} | message={data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"CLIENT {client_id} DISCONNECTED")
        await manager.broadcast(f"Client {client_id} left the chat!")