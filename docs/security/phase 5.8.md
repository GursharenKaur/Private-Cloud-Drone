# Phase 5.8.1 — User Login Rate Limiting

## Overview

Phase 5.8.1 introduces abuse protection for the user authentication system by implementing persistent failed-login tracking and temporary account lockouts.

The primary objective of this phase is to protect the user login endpoint from brute-force password attacks while preserving the existing authentication and authorization architecture.

This implementation extends the existing security architecture incrementally and does not replace or redesign the current JWT-based user authentication flow.

---

## Objectives

The objectives of Phase 5.8.1 are:

- Prevent repeated brute-force password attempts.
- Track consecutive failed login attempts.
- Temporarily lock authentication attempts after a configurable threshold.
- Automatically remove expired lockouts.
- Reset failure tracking after successful authentication.
- Store login attempt state persistently in PostgreSQL.
- Integrate lockout events with the existing centralized security audit logging system.
- Keep rate-limiting logic outside API routers.
- Preserve the existing JWT authentication architecture.

---

## Protected Endpoint

The following endpoint is protected by the login rate-limiting mechanism:

```text
POST /auth/login

# Phase 5.8.2 — Device Authentication Rate Limiting

## Overview

Phase 5.8.2 introduces rate limiting and temporary lockout protection for device authentication.

The purpose of this phase is to protect the device authentication endpoint:

`POST /devices/auth`

against repeated brute-force attempts targeting device credentials, particularly the `device_secret`.

This implementation extends the existing security architecture without replacing or redesigning the existing device authentication mechanism.

The existing device identity, authentication, JWT generation, capability authorization, and endpoint authorization mechanisms remain unchanged.

---

## Security Objective

The main objectives of Phase 5.8.2 are:

- Prevent brute-force attacks against device secrets.
- Track consecutive failed authentication attempts per device UUID.
- Temporarily block authentication after repeated failures.
- Automatically clear expired lockouts.
- Reset failure tracking after successful authentication.
- Integrate device authentication lockouts with the existing audit logging system.
- Preserve the existing device JWT authentication architecture.

---

## Protected Endpoint

The following endpoint is protected:

`POST /devices/auth`

This endpoint accepts:

- `device_uuid`
- `device_secret`

Before Phase 5.8.2, invalid credentials resulted in:

`401 Unauthorized`

Phase 5.8.2 adds abuse protection around this existing authentication flow.

---

## Architecture

The implementation follows the existing layered project architecture.

```text
Device / Edge Device
        |
        v
POST /devices/auth
        |
        v
Device Authentication Lock Check
        |
        +---- Locked ----> 429 Too Many Requests
        |
        v
Existing authenticate_device()
        |
        +---- Invalid Credentials
        |           |
        |           v
        |   Record Failed Attempt
        |           |
        |           v
        |   Temporary Lockout if Threshold Reached
        |           |
        |           v
        |      401 Unauthorized
        |
        v
Successful Authentication
        |
        v
Reset Authentication Failure Counter
        |
        v
Existing Device JWT Generation
        |
        v
200 OK