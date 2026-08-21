from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_websocket_connection():
    with client.websocket_connect("/ws?client_id=test-client") as websocket:
        message = websocket.receive_text()
        assert message == "Client test-client joined the chat!"

def test_websocket_broadcast():
    with client.websocket_connect("/ws?client_id=client-a") as websocket_a:

        # A receives its own join message
        assert websocket_a.receive_text() == \
            "Client client-a joined the chat!"

        with client.websocket_connect("/ws?client_id=client-b") as websocket_b:

            # A gets notified that B joined
            assert websocket_a.receive_text() == \
                "Client client-b joined the chat!"

            # B gets its own join notification
            assert websocket_b.receive_text() == \
                "Client client-b joined the chat!"

            # A sends a message
            websocket_a.send_text("hello")

            # Both clients receive the broadcast
            assert websocket_a.receive_text() == \
                "Client [client-a]: hello"

            assert websocket_b.receive_text() == \
                "Client [client-a]: hello"

def test_websocket_disconnect():
    with client.websocket_connect("/ws?client_id=client-a") as websocket_a:

        # Consume A's join message
        assert websocket_a.receive_text() == \
            "Client client-a joined the chat!"

        with client.websocket_connect("/ws?client_id=client-b") as websocket_b:

            # Consume B's join messages
            assert websocket_a.receive_text() == \
                "Client client-b joined the chat!"

            assert websocket_b.receive_text() == \
                "Client client-b joined the chat!"

        # B disconnected, so A should receive the leave message
        assert websocket_a.receive_text() == \
            "Client client-b left the chat!"