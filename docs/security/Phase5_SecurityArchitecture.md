# Phase 5.0 – Security Architecture

---

# 1. Introduction

The **Private Cloud Drone Project** is designed as a secure, scalable, and hardware-independent platform for real-time device communication, live video streaming, telemetry collection, recording management, and remote monitoring.

The project initially uses an **Android phone** as the edge device to simplify development and testing. However, the long-term vision is to support multiple hardware platforms without requiring changes to the backend architecture.

## Key Concepts

- The backend is designed around the concept of a generic **Edge Device**.
- An edge device represents any authenticated hardware capable of communicating securely with the backend.
- The backend does not depend on the physical hardware being used.
- Every connected device is treated as an authenticated entity with its own identity, capabilities, and permissions.

## Supported Edge Devices (Current & Future)

Examples of supported devices include:

- Android Phone
- Raspberry Pi
- Raspberry Pi with Camera Module
- NVIDIA Jetson Nano
- NVIDIA Orin
- Industrial IPC
- Future embedded edge devices

## Hardware-Independent Architecture

Instead of designing the system specifically for mobile phones, the backend is built around authenticated devices.

The backend never asks:

> "Is this a phone?"

Instead, it asks:

> "Is this an authenticated device?"

As long as a device successfully authenticates and possesses the required capabilities, it is handled identically regardless of its hardware platform.

## Importance of Security

As the project evolves into a production-ready private cloud platform, security becomes a core architectural requirement rather than an additional feature.

Security must protect:

- Users
- Devices
- Live video streams
- Telemetry data
- Recorded videos
- APIs
- WebSocket communication
- Database contents
- Administrative operations
- System configuration

Every interaction within the system must be:

- Authenticated
- Authorized
- Validated
- Auditable
- Protected against unauthorized access

---

# 2. Security Objectives

The primary goal of this security architecture is to build a secure and hardware-independent platform for communication between edge devices and the backend.

The security architecture focuses on the following objectives:

- Authenticate every user and edge device before allowing access to the system.
- Ensure that users and devices can only perform actions they are authorized to execute.
- Protect all communication between devices, the backend, and the dashboard.
- Secure APIs, WebSocket connections, video recordings, and telemetry data from unauthorized access.
- Maintain the confidentiality, integrity, and availability of system resources.
- Record important security-related activities through audit logs.
- Design the backend to work with any authenticated edge device without depending on specific hardware.
- Provide a scalable security foundation that can support future enhancements and additional edge devices.

Overall, the objective of this security architecture is to ensure that the system remains secure, scalable, maintainable, and ready for deployment in real-world edge computing environments.

---

# 3. Scope

This document defines the security architecture for the Private Cloud Drone Project. It outlines the security principles, requirements, and strategies that will be followed throughout the development of the system.

## In Scope

The security architecture covers:

- User authentication and authorization
- Edge device authentication
- Secure REST APIs
- Secure WebSocket communication
- Video recording and playback security
- File upload security
- Database security
- Audit logging
- HTTP security
- Data integrity and protection

## Out of Scope

The following topics are not covered in this phase and may be considered in future enhancements:

- Physical security of edge devices
- Operating system hardening
- Secure Boot and firmware signing
- Hardware security modules (HSM/TPM)
- Network infrastructure security outside the application
- Cloud infrastructure security

The focus of this document is to establish a strong security foundation for the application while keeping the backend scalable, maintainable, and hardware-independent.

---

# 4. System Overview

The Private Cloud Drone Project is designed around a generic **Edge Device** architecture instead of being tied to a specific hardware platform.

An edge device can be any authenticated hardware capable of streaming video, sending telemetry, receiving commands, and communicating securely with the backend.

Current and future supported edge devices include:

- Android Phone
- Raspberry Pi
- Raspberry Pi with Camera Module
- NVIDIA Jetson Nano
- NVIDIA Orin
- Industrial IPC
- Other embedded edge devices

The backend is designed to identify and communicate with authenticated devices rather than specific hardware types. This ensures that new devices can be integrated without modifying the backend architecture.

## System Architecture

