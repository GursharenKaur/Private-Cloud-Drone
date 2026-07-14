# Phase 5.3 — Secure WebSocket Authentication & Protected Video Upload

## Objective

The goal of Phase 5.3 was to secure all real-time communication between devices and the backend by introducing authentication for WebSocket connections and ensuring that only authenticated users can upload recorded videos.

This phase completed the security layer around live streaming and recording while maintaining the separation between **User Identity** and **Device Identity** introduced in Phase 5.2.

---

# Architecture

```
                    +----------------------+
                    |      Dashboard       |
                    |   (Authenticated)    |
                    +----------+-----------+
                               |
                      User JWT (Bearer)
                               |
                               ▼
                    Secure WebSocket
                               ▲
                               |
                     Device JWT Authentication
                               |
                    +----------+-----------+
                    |     Camera Device     |
                    |   (Phone / Raspberry) |
                    +-----------------------+

```

---

# Authentication Model

Two independent identities now exist in the system.

## 1. User Authentication

Used by:

- Dashboard
- Admin APIs
- Video Upload
- Future Management APIs

JWT Payload

```json
{
    "sub": "2",
    "type": "user",
    "email": "gks@gmail.com",
    "role": "admin",
    "exp": ...
}
```

---

## 2. Device Authentication

Used by:

- Camera
- Raspberry Pi
- Drone
- Future Edge Devices

JWT Payload

```json
{
    "sub": "<device_uuid>",
    "type": "device",
    "exp": ...
}
```

---

# Major Changes

---

## 1. Generic WebSocket Authentication

Previously

```
Anyone could connect.

ws://server/ws/phone_001
```

Now

```
ws://server/ws/phone_001?token=<device_jwt>

ws://server/ws/dashboard?token=<user_jwt>
```

Every websocket connection now requires authentication.

---

## 2. Authentication Flow

When a websocket connects

```
Client
      │
      ▼
Extract JWT
      │
      ▼
Is client dashboard?
      │
      ├──────────────► YES
      │                   │
      │                   ▼
      │          authenticate_user_token()
      │
      └──────────────► NO
                          │
                          ▼
               authenticate_device_token()
```

If authentication fails

```
401 Unauthorized
```

Connection is rejected immediately.

---

## 3. Connection Manager Improvements

The ConnectionManager now stores

```python
{
    client_id: {
        "role": "...",
        "websocket": websocket,
        "device": device
    }
}
```

Each active connection now maintains

- websocket
- role
- authenticated device (if applicable)

---

## 4. Dashboard Authentication

Dashboard login flow

```
POST /auth/login

↓

User JWT

↓

Store in LocalStorage

↓

Open authenticated websocket
```

Dashboard JavaScript now

- authenticates automatically
- stores access token
- uses token for websocket
- uses token for uploads

---

## 5. Camera Authentication

Camera now performs

```
POST /devices/auth

↓

Device JWT

↓

Connect websocket

/ws/phone_001?token=<device_jwt>
```

Only registered devices can connect.

---

# Protected Video Upload

Previously

```
POST /videos/upload

No Authentication
```

Now

```
POST /videos/upload

Authorization:
Bearer <user_jwt>

device_uuid

video.webm
```

The upload endpoint now requires

- authenticated user
- device UUID
- uploaded recording

---

# Upload Flow

```
Dashboard
      │
      │ Record Stream
      ▼
recording.webm
      │
      ▼
POST /videos/upload
      │
      ├── User JWT
      ├── Device UUID
      └── Video File
      ▼
Backend
      │
Authenticate User
      │
Find Device
      │
Store File
      │
Create Database Record
      ▼
200 OK
```

---

# Backend Upload Logic

Upload endpoint now performs

```
Authenticate User

↓

Read device_uuid

↓

Find Device

↓

Save Video

↓

Create Database Entry

↓

Return Success
```

The database relationship remains

```
Device

↓

Videos
```

instead of

```
User

↓

Videos
```

This preserves the correct ownership model because videos originate from devices.

---

# Device Ownership

Every uploaded recording is still linked to the originating device.

```
Device

↓

Video 1

Video 2

Video 3
```

The dashboard merely uploads the file on behalf of the authenticated user.

---

# Security Improvements

## Before Phase 5.3

✔ Device Registration

✔ Device Authentication API

❌ Unauthenticated WebSockets

❌ Unauthenticated Uploads

---

## After Phase 5.3

✔ Device Registration

✔ Device Authentication

✔ User Authentication

✔ Secure Dashboard WebSocket

✔ Secure Camera WebSocket

✔ Protected Upload Endpoint

✔ Device Ownership Verification

✔ JWT Validation

✔ Connection Rejection on Invalid Token

---

# Problems Encountered

During implementation several issues were resolved.

---

## 1. Dashboard WebSocket

Problem

```
403 Forbidden
```

Cause

Dashboard JWT lacked the required

```
"type": "user"
```

claim.

Solution

Updated JWT creation and validation.

---

## 2. Upload Authentication

Problem

```
401 Unauthorized
```

Cause

Dashboard upload request did not include Authorization header.

Solution

Stored JWT in LocalStorage and added

```
Authorization:
Bearer <token>
```

to upload requests.

---

## 3. Invalid Device Token

Problem

```
Invalid device token
```

Cause

Upload endpoint authenticated uploads using

```
get_current_device()
```

even though uploads originate from the dashboard.

Solution

Endpoint now authenticates the user and resolves the device using the provided `device_uuid`.

---

## 4. Network Access

Problem

Phone could not reach

```
10.148.x.x
```

Cause

Incorrect network IP.

Solution

Used the active Wi-Fi interface IP

```
172.31.233.129
```

for cross-device testing.

---

## 5. HTTPS Camera Access

Problem

Safari reported

```
enumerateDevices
```

errors.

Cause

Camera APIs require HTTPS.

Solution

Used

```
https://172.31.233.129/camera
```

through Nginx.

---

# Final End-to-End Flow

```
Phone

↓

Authenticate Device

↓

Secure WebSocket

↓

Dashboard

↓

Authenticate User

↓

Secure WebSocket

↓

Receive Live Stream

↓

Record WebRTC

↓

Upload Recording

↓

Authenticate User

↓

Resolve Device

↓

Save Recording

↓

Create Video Entry

↓

200 OK
```

---

# Files Modified

Backend

- `backend/app/core/security.py`
- `backend/app/streaming/websocket.py`
- `backend/app/streaming/manager.py`
- `backend/app/api/videos.py`

Frontend

- `frontend/dashboard/dashboard.js`
- `frontend/camera/media.js`

---

# Validation Performed

Successfully verified

- Dashboard authentication
- Device authentication
- Secure WebSocket connections
- User JWT validation
- Device JWT validation
- Dashboard login
- Camera login
- Live WebRTC streaming
- Recording functionality
- Protected upload endpoint
- Device ownership association
- Successful video upload (`200 OK`)

---

# Phase 5.3 Status

## ✅ Completed

Phase 5.3 successfully established secure communication between users, devices, and the backend by introducing authenticated WebSocket connections, protected video uploads, and correct device ownership while preserving the project's scalable device-centric architecture.