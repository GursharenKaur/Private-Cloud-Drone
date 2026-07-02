const statusText = document.getElementById("statusText");

const socket = new WebSocket(
    "ws://localhost:8000/ws/dashboard"
);

socket.onopen = () => {

    console.log("✅ Dashboard Connected");

    statusText.textContent =
        "Connected to backend.";

};

socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    console.log("📨 Received:", data);

    statusText.textContent =
        data.message;

};

socket.onerror = () => {

    statusText.textContent =
        "Connection Error.";

};

socket.onclose = () => {

    statusText.textContent =
        "Disconnected.";

};