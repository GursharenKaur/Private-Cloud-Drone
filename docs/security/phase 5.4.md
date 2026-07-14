# Phase 5.4 — Endpoint Authorization & Capability-Based Access Control

## Objective

After completing Phase 5.3 (Device Authentication & Authorization), the next objective was to secure every sensitive backend endpoint using authorization checks.

Authentication verifies **who** the requester is.

Authorization verifies **what** the authenticated requester is allowed to do.

This phase introduced a centralized authorization layer based on:

- Device status
- Device capabilities
- User roles
- JWT identity

This architecture ensures that even a valid authenticated device cannot perform operations outside its assigned permissions.

---

# Architecture

```

                 JWT Authentication
│
▼
Authenticated Device
│
▼
Authorization Layer
│
├── Device Active?
├── Required Capability?
├── Allowed Status?
│
▼
Protected API Endpoint

```

Every protected endpoint now passes through the authorization pipeline before business logic is executed.

---

# Authorization Components

## 1. Device Capability Enum

A centralized enumeration was introduced for every supported device permission.

File

```

backend/app/core/device_capabilities.py

```

Implementation

```python
from enum import StrEnum

class DeviceCapability(StrEnum):
    VIDEO_STREAM = "video_stream"
    VIDEO_UPLOAD = "video_upload"
    TELEMETRY = "telemetry"
    COMMANDS = "commands"
```

Using an Enum eliminates string duplication throughout the project and prevents typographical errors.

---

# Device Authorization Pipeline

The central authorization function is:

```python
authorize_device(...)
```

It performs multiple validation stages sequentially.

```

Authenticated Device
│
├── require_active_device()
│
├── require_device_status()
│
├── require_device_capability()
│
▼
Authorized Device

```

---

# Active Device Verification

Every protected endpoint first verifies that the device is enabled.

```python
require_active_device(device)
```

Validation

```

device.is_active == True

```

Rejected devices receive:

```

HTTP 403
Device is inactive

```

---

# Device Status Verification

Certain endpoints may require a specific operational state.

Example

```python
require_device_status(
    device,
    allowed_statuses=["online"]
)
```

Possible statuses

- online
- offline
- recording
- idle

---

# Capability-Based Authorization

Every device stores its supported capabilities.

Database example

```

video_stream
video_upload
telemetry
commands

```

Before executing an endpoint, the backend verifies that the requested capability exists.

Example

```python
authorize_device(
    current_device,
    capability=DeviceCapability.VIDEO_STREAM
)
```

If missing

```

HTTP 403

Device lacks required capability

```

---

# Updated Capability Validation

The authorization logic was improved to support both PostgreSQL storage formats.

Supported

```

video_stream,video_upload

```

and

```

{video_stream,video_upload}

```

The validator now normalizes capabilities before comparison.

Example

```python
required = capability.value.lower()
```

This guarantees compatibility across different database representations.

---

# Protected WebSocket Endpoint

The streaming WebSocket now performs authorization before allowing a connection.

Connection flow

```

Phone
│
▼
JWT Validation
│
▼
Active Device Check
│
▼
Capability Check
│
▼
WebSocket Accepted

```

Implementation

```python
current_device = authenticate_device_token(
    token=token,
    db=db,
)

current_device = authorize_device(
    current_device,
    capability=DeviceCapability.VIDEO_STREAM,
)
```

---

# Dashboard Authorization

Dashboard users are authenticated independently using user JWTs.

Flow

```

User Login
│
▼
JWT Validation
│
▼
User Lookup
│
▼
Dashboard Access

```

Only authenticated users may establish the dashboard WebSocket.

---

# Authorization Debugging

During development several issues were encountered.

---

## Issue 1

```

ImportError:
DeviceCapability

```

Cause

The container was loading an outdated file.

Resolution

- Updated device_capabilities.py
- Restarted backend container
- Verified container filesystem

---

## Issue 2

```

AttributeError

VIDEO_STREAM

```

Cause

Old enum values still existed.

Resolution

Updated enum

```

VIDEO_STREAM
VIDEO_UPLOAD
TELEMETRY
COMMANDS

```

---

## Issue 3

```

403 Forbidden

Device lacks required capability

```

Cause

Authorization failed because PostgreSQL returned capabilities using different formats.

Example

```

video_stream,video_upload

```

vs

```

{video_stream,video_upload}

```

Resolution

Capability normalization added before comparison.

---

## Issue 4

Container running stale code

Resolution

Verified inside Docker

```bash
docker exec -it drone_backend cat /app/app/core/device_capabilities.py
```

and

```bash
docker exec -it drone_backend grep "Required capability" ...
```

This ensured the backend was executing the latest implementation.

---

# Database Verification

Device capabilities were verified directly from PostgreSQL.

Example

```sql
SELECT
device_uuid,
capabilities
FROM devices;
```

Result

```

video_stream
video_upload
telemetry
commands

```

All registered devices were updated to the new capability model.

---

# Security Improvements

This phase introduced:

✔ Active device verification

✔ Capability-based authorization

✔ Device status validation

✔ WebSocket authorization

✔ Dashboard authorization

✔ Centralized authorization pipeline

✔ Enum-based capability management

✔ Normalized capability parsing

---

# Authorization Flow

```

Device
│
▼
Authenticate JWT
│
▼
Load Device
│
▼
Check Active
│
▼
Check Status
│
▼
Check Capability
│
▼
Endpoint Execution

```

---

# Protected Operations

Current capability mapping

| Capability | Operation |
|------------|-----------|
| VIDEO_STREAM | Live video streaming |
| VIDEO_UPLOAD | Video uploads |
| TELEMETRY | Telemetry transmission |
| COMMANDS | Command execution |

---

# Testing Performed

## Device Authentication

✔ Passed

---

## Dashboard Authentication

✔ Passed

---

## WebSocket Authentication

✔ Passed

---

## Device Capability Validation

✔ Passed

---

## Unauthorized Device Rejection

✔ Passed

Returned

```

HTTP 403

```

---

## Authorized Device Connection

✔ Passed

Device successfully connected to WebSocket.

---

## Dashboard Connection

✔ Passed

Dashboard authenticated and connected successfully.

---

## Live Streaming

✔ Passed

Authenticated camera successfully streamed video to the dashboard.

---

# Final Outcome

Phase 5.4 completed the backend authorization layer.

The server now guarantees that:

- every device is authenticated
- every device is active
- every operation is capability checked
- every WebSocket connection is authorized
- unauthorized devices are rejected before accessing protected resources

Authentication and authorization are now fully separated, making the security model modular, scalable, and suitable for future edge devices such as Raspberry Pi, Jetson Nano, ESP32, or custom drone hardware.

---

# Phase Status

**Phase 5.4 — Completed ✅**

The Drone Cloud backend now enforces capability-based authorization across protected communication channels and establishes a secure foundation for future endpoint protection and fine-grained access control.