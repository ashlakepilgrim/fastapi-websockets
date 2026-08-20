from fastapi import FastAPI, WebSocket, HTTPException, status, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from utils.logger import logger

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger.info("SERVER STARTED")
logger.info("LOADED TEMPLATES & STATIC FILES")

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

@app.websocket("/ws")                                                   # define the websocket endpoint
async def websocket_endpoint(websocket: WebSocket):                     # rece;ive incoming websocket connection
    logger.info("GET /ws CALLED")
    await websocket.accept()                                            # accept the ws connection
    try:
        logger.info("WEBSOCKET CONNECTION ESTABLISHED SUCCESSFULLY")
        while True:                                                     # start a loop
            message = await websocket.receive_text()                    # wait until the client sends me a text message
            logger.info("MESSAGE RECEIVED: %s", message)
            await websocket.send_text(message)                          # send the message as soon as it is available
            logger.info("MESSAGE SENT: %s", message)
    except WebSocketDisconnect:
        logger.info("WEBSOCKET CLIENT DISCONNECTED")