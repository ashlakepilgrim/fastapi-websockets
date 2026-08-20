const ws = new WebSocket("ws://localhost:8000/ws");

const form = document.getElementById("message-form");
const input = document.getElementById("input-textbox");
const messages = document.getElementById("messages");

ws.onmessage = function(event) {
    const message = document.createElement("div");
    message.className = "message server";
    message.textContent = "SERVER: " + event.data;
    messages.appendChild(message);
};

form.onsubmit = function(event) {
    event.preventDefault();
    const text = input.value;
    if (text === "") {
        return;
    }
    const message = document.createElement("div");
    message.className = "message client";
    message.textContent = "CLIENT: " + text;
    messages.appendChild(message);
    ws.send(text);
    input.value = "";
    input.focus();
};