```
            Camera / Sensors
                   │
                   ▼
              Edge Device
                   │
                   ▼
        Secure Communication Layer
          (HTTPS / WSS / WebRTC)
                   │
                   ▼
             Secure Backend
        (FastAPI + PostgreSQL)
                   │
                   ▼
               Dashboard
```

## Component Overview

### Edge Device

The edge device is responsible for:

- Capturing live video
- Sending telemetry data
- Receiving commands
- Authenticating with the backend

### Communication Layer

The communication layer provides secure communication between edge devices and the backend using:

- HTTPS for REST APIs
- Secure WebSockets (WSS) for signaling
- WebRTC for live video streaming

### Secure Backend

The backend is responsible for:

- Authenticating users and devices
- Processing API requests
- Managing recordings and telemetry
- Enforcing authorization
- Maintaining audit logs

### Dashboard

The dashboard allows authenticated users to:

- Monitor live video streams
- View telemetry
- Manage recordings
- Control authorized devices

---

# 5. Security Design Principles

The security architecture of the project is based on a set of core principles that guide the design and implementation of every security feature.

## Zero Trust

- No user or device is trusted by default.
- Every request must be authenticated before access is granted.

---

## Least Privilege

- Users and devices are given only the permissions they need.
- Access to sensitive resources is restricted to authorized entities.

---

## Hardware Independence

- The backend is designed around authenticated edge devices instead of specific hardware.
- New devices can be integrated without changing the backend architecture.

---

## Secure Communication

- All communication between devices, the backend, and the dashboard must use secure channels.
- Sensitive data should never be transmitted over unsecured connections.

---

## Defense in Depth

- Security is applied at multiple layers instead of relying on a single protection mechanism.
- Authentication, authorization, validation, and logging work together to secure the system.

---

## Input Validation

- Every request received by the backend must be validated before processing.
- Invalid or malicious data should be rejected.

---

## Auditability

- Important system activities should be recorded through audit logs.
- Logs help monitor system activity and support troubleshooting and security analysis.

---

## Scalability

- The security architecture should support future devices and new features without requiring major architectural changes.
- New security mechanisms should integrate seamlessly with the existing system.

---

# 6. Assets to Protect

The security architecture is designed to protect the critical resources of the Private Cloud Drone Project from unauthorized access, modification, or misuse.

The primary assets that require protection include:

- User accounts and credentials
- Edge device identities and authentication information
- Live video streams
- Recorded videos
- Telemetry data
- Device commands
- REST APIs
- WebSocket connections
- Database records
- Authentication tokens
- Configuration files and application secrets
- Audit logs

Protecting these assets ensures that only authorized users and devices can access system resources while maintaining the confidentiality, integrity, and availability of the platform.

---

# 7. Actors

The Private Cloud Drone Project consists of two primary types of actors: **Users** and **Edge Devices**. Each actor has a specific role and set of permissions within the system.

## Users

Users access the system through the dashboard to monitor devices and manage system resources.

The supported user roles include:

- Administrator
- Operator
- Viewer

Each role is assigned different permissions based on its responsibilities.

---

## Edge Devices

Edge devices communicate directly with the backend after successful authentication.

Examples of supported edge devices include:

- Android Phone
- Raspberry Pi
- Raspberry Pi with Camera Module
- NVIDIA Jetson Nano
- NVIDIA Orin
- Industrial IPC
- Other embedded edge devices

Regardless of the hardware platform, every device is treated as a generic authenticated edge device by the backend.

---

## Interaction Model

The system is designed around two independent authentication models:

- **Users** authenticate to access the dashboard and management features.
- **Edge Devices** authenticate to stream video, send telemetry, upload recordings, receive commands, and communicate with the backend.

This separation ensures that user operations and device operations remain independent while following the same security principles.

---

# 8. Threat Model

The security architecture is designed to protect the system against common security threats that may affect users, edge devices, communication channels, and stored data.

Some of the primary threats considered include:

- Unauthorized user or device access
- Device impersonation
- Stolen or expired authentication tokens
- Unauthorized API requests
- WebSocket connection misuse
- Malicious file uploads
- Unauthorized access to video recordings
- Data tampering during transmission
- Database compromise
- Denial-of-Service (DoS) attacks

To reduce these risks, the system follows a layered security approach that includes authentication, authorization, encrypted communication, input validation, audit logging, and secure data handling.

By identifying these threats during the design phase, appropriate security controls can be implemented throughout the system to minimize potential vulnerabilities.

---

# 9. Authentication Model

Authentication is the process of verifying the identity of users and edge devices before allowing access to the system.

The project uses separate authentication mechanisms for users and edge devices to ensure secure and independent access control.

## User Authentication

Users authenticate through the dashboard using their credentials.

After successful authentication:

- A JWT access token is issued.
- The token is used to access protected APIs.
- User permissions are determined based on their assigned role.

## Device Authentication

Every edge device must authenticate with the backend before communicating with the system.

Each device is identified using:

- Device ID / UUID
- Device Type
- Authentication Credentials

After successful authentication:

- The device receives a JWT access token.
- The token is used for secure communication with the backend.
- The device can only access the services it is authorized to use.

## Authentication Flow

```
User / Edge Device
        │
        ▼
Authenticate
        │
        ▼
Identity Verified
        │
        ▼
JWT Token Issued
        │
        ▼
Access Protected Resources
```

By maintaining separate authentication models for users and edge devices, the system remains secure, scalable, and independent of the underlying hardware platform.

---

# 10. Authorization Model

Authorization determines what an authenticated user or edge device is allowed to access within the system.

The project follows **Role-Based Access Control (RBAC)**, where permissions are assigned based on roles instead of individual users or devices.

## User Roles

The system supports the following user roles:

- Administrator
- Operator
- Viewer

Each role has a different level of access to system resources and management features.

## Device Permissions

Authenticated edge devices are granted permissions based on their assigned capabilities.

Examples include:

- Live video streaming
- Telemetry transmission
- Recording uploads
- Command reception
- Heartbeat communication

Devices are only allowed to perform the operations assigned to them and cannot access administrative or user management features.

## Authorization Principle

The system follows the **Least Privilege Principle**, meaning users and devices are granted only the permissions required to perform their intended tasks.

This approach helps prevent unauthorized access while improving the overall security of the platform.

---

# 11. Communication Security

All communication between edge devices, users, and the backend must take place over secure communication channels.

The project uses:

- HTTPS for REST API communication
- Secure WebSockets (WSS) for signaling
- WebRTC for peer-to-peer live video streaming

These protocols help protect data from unauthorized access and interception during transmission.

---

# 12. Data Protection

The system is designed to protect both transmitted and stored data.

The following data is considered sensitive:

- User information
- Device information
- Video recordings
- Telemetry data
- Authentication tokens
- System configuration

Security measures will ensure that only authorized users and devices can access or modify this information.

---

# 13. Audit Logging

Security-related activities should be recorded to improve system monitoring and traceability.

Examples of logged events include:

- User login
- Device authentication
- Recording upload
- Recording deletion
- Failed authentication attempts
- Important administrative actions

Audit logs help monitor system activity and support troubleshooting and security analysis.

---

# 14. Security Roadmap

The security architecture will be implemented in multiple phases.

| Phase | Focus |
|--------|-------|
| Phase 5.1 | Identity & Authentication |
| Phase 5.2 | Authorization |
| Phase 5.3 | API Security |
| Phase 5.4 | WebSocket Security |
| Phase 5.5 | Video Security |
| Phase 5.6 | Upload Security |
| Phase 5.7 | Database Hardening |
| Phase 5.8 | Audit Logging |
| Phase 5.9 | HTTP Security |
| Phase 5.10 | Integrity & Encryption |

Each phase builds upon the previous one to create a complete and scalable security framework.

---

# 15. Summary

The security architecture establishes the foundation for building a secure, scalable, and hardware-independent Private Cloud Drone Platform.

Key highlights of the architecture include:

- Hardware-independent edge device model
- Separate authentication for users and devices
- Role-based authorization
- Secure communication channels
- Protection of sensitive data and recordings
- Audit logging for important system events
- Modular security implementation through phased development

This architecture serves as the blueprint for all future security implementations while ensuring that the backend remains adaptable to new edge devices and future system enhancements.
