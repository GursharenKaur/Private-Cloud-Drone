# Phase 5.4 — Endpoint Authorization & Capability-Based Access Control

## Objective

After completing **Phase 5.3 (Device Authentication & Authorization)**, the next objective was to secure every sensitive backend endpoint using authorization checks.

Authentication verifies **who** the requester is.

Authorization verifies **what** the authenticated requester is allowed to do.

This phase introduced a centralized authorization framework that is now enforced across both **REST APIs** and **WebSocket connections**.

The authorization framework validates:

- Device active status
- Device operational status
- Device capabilities
- User authentication
- JWT identity

By centralizing authorization logic, every protected endpoint now follows the same security pipeline, reducing duplicated code and ensuring consistent access control throughout the backend.

---

# Architecture

```
                 JWT Authentication
                        │
                        ▼
            Authenticated User / Device
                        │
                        ▼
             Central Authorization Layer
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   Device Active?   Device Status?   Required Capability?
          │             │             │
          └─────────────┼─────────────┘
                        ▼
              Protected REST Endpoint
                 or WebSocket Route
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
        ▼
require_active_device()
        │
        ▼
require_device_status()
        │
        ▼
require_device_capability()
        │
        ▼
Authorized Device
```

This centralized design ensures that every protected endpoint follows identical authorization rules.

---

# Endpoint Authorization Strategy

Phase 5.4 extended authorization beyond WebSocket connections.

Every protected REST endpoint now invokes the centralized authorization function before executing business logic.

Protected endpoints include:

| Endpoint | Required Capability |
|----------|---------------------|
| POST /videos/upload | VIDEO_UPLOAD |
| POST /images/upload | VIDEO_UPLOAD |
| POST /telemetry | TELEMETRY |
| WebSocket `/ws/{client}` | VIDEO_STREAM |

Dashboard endpoints continue to require authenticated user JWTs.

---

# Active Device Verification

Every protected endpoint first verifies that the device is active.

```python
require_active_device(device)
```

Validation

```
device.is_active == True
```

Rejected devices receive

```
HTTP 403

Device is inactive
```

---

# Device Status Verification

Certain endpoints may require a specific operational status.

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

Every registered device stores its supported capabilities.

Example

```
video_stream
video_upload
telemetry
commands
```

Before executing protected operations, the backend verifies that the requested capability exists.

Example

```python
authorize_device(
    current_device,
    capability=DeviceCapability.VIDEO_STREAM,
)
```

If the capability is missing

```
HTTP 403

Device lacks required capability
```

---

# Updated Capability Validation

Capability validation was enhanced to support multiple PostgreSQL storage formats.

Supported formats

```
video_stream,video_upload
```

and

```
{video_stream,video_upload}
```

Capabilities are normalized before comparison.

Example

```python
required = capability.value.lower()
```

This guarantees compatibility across different database representations.

---

# Protected Communication Channels

## WebSocket Streaming

Before a camera device can establish a WebSocket connection, it passes through the authorization pipeline.

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

## REST API Protection

Every device-facing REST endpoint now performs authorization before executing endpoint logic.

General flow

```
Device Request
        │
        ▼
JWT Authentication
        │
        ▼
authorize_device()
        │
        ▼
Business Logic
```

This provides identical authorization behavior across both REST APIs and WebSocket communication.

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

Only authenticated users may establish the dashboard WebSocket or access protected dashboard APIs.

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

The Docker container was loading an outdated version of the file.

Resolution

- Updated `device_capabilities.py`
- Restarted backend container
- Verified container filesystem

---

## Issue 2

```
AttributeError

VIDEO_STREAM
```

Cause

The backend was using an outdated enum definition.

Resolution

Updated the enum to

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

PostgreSQL stored capabilities using different formats.

Examples

```
video_stream,video_upload
```

vs

```
{video_stream,video_upload}
```

Resolution

Capability normalization was introduced before comparison.

---

## Issue 4

Docker Container Running Stale Code

Resolution

Verified the actual code inside the running container using

```bash
docker exec -it drone_backend cat /app/app/core/device_capabilities.py
```

and

```bash
docker exec -it drone_backend grep "Required capability" /app/app/core/security.py
```

This confirmed the backend was executing the latest implementation.

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

All registered devices were successfully updated to the new capability model.

---

# Security Improvements

This phase introduced

✔ Centralized authorization pipeline

✔ Capability-based REST API protection

✔ Capability-based WebSocket protection

✔ Active device verification

✔ Device status validation

✔ Enum-based capability management

✔ Normalized capability parsing

✔ Shared authorization framework reused across the backend

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

| Endpoint | Authentication | Authorization |
|-----------|----------------|---------------|
| POST /videos/upload | Device JWT | VIDEO_UPLOAD |
| POST /images/upload | Device JWT | VIDEO_UPLOAD |
| POST /telemetry | Device JWT | TELEMETRY |
| GET /telemetry | User JWT | Authenticated User |
| PUT /telemetry | User JWT | Authenticated User |
| DELETE /telemetry | User JWT | Authenticated User |
| Camera WebSocket | Device JWT | VIDEO_STREAM |
| Dashboard WebSocket | User JWT | Authenticated User |

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

## Video Upload Authorization

✔ Passed

Authorized devices with the `VIDEO_UPLOAD` capability successfully uploaded videos.

---

## Image Upload Authorization

✔ Passed

Authorized devices successfully uploaded images.

---

## Telemetry Authorization

✔ Passed

Devices with the `TELEMETRY` capability successfully submitted telemetry.

---

## REST Endpoint Authorization

✔ Passed

Every protected REST endpoint now executes centralized authorization before business logic.

---

## Unauthorized Device Rejection

✔ Passed

Returned

```
HTTP 403
```

for devices lacking the required capability.

---

## Authorized Device Connection

✔ Passed

Authorized devices successfully connected to the protected WebSocket endpoint.

---

## Dashboard Connection

✔ Passed

Dashboard authenticated and connected successfully.

---

## Live Streaming

✔ Passed

Authenticated camera successfully streamed live video to the dashboard.

---

# Final Outcome

Phase 5.4 completed the centralized authorization layer for the Drone Cloud backend.

Every protected communication channel now passes through a shared authorization pipeline before executing application logic.

The backend now guarantees that

- every device is authenticated using JWTs
- every device is verified to be active
- device status can be validated when required
- every protected REST endpoint enforces capability-based authorization
- every WebSocket connection enforces capability-based authorization
- unauthorized devices are rejected before accessing protected resources
- authorization logic is centralized, reusable, and consistent throughout the backend

By separating authentication from authorization, the backend now follows a layered security architecture that is easier to maintain, extend, and scale for future edge devices such as Raspberry Pi, Jetson Nano, ESP32, or custom drone hardware.

---

# Phase Status

**Phase 5.4 — Completed ✅**

## Deliverables

- Centralized authorization framework
- Device capability enumeration
- Active device validation
- Device status validation
- Capability-based REST API protection
- Capability-based WebSocket protection
- Shared authorization utilities
- Comprehensive endpoint authorization testing