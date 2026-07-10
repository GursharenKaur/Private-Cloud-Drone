# Phase 5.2 Progress Report
## Secure Device Authentication for Telemetry & Video Upload

---

# Objective

Phase 5.2 focuses on securing all device-facing APIs.

The goal is to ensure that every request coming from an edge device
(Android phone today, Raspberry Pi or Jetson Nano in the future)
is authenticated using a Device JWT instead of trusting client-supplied
device identifiers.

This establishes a secure Device → Backend trust model.

---

# Security Architecture

Current authentication flow:

Device
    │
    ▼
POST /devices/auth
    │
    ▼
Device JWT
    │
    ▼
Protected API Endpoint
    │
    ▼
get_current_device()
    │
    ▼
Authenticated Device
    │
    ▼
Business Logic
    │
    ▼
Database

The backend no longer trusts any client-supplied device identity.

Device ownership is derived exclusively from the authenticated JWT.

---

# Completed Work

## 1. Telemetry API Security

### Previous Design

Telemetry upload accepted a device identifier from the client.

Example:

```json
{
    "device_id": 7,
    "latitude": 30.73,
    "longitude": 76.77
}
```

Problem:

A malicious client could modify the device_id and impersonate another device.

---

### New Design

Telemetry upload is now protected using:

```python
current_device: Device = Depends(get_current_device)
```

The CRUD layer stores:

```python
device_id = current_device.id
```

instead of:

```python
device_id = telemetry.device_id
```

Device identity is now obtained from the JWT.

---

### Router Changes

Modified:

backend/app/api/v1/telemetry.py

Changes:

- Added get_current_device()
- Imported Device model
- Protected POST /telemetry
- Upload endpoint now authenticates devices instead of users

---

### CRUD Changes

Modified:

backend/app/crud/telemetry.py

Changes:

Old:

create_telemetry(db, telemetry)

New:

create_telemetry(db, telemetry, device)

Telemetry records are now stored using:

device.id

instead of trusting the client request.

---

### Schema Changes

Modified:

backend/app/schemas/telemetry.py

Changes:

Removed:

device_id

from:

TelemetryCreate

The client now only sends telemetry values.

The backend determines device ownership automatically.

---

### Cleanup

Removed duplicated:

- imports
- routes
- CRUD functions
- obsolete telemetry schema

Telemetry module is now clean and maintainable.

---

## 2. Video Upload Security

Video uploads are now associated with authenticated devices.

---

### Database Changes

Modified:

backend/app/models/video.py

Added:

device_id

Foreign Key:

devices.id

---

### Alembic Migration

Created migration:

add device_id to videos

Migration added:

device_id INTEGER NOT NULL

Foreign key:

videos.device_id

→ devices.id

---

### CRUD Changes

Modified:

backend/app/crud/video.py

Old:

create_video(...)

New:

create_video(
    db,
    device,
    filename,
    filepath,
    ...
)

Video ownership is stored as:

device.id

---

### API Changes

Modified:

backend/app/api/videos.py

Upload endpoint now uses:

```python
current_device: Device = Depends(get_current_device)
```

instead of anonymous uploads.

Video creation now passes:

```python
device=current_device
```

to the CRUD layer.

---

# Testing Performed

## Device Authentication

Verified:

POST /devices/auth

Returns:

- Device JWT
- Bearer Token

Successfully tested.

---

## Telemetry Upload

Tested using curl.

Request:

Authorization:

Bearer <Device JWT>

Body:

```json
{
    "latitude": 30.7333,
    "longitude": 76.7794,
    "altitude": 320.5,
    "battery_level": 87
}
```

Verified:

- JWT validation
- Device lookup
- Database insertion
- device_id assigned automatically

Successful.

---

## Video Upload

Tested using curl.

Authorization:

Bearer <Device JWT>

Multipart upload:

video=@recording.webm

Verified:

- Device authentication
- Video upload
- Database insertion
- device_id stored correctly

Database verification:

```sql
SELECT id,
       device_id,
       filename,
       uploaded_at
FROM videos;
```

Verified that uploaded video belongs to the authenticated device.

Successful.

---

# Files Modified

Telemetry

- backend/app/api/v1/telemetry.py
- backend/app/crud/telemetry.py
- backend/app/schemas/telemetry.py

Video

- backend/app/api/videos.py
- backend/app/crud/video.py
- backend/app/models/video.py

Security

- app/core/security.py

Database

- Alembic migration
- videos table

---

# Current Security Status

Completed:

✅ Device Registration

✅ Device Authentication

✅ Device JWT

✅ get_current_device()

✅ Secure Telemetry Upload

✅ Secure Video Upload

Pending:

⬜ Secure Image Upload

⬜ Secure WebSocket Authentication

⬜ Secure Device Command APIs

⬜ Device Permission / Authorization Layer

---

# Current Backend Architecture

                 Edge Device
                        │
                        ▼
                Device Authentication
                        │
                        ▼
                  Device JWT
                        │
        ┌───────────────┼───────────────┐
        │                               │
        ▼                               ▼
  Telemetry API                  Video Upload API
        │                               │
        ▼                               ▼
 get_current_device()          get_current_device()
        │                               │
        ▼                               ▼
 telemetry.device_id          videos.device_id

All device-generated resources are now linked to authenticated devices.

---

# Next Phase

Continue Phase 5.2 by securing:

1. Image Upload API
2. WebSocket Authentication
3. Device Command APIs

The same security pattern established for Telemetry and Video Upload will be applied to all remaining device-facing endpoints.

This ensures a consistent authentication model across the entire backend.

---