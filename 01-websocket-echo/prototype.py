from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<html>
    <head>
        <title>WebSocket Echo</title>
    </head>
    <body>
        <h1>WebSocket Echo</h1>
        <form onsubmit="sendMessage(event)">
            <input id="input-textbox" type="text" />
            <button>Send</button>
        </form>
        <hr>
        <h2>Logs</h2>
        <ul id="messages"></ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode("SERVER: " + event.data);
                message.appendChild(content);
                messages.appendChild(message);
            }
            function sendMessage(event) {
                event.preventDefault();
                var input = document.getElementById('input-textbox');
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode("CLIENT: " + input.value);
                message.appendChild(content);
                messages.appendChild(message);
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_root():
    return html

@app.websocket("/ws")                                               # define the websocket endpoint
async def websocket_endpoint(websocket: WebSocket):                 # receive incoming websocket connection
    await websocket.accept()                                        # accept the ws connection
    while True:                                                     # start a loop
        message = await websocket.receive_text()                    # wait until the client sends me a text message
        await websocket.send_text(message)                          # send the message as soon as it is available

# javascript
# =======================
# const ws = new WebSocket("ws://localhost:8000/ws");
# ws;
# ws.onmessage = (event) => {console.log("SERVER: ", event.data)}
# ws.send("hello")