from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "WebSocket Broadcast" in response.text