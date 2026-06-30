# Private Cloud Drone Project - Project Setup Documentation

---

# Project Information

**Project Name**

Private Cloud Drone Project

**Project Objective**

The objective of this project is to design and develop a secure private cloud platform capable of receiving live video streams from mobile devices (and later drones), displaying the stream through a secure HTTPS web interface, recording videos, storing captured images, collecting telemetry data, and managing all information through a scalable backend infrastructure.

The system is initially developed using a mobile phone as the streaming device to simplify testing and development. Once the architecture is fully validated, the same backend will be extended to support drone-based live transmission with minimal modifications.

---

# Development Environment

| Component | Version |
|-----------|---------|
| Operating System | Ubuntu 24.04.4 LTS |
| Python | Python 3.x |
| Docker | Installed |
| Docker Compose | Installed |
| Git | Installed |
| FFmpeg | Installed |
| mkcert | Installed |
| OpenSSL | Installed |

---

# Project Goals

The project aims to achieve the following objectives:

- Secure HTTPS communication
- Live video transmission
- Video recording
- Image capture
- Telemetry data storage
- PostgreSQL database integration
- Docker-based deployment
- Modular backend architecture
- Future drone compatibility
- Scalable private cloud infrastructure

---

# System Requirements

## Hardware

- Ubuntu PC
- Minimum 8 GB RAM
- Multi-core Processor
- Internet Connection
- Mobile Phone (Initial Testing)
- Drone (Future Phase)

---

## Software

- Ubuntu 24.04 LTS
- Python 3
- Docker
- Docker Compose
- Git
- GitHub
- FastAPI
- PostgreSQL
- Nginx
- FFmpeg
- mkcert
- OpenSSL

---

# Development Workflow

The project follows an incremental development methodology.

Each phase consists of:

1. Environment Setup
2. Implementation
3. Testing
4. Documentation
5. Git Commit
6. GitHub Push

---

# Ubuntu Installation

Ubuntu 24.04.4 LTS was installed as the primary development operating system.

Verification command:

```bash
lsb_release -a
```

Output verified:

```
Ubuntu 24.04.4 LTS
```

---

# Git Installation

Git was verified using:

```bash
git --version
```

Purpose:

- Version Control
- Collaboration
- GitHub Integration

---

# GitHub Repository Setup

A private GitHub repository was created for the project.

Repository Features:

- Private Repository
- SSH Authentication
- Git Version Control
- Documentation Management

---

# SSH Authentication

An SSH key pair was generated and linked to the GitHub account.

Commands used:

```bash
ssh-keygen -t ed25519 -C "<GitHub Email>"
```

Start SSH Agent

```bash
eval "$(ssh-agent -s)"
```

Add SSH Key

```bash
ssh-add ~/.ssh/id_ed25519
```

Verify Connection

```bash
ssh -T git@github.com
```

Purpose:

Secure authentication without entering username and password for every Git operation.

---

# Docker Installation

Docker was verified.

Verification command:

```bash
docker --version
```

Purpose:

Containerization of the complete application stack.

---

# Docker Compose

Docker Compose was verified.

Verification:

```bash
docker compose version
```

Purpose:

Manage multiple services including:

- FastAPI
- PostgreSQL
- Nginx

using a single configuration file.

---

# Python Virtual Environment

A dedicated virtual environment was created.

Create environment

```bash
python3 -m venv .venv
```

Activate

```bash
source .venv/bin/activate
```

Purpose:

- Isolated Python dependencies
- Reproducible development environment

---

# FFmpeg Installation

Installed using:

```bash
sudo apt install ffmpeg
```

Purpose:

- Video Recording
- Image Extraction
- Video Compression
- Metadata Extraction
- Future Live Stream Recording

---

# mkcert Installation

Installed using:

```bash
sudo apt install mkcert libnss3-tools
```

Initialize:

```bash
mkcert -install
```

Purpose:

Generate trusted local HTTPS certificates for development.

---

# OpenSSL

Verified as part of the Ubuntu installation.

Purpose:

- Cryptographic operations
- SSL certificate support
- Secure communication

---

# Project Folder Structure

```
DroneCloudProject/

│

├── backend/

├── frontend/

├── nginx/

├── database/

├── uploads/

├── videos/

├── recordings/

├── logs/

├── certificates/

├── docs/

├── docker-compose.yml

├── README.md

└── .env
```

---

# Backend Initialization

Backend Framework:

FastAPI

Backend Structure

```
backend/

│

├── app/

│ ├── api/

│ ├── auth/

│ ├── core/

│ ├── database/

│ ├── models/

│ ├── schemas/

│ ├── services/

│ ├── storage/

│ ├── streaming/

│ ├── telemetry/

│ ├── utils/

│ ├── __init__.py

│ └── main.py

│

├── Dockerfile

└── requirements.txt
```

---

# Python Dependencies

Major backend packages installed:

- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- psycopg
- python-dotenv
- Pydantic
- python-multipart
- python-jose
- passlib
- aiofiles
- loguru

Dependency list stored in:

```
requirements.txt
```

---

# Dockerfile

A backend Docker image was created using:

- Python 3.12 Slim
- FastAPI
- Uvicorn

Purpose:

Create a portable backend container.

---

# Docker Compose

Docker Compose orchestrates:

- Backend Container
- PostgreSQL Container
- Nginx Container

Responsibilities:

- Network creation
- Volume mounting
- Service orchestration
- Environment variable management

---

# PostgreSQL Container

Database:

PostgreSQL 16

Purpose:

Store:

- Users
- Devices
- Videos
- Images
- Telemetry
- Authentication data

---

# Nginx Configuration

Nginx acts as:

- Reverse Proxy
- HTTPS Gateway
- Future Static File Server

Responsibilities:

- HTTPS termination
- Request forwarding
- Security headers
- Future rate limiting

---

# HTTPS Configuration

Development certificates were generated using:

```bash
mkcert localhost 127.0.0.1 ::1
```

Generated files:

```
localhost.pem

localhost-key.pem
```

Purpose:

Enable secure HTTPS communication during development.

---

# Problems Encountered

During the setup process several issues were encountered.

## Docker Image Download

Problem:

Docker experienced TLS handshake timeout while downloading images.

Solution:

Images were downloaded manually before running Docker Compose.

---

## Nginx HTTPS Certificates

Problem:

Nginx failed to locate SSL certificate files.

Cause:

Generated certificate names differed from the names expected in the Nginx configuration.

Solution:

Certificate files were renamed to match the Nginx configuration.

---

## Docker Backend Port

Problem:

Backend service was inaccessible from the host machine.

Cause:

Port mapping was missing from the backend service in `docker-compose.yml`.

Solution:

Added:

```yaml
ports:
  - "8000:8000"
```

---

# Final Verification

The following components were successfully verified.

| Component | Status |
|-----------|--------|
| Ubuntu | ✅ |
| Git | ✅ |
| GitHub SSH | ✅ |
| Docker | ✅ |
| Docker Compose | ✅ |
| Python Virtual Environment | ✅ |
| FFmpeg | ✅ |
| mkcert | ✅ |
| OpenSSL | ✅ |
| FastAPI Backend | ✅ |
| Docker Backend Container | ✅ |
| PostgreSQL Container | ✅ |
| Nginx Container | ✅ |
| HTTPS Certificates | ✅ |

---

# Current Project Status

**Phase Completed**

Project Environment Setup and Backend Infrastructure

Current Working Features:

- Ubuntu Development Environment
- Docker Infrastructure
- FastAPI Backend
- PostgreSQL Container
- Nginx Reverse Proxy
- HTTPS Development Certificates
- GitHub Version Control

---

# Next Phase

Backend Development

Upcoming Tasks:

- Database Integration
- Authentication System
- File Storage APIs
- Video Recording
- Image Capture
- Telemetry Management
- Secure Live Video Transmission
