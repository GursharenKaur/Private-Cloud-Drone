# Private Cloud Drone Project

## Overview

Private Cloud Drone Project is a secure private cloud platform designed for real-time live video transmission, recording, telemetry monitoring, and media storage. The system is initially developed using a mobile phone as the streaming device and is designed to be extended to drones without major architectural changes.

The project emphasizes secure communication using HTTPS, containerized deployment with Docker, modular backend development using FastAPI, and efficient storage of media and telemetry data.

---

## Key Features

- Secure HTTPS communication
- Live video streaming from mobile devices
- Video recording and storage
- Image capture and storage
- Telemetry data collection
- PostgreSQL database integration
- Docker-based deployment
- Modular backend architecture
- Scalable design for future drone integration

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Operating System | Ubuntu 24.04 LTS |
| Backend | FastAPI |
| Web Server | Nginx |
| Database | PostgreSQL |
| Containerization | Docker & Docker Compose |
| Programming Language | Python |
| Security | HTTPS (mkcert during development) |
| Media Processing | FFmpeg |

---

## Project Structure

```text
DroneCloudProject/
├── backend/
├── frontend/
├── nginx/
├── database/
├── uploads/
├── recordings/
├── videos/
├── certificates/
├── docs/
├── docker-compose.yml
└── README.md
```

---

## Documentation

Detailed documentation is available in the `docs/` directory.

device_uuid:
f04a2356-0b19-409e-9d85-5ba9ca61617b

device_secret:
tKYca9EE59I1lAmGm_Qx4HWBFAgLBXVuCNu0F4jQoMc

---


## License

This project is intended for academic and research purposes.
