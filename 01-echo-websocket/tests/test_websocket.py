from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_websocket_echo():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("hello")
        message = websocket.receive_text()
        assert message == "hello"

def test_websocket_echo_multiple_messages():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("hello")
        assert websocket.receive_text() == "hello"
        websocket.send_text("world")
        assert websocket.receive_text() == "world"
        websocket.send_text("bhai")
        assert websocket.receive_text() == "bhai"