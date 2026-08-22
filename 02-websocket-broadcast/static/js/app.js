const uuid = Date.now().toString(36) + Math.random().toString(36).slice(2);
const websocketUrl = `ws://${window.location.host}/ws?client_id=${uuid}`;

const ws = new WebSocket(websocketUrl);

const messages = document.getElementById("messages");
const members = document.getElementById("members");
const memberCount = document.getElementById("member-count");
const form = document.getElementById("message-form");
const input = document.getElementById("input-box");

const activeMembers = new Map();

function getTime() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
}

function addMessage(text, type = "") {
    const message = document.createElement("div");
    message.className = `message ${type}`;

    const time = document.createElement("span");
    time.className = "message-time";
    time.textContent = getTime();

    const content = document.createElement("span");
    content.className = "message-text";
    content.textContent = text;

    message.appendChild(time);
    message.appendChild(content);

    messages.appendChild(message);

    scrollToBottom();
}

function addMember(id) {
    if (!id) return;

    activeMembers.set(id, id);
    renderMembers();
}

function removeMember(id) {
    if (!id) return;

    activeMembers.delete(id);
    renderMembers();
}

function renderMembers() {
    members.innerHTML = "";

    for (const id of activeMembers.keys()) {
        const member = document.createElement("div");
        member.className = "member";

        if (id === uuid) {
            member.classList.add("you");
        }

        const dot = document.createElement("span");
        dot.className = "member-dot";

        const label = document.createElement("span");
        label.className = "member-label";

        label.textContent =
            id === uuid
                ? "you"
                : id;

        member.appendChild(dot);
        member.appendChild(label);

        if (id === uuid) {
            const you = document.createElement("span");
            you.className = "you-label";
            you.textContent = "you";
            member.appendChild(you);
        }

        members.appendChild(member);
    }

    memberCount.textContent = activeMembers.size;
}

ws.onopen = () => {
    addMember(uuid);
    addMessage("connected to server", "system-message");
};

ws.onmessage = (event) => {
    const data = event.data;

    /*
     * Server messages:
     *
     * Client <uuid> joined the chat!
     * Client [<uuid>]: hello
     * Client <uuid> left the chat!
     */

    const joined = data.match(
        /^Client ([a-z0-9]+) joined the chat!$/
    );

    if (joined) {
        const id = joined[1];

        addMember(id);
        addMessage(data, "join-message");

        return;
    }

    const left = data.match(
        /^Client ([a-z0-9]+) left the chat!$/
    );

    if (left) {
        const id = left[1];

        removeMember(id);
        addMessage(data, "leave-message");

        return;
    }

    const chat = data.match(
        /^Client \[([a-z0-9]+)\]: (.*)$/
    );

    if (chat) {
        const id = chat[1];
        const text = chat[2];

        addMember(id);

        const message = document.createElement("div");
        message.className = "message";

        const time = document.createElement("span");
        time.className = "message-time";
        time.textContent = getTime();

        const client = document.createElement("span");
        client.className = "message-client";
        client.textContent =
            id === uuid ? "you" : id;

        const separator = document.createTextNode(": ");

        const content = document.createElement("span");
        content.className = "message-text";
        content.textContent = text;

        message.appendChild(time);
        message.appendChild(client);
        message.appendChild(separator);
        message.appendChild(content);

        messages.appendChild(message);

        scrollToBottom();

        return;
    }

    addMessage(data);
};

ws.onclose = () => {
    addMessage("connection closed", "leave-message");
};

ws.onerror = () => {
    addMessage("websocket connection error", "leave-message");
};

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const text = input.value.trim();

    if (!text || ws.readyState !== WebSocket.OPEN) {
        return;
    }

    ws.send(text);

    input.value = "";
    input.focus();
});

document.addEventListener("click", () => {
    input.focus();
});

input.focus();