# Phase 2 Documentation

## Overview

Phase 2 focused on developing the backend REST APIs for the DroneCloud application. The primary objective was to build secure APIs for user management, device management, and telemetry management using FastAPI, SQLAlchemy, and PostgreSQL. All protected endpoints require JWT-based authentication.

---

# Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose
- Pydantic
- JWT Authentication
- Swagger UI

---

# Modules Implemented

## 1. Authentication Module

Responsible for authenticating users and generating JWT access tokens.

### APIs

| Method | Endpoint | Role |
|---------|----------|------|
| POST | `/auth/login` | Authenticates a user and returns a JWT access token. |

**Database Interaction**

- Reads user credentials from the `users` table.
- Verifies the hashed password.
- Generates a JWT token for authenticated requests.

---

## 2. User Management Module

Responsible for managing user information and profile access.

### APIs

| Method | Endpoint | Role |
|---------|----------|------|
| GET | `/users/` | Retrieves all registered users. |
| POST | `/users/` | Creates a new user account. |
| GET | `/users/me` | Returns the currently authenticated user's profile. |
| GET | `/users/admin` | Returns the admin dashboard information (Admin only). |

**Database Interaction**

- Inserts new records into the `users` table.
- Retrieves user records.
- Validates user roles before granting admin access.

---

## 3. Device Management Module

Responsible for maintaining all registered drones/devices.

### APIs

| Method | Endpoint | Role |
|---------|----------|------|
| GET | `/devices/` | Retrieves all registered devices. |
| POST | `/devices/` | Registers a new device. |
| GET | `/devices/{device_id}` | Retrieves details of a specific device. |
| DELETE | `/devices/{device_id}` | Deletes a device from the database. |
| PATCH | `/devices/{device_id}/status` | Updates the operational status of a device. |
| GET | `/devices/stats` | Returns overall device statistics. |

**Database Interaction**

- Inserts new devices into the `devices` table.
- Reads device information.
- Updates device status.
- Deletes device records.
- Generates statistics using existing device records.

---

## 4. Telemetry Management Module

Responsible for storing and managing telemetry received from drones.

### APIs

| Method | Endpoint | Role |
|---------|----------|------|
| GET | `/telemetry/` | Retrieves all telemetry records. |
| POST | `/telemetry/` | Stores new telemetry received from a drone. |
| GET | `/telemetry/device/{device_id}` | Retrieves all telemetry records for a specific device. |
| GET | `/telemetry/device/{device_id}/latest` | Retrieves the latest telemetry record of a device. |
| PUT | `/telemetry/{telemetry_id}` | Updates an existing telemetry record. |
| DELETE | `/telemetry/{telemetry_id}` | Deletes a telemetry record. |

**Database Interaction**

- Inserts telemetry into the `telemetry` table.
- Retrieves telemetry based on device ID.
- Retrieves the latest telemetry using timestamp ordering.
- Updates telemetry values.
- Deletes telemetry records.

---

## 5. System APIs

These APIs are used for application monitoring.

### APIs

| Method | Endpoint | Role |
|---------|----------|------|
| GET | `/` | Root endpoint to verify API availability. |
| GET | `/health` | Returns the health status of the backend service. |

**Database Interaction**

- No database interaction.
- Used only for service availability checks.

---

# Database Tables Used

| Table | Purpose |
|--------|---------|
| `users` | Stores user accounts and authentication information. |
| `devices` | Stores registered drone/device information. |
| `telemetry` | Stores telemetry data received from drones. |

---

# Authentication

Protected APIs use JWT Bearer Authentication.

Workflow:

1. User logs in using `/auth/login`.
2. Server validates credentials.
3. JWT token is generated.
4. Token is supplied through Swagger Authorize or HTTP Authorization Header.
5. Protected APIs validate the token before processing the request.

---

# API Testing

All APIs were tested using Swagger UI.

Testing included:

- Successful requests (200 OK)
- Resource creation
- Resource retrieval
- Resource update
- Resource deletion
- Authentication using JWT tokens

---

# Phase 2 Summary

Phase 2 successfully implemented the core backend functionality of the DroneCloud project. The backend now supports:

- User Authentication
- User Management
- Device Management
- Telemetry Management
- Health Monitoring APIs

A total of **19 REST APIs** were developed and integrated with the PostgreSQL database. All CRUD operations were implemented where required, and protected endpoints were secured using JWT authentication.

Phase 2 establishes the backend foundation required for subsequent phases, including mission management, live video streaming, and drone control.
