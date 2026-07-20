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