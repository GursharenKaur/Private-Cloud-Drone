# Phase 3 – WebRTC Signaling & Live Streaming

## Objective

The objective of Phase 3 was to establish a complete WebRTC signaling mechanism for streaming a live camera feed from an Android device to the Drone Monitoring Dashboard. This phase focused on creating the signaling infrastructure, implementing WebRTC peer connections, exchanging SDP Offers and Answers, and beginning ICE candidate exchange.

---

# Architecture Overview

```
Android Camera
      │
      │
  WebRTC Offer
      │
      ▼
FastAPI WebSocket Signaling Server
      │
      ▼
Dashboard (Laptop Browser)
      │
      │
 WebRTC Answer
      │
      ▼
Android Camera
```

The FastAPI backend acts only as a signaling server. Video packets are never sent through the backend. Once signaling completes, media flows directly between the Android device and the dashboard using WebRTC.

---

# Components Developed

## 1. Camera Console

Created a dedicated camera page responsible for:

- Accessing the mobile camera
- Creating the WebRTC Peer Connection
- Capturing local video
- Creating SDP Offer
- Sending Offer to the dashboard
- Receiving SDP Answer
- Generating ICE Candidates

### Files

```
frontend/
└── camera/
    ├── index.html
    ├── camera.css
    ├── camera.js
    ├── media.js
    └── webrtc.js
```

---

## 2. Dashboard

Created a monitoring dashboard responsible for:

- Receiving SDP Offer
- Creating Peer Connection
- Receiving remote video track
- Creating SDP Answer
- Sending Answer back
- Receiving ICE Candidates

### Files

```
frontend/
└── dashboard/
    ├── index.html
    ├── dashboard.css
    ├── dashboard.js
    └── webrtc.js
```

---

## 3. FastAPI Signaling Server

Implemented WebSocket signaling using FastAPI.

### WebSocket Endpoints

```
/ws/phone_001
/ws/dashboard
```

Responsibilities:

- Register connected peers
- Relay SDP Offers
- Relay SDP Answers
- Relay ICE Candidates
- Maintain signaling connections

---

# Features Implemented

## Camera Side

### Camera Initialization

Implemented media access using:

```javascript
navigator.mediaDevices.getUserMedia()
```

Features:

- Local video preview
- Camera permission handling
- Camera start/stop controls

---

### RTCPeerConnection

Implemented Peer Connection using Google's public STUN server.

```javascript
new RTCPeerConnection({
    iceServers: [
        {
            urls: "stun:stun.l.google.com:19302"
        }
    ]
});
```

---

### Local Media Tracks

Added camera tracks to Peer Connection.

```
Camera Stream
      │
      ▼
RTCPeerConnection
```

Verified:

- Video track attached
- Sender count verified

---

### SDP Offer Creation

Implemented:

- createOffer()
- setLocalDescription()

Offer successfully generated and transmitted to the dashboard.

---

### Receiving SDP Answer

Implemented:

```
setRemoteDescription(answer)
```

Phone successfully accepts the dashboard's SDP Answer.

---

### ICE Candidate Generation

Implemented:

```javascript
peerConnection.onicecandidate
```

Verified generation of:

- Host Candidates
- Server Reflexive Candidates (srflx)
- TCP Candidates

Successfully transmitted candidates to the backend.

---

# Dashboard Side

## Peer Connection

Created Peer Connection.

Implemented:

```javascript
RTCPeerConnection()
```

---

## Remote Video

Implemented:

```javascript
peerConnection.ontrack
```

Remote video stream is assigned to:

```javascript
remoteVideo.srcObject
```

---

## Offer Handling

Dashboard receives Offer through WebSocket.

Flow:

```
Offer Received

↓

setRemoteDescription()

↓

Remote Description Set
```

---

## SDP Answer

Dashboard successfully:

```
createAnswer()

↓

setLocalDescription()

↓

Send Answer
```

Verified through backend logs.

---

## ICE Candidate Reception

Implemented:

```
addIceCandidate()
```

Dashboard is prepared to receive candidates from the Android device.

---

# WebSocket Signaling Flow

```
Android

↓

Offer

↓

FastAPI

↓

Dashboard

↓

Answer

↓

FastAPI

↓

Android
```

Verified successfully.

---

# SDP Negotiation

Completed negotiation flow:

```
Phone

↓

createOffer()

↓

Dashboard

↓

setRemoteDescription()

↓

createAnswer()

↓

setLocalDescription()

↓

Phone

↓

setRemoteDescription(answer)
```

Status:

✅ Completed

---

# ICE Candidate Progress

Completed:

```
Phone
      │
Generate ICE
      │
      ▼
Backend
      │
      ▼
Dashboard
```

Verified in backend logs.

Example candidates observed:

- Host Candidate
- Server Reflexive Candidate
- TCP Candidate

---

# Backend Verification

Successfully verified:

- Camera WebSocket connection
- Dashboard WebSocket connection
- SDP Offer relay
- SDP Answer relay
- ICE Candidate relay

Backend logs confirmed successful signaling.

---

# Current Project Status

## Completed

- HTTPS configuration
- Nginx Reverse Proxy
- FastAPI Backend
- WebSocket Signaling
- Camera Module
- Dashboard Module
- Local Camera Access
- Peer Connection Creation
- SDP Offer
- SDP Answer
- Phone ICE Candidate Generation
- ICE Candidate Transmission
- Dashboard ICE Candidate Reception

---

# Remaining Work

The remaining tasks before live video streaming are:

1. Generate ICE Candidates on Dashboard
2. Send Dashboard ICE Candidates to Phone
3. Receive Dashboard ICE Candidates on Phone
4. Add Remote ICE Candidates on Phone
5. Complete ICE Connectivity
6. Establish Peer-to-Peer Media Connection
7. Display Live Android Camera Feed on Dashboard

---

# Files Created / Modified

## Backend

```
app/
└── streaming/
    ├── manager.py
    ├── signaling.py
    └── websocket.py
```

---

## Frontend

### Camera

```
camera/
├── index.html
├── camera.css
├── camera.js
├── media.js
└── webrtc.js
```

---

### Dashboard

```
dashboard/
├── index.html
├── dashboard.css
├── dashboard.js
└── webrtc.js
```

---

# Major Milestones Achieved

- Successfully established WebSocket signaling between Android device and dashboard.
- Implemented WebRTC Peer Connections on both devices.
- Completed SDP Offer/Answer negotiation.
- Verified camera access over HTTPS.
- Generated and transmitted ICE Candidates from the Android device.
- Prepared dashboard for ICE candidate processing.
- Established the foundation required for peer-to-peer live video streaming.

---

# Next Phase

The next phase will complete bidirectional ICE candidate exchange between the Android device and the dashboard, allowing the WebRTC connection to become fully established and enabling real-time live camera streaming directly onto the monitoring dashboard.