# Phase 3 - Milestone 2
# WebSocket Communication Layer

---

# Project

**Private Cloud Drone Security System**

Phase 3 focuses on enabling secure, low-latency live video streaming between a mobile device (acting as the drone camera) and the monitoring dashboard.

Before implementing WebRTC, a reliable communication channel is required for exchanging signaling messages between devices.

This milestone implements that communication layer using FastAPI WebSockets.

---

# Objective

The objective of this milestone is to establish persistent, bidirectional communication between connected clients and the FastAPI backend.

Instead of using traditional HTTP requests, WebSockets allow continuous communication over a single TCP connection.

This communication layer will later be used to exchange:

- WebRTC SDP Offers
- WebRTC SDP Answers
- ICE Candidates
- Authentication Messages
- Device Status
- Telemetry
- Heartbeat Packets

No video is transmitted during this milestone.

Only signaling communication is implemented.

---

# Why WebSockets?

HTTP follows a Request → Response model.

Example:

Browser → Server

Request

↓

Server → Browser

Response

Connection Closed

This model is unsuitable for real-time communication because the server cannot push new data whenever required.

WebSockets solve this limitation.

Once connected:

Client

⇅

Server

Both sides can send messages at any time.

This is essential for WebRTC.

---

# Architecture

                Mobile Camera
                      │
                      │
              WebSocket Client
                      │
                      ▼
        ┌──────────────────────────┐
        │      FastAPI Backend     │
        │                          │
        │   Connection Manager     │
        │   WebSocket Endpoint     │
        └──────────────────────────┘
                      │
                      │
               Dashboard Client

At this stage, the backend simply receives JSON messages and replies to the sender.

Future milestones will forward messages between clients.

---

# Folder Structure

backend/

app/

streaming/

├── manager.py

├── websocket.py

├── signaling.py

└── __init__.py

---

# Connection Manager

File:

app/streaming/manager.py

The Connection Manager is responsible for maintaining all active WebSocket connections.

Instead of storing only the websocket object, each connected client is represented using metadata.

Example:

```python
{
    "phone_001": {
        "role": "camera",
        "websocket": websocket
    }
}


---

# ✅ Current Project Status

| Phase | Status |
|--------|--------|
| Phase 1 – Backend Foundation | ✅ Completed |
| Phase 2 – REST APIs, Authentication, Database | ✅ Completed |
| Phase 3 – Camera UI | ✅ Completed |
| Phase 3 – WebSocket Communication | ✅ Completed |
| Phase 3 – Signaling Server | 🔄 Next |
| Phase 3 – Phone Camera → Dashboard Streaming | ⏳ Pending |
| Phase 3 – Secure Streaming (JWT + WSS + Authentication) | ⏳ Pending |

---

## 🚀 Next

Now comes the most exciting part of the project.

From this point onward, we will stop "echoing" messages and build a real **WebRTC signaling server**, after which we'll establish a direct peer-to-peer connection so that the **phone's camera streams live onto the dashboard**. This is where the project transitions from backend infrastructure into a real-time video streaming system.

                FastAPI Backend

           websocket.py
                 │
                 ▼
           signaling.py
                 │
                 ▼
        ConnectionManager
         ▲            ▲
         │            │
         │            │
 Camera Page      Dashboard
