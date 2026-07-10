# Phase 5.1 – Device Registration & Authentication

## Overview

This phase introduces a complete authentication system for edge devices. The backend now supports secure device registration, device authentication using UUID and secret, and JWT-based identity for all future device communication.

The authentication system is designed around a generic **Device** abstraction rather than a phone-specific implementation. This ensures the backend can support Android phones, Raspberry Pi, Jetson Nano, ESP32, drones, and future edge devices without architectural changes.

---

# Architecture

```
Administrator
      │
      ▼
Register Device
      │
      ▼
Backend Generates UUID
      │
      ▼
Backend Generates Device Secret
      │
      ▼
Hash Secret (bcrypt)
      │
      ▼
Store Device
      │
      ▼
Return Secret Once
      │
      ▼
Device Authentication
      │
      ▼
Verify UUID + Secret
      │
      ▼
Issue Device JWT
      │
      ▼
Protected Device APIs
```

---

# Completed Features

## 1. Device Registration

Implemented:

- Backend-generated UUID using `uuid.uuid4()`
- Cryptographically secure device secret using Python's `secrets` module
- Secret hashing using bcrypt
- Plaintext secret returned exactly once
- Secret never stored in plaintext
- Device registration protected by authenticated user
- Registration response improved with device information

Registration Response:

```json
{
    "device_uuid": "...",
    "device_name": "...",
    "device_type": "...",
    "device_secret": "...",
    "message": "Device registered successfully. Save the device secret securely. It will not be shown again."
}
```

---

## 2. Device Capabilities

Registration now supports explicit capabilities.

Example:

```text
video,telemetry,commands
```

Capabilities are now part of the API contract instead of relying on database defaults.

---

## 3. Secure Secret Storage

The backend stores only:

```
secret_hash
```

using bcrypt.

The plaintext secret is never persisted in PostgreSQL.

---

## 4. Device Authentication

Implemented endpoint:

```
POST /devices/auth
```

Authentication Flow:

```
Device
    │
    ▼
Send UUID
Send Secret
    │
    ▼
Find Device
    │
    ▼
Verify bcrypt Hash
    │
    ▼
Check Device Active
    │
    ▼
Generate JWT
```

Response:

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

## 5. JWT Improvements

Originally the JWT contained:

```json
{
    "sub": "5"
}
```

where `5` was the database primary key.

This was refactored.

Current JWT:

```json
{
    "sub": "<device_uuid>",
    "type": "device"
}
```

Example:

```json
{
    "sub": "a84755f9-dbfc-4718-931a-55e892e7c5a3",
    "type": "device"
}
```

Using `device_uuid` instead of the database ID keeps the authentication layer aligned with the overall device architecture and avoids exposing internal database identifiers.

---

## 6. Device Authentication Dependency

Implemented:

```
get_current_device()
```

Responsibilities:

- Decode JWT
- Verify token type is `device`
- Extract device UUID
- Query device from database
- Verify device exists
- Verify device is active
- Return authenticated Device object

This mirrors the existing `get_current_user()` dependency for users.

---

## 7. Temporary Verification Endpoint

Implemented:

```
GET /devices/me
```

Purpose:

- Verify device JWT
- Verify dependency injection
- Verify authenticated device retrieval

This endpoint was introduced solely for testing the authentication pipeline.

---

# Files Modified

## API

```
backend/app/api/v1/devices.py
```

Changes:

- Added `POST /devices/auth`
- Added `GET /devices/me`
- Updated registration endpoint

---

## CRUD

```
backend/app/crud/device.py
```

Changes:

- Device registration
- Secret generation
- Secret hashing
- Device authentication
- JWT creation

---

## Schemas

```
backend/app/schemas/device.py
```

Added:

- DeviceAuthRequest
- DeviceAuthResponse

Updated:

- DeviceRegistrationResponse
- DeviceCreate

---

## Security

```
backend/app/core/security.py
```

Added:

- get_current_device()

---

# Security Features Implemented

- Backend-controlled device identity
- UUID-based authentication
- Cryptographically secure secrets
- bcrypt hashing
- JWT authentication
- Active device validation
- Generic device architecture
- One-time secret provisioning

---

# Testing Completed

Successfully verified:

- Device registration
- PostgreSQL storage
- Secret hashing
- UUID generation
- Device authentication
- JWT issuance
- JWT payload uses device UUID

---

# Current Status

Completed:

- Device Registration
- Device Authentication
- Device JWT Generation
- get_current_device()

Pending:

- Swagger/OpenAPI support for separate user and device authentication flows
- Full verification of `GET /devices/me`
- Protect telemetry endpoints
- Protect video upload endpoints
- Protect WebSocket communication
- Continue remaining Phase 5 security implementation

---

# Next Phase

The next work item is to separate user and device authentication schemes in Swagger/OpenAPI, complete end-to-end verification of `get_current_device()`, and begin securing device APIs using `Depends(get_current_device)`.
