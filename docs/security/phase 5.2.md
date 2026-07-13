# Phase 5.2 Final Report
# Secure Device Authentication & Resource Ownership

---

# Objective

Phase 5.2 extends the Device Authentication framework introduced in Phase 5.1 to every device-generated resource in the system.

Instead of trusting client-supplied device identifiers, the backend now derives device ownership directly from the authenticated Device JWT.

Every telemetry packet, uploaded video, and uploaded image is automatically associated with the authenticated device.

This establishes a secure Device → Backend trust model suitable for Android devices today and Raspberry Pi / Jetson devices in future deployments.

---

# Security Architecture

```
                    User
                      │
            POST /auth/login
                      │
                  User JWT
                      │
                      ▼
          POST /devices/register
                      │
                      ▼
      device_uuid + device_secret
                      │
                      ▼
                 Edge Device
          (Android / Raspberry Pi)
                      │
          POST /devices/auth
                      │
                  Device JWT
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Telemetry      Video Upload   Image Upload
        │             │             │
        ▼             ▼             ▼
 get_current_device() get_current_device() get_current_device()
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                 PostgreSQL
```

---

# Core Security Principle

The backend never trusts:

```json
{
    "device_id": 7
}
```

Instead:

```
Device JWT

↓

get_current_device()

↓

Authenticated Device

↓

device.id

↓

Database
```

Device ownership is always determined by the backend.

Clients cannot impersonate another device simply by modifying request payloads.

---

# Completed Work

---

# 1. Secure Telemetry Upload

## Previous Design

Telemetry upload accepted:

```json
{
    "device_id": 7,
    "latitude": ...,
    "longitude": ...
}
```

This allowed device spoofing.

---

## New Design

Telemetry upload now requires:

```python
current_device: Device = Depends(get_current_device)
```

The CRUD layer stores:

```python
device_id=current_device.id
```

instead of trusting client input.

---

## Files Modified

```
backend/app/api/v1/telemetry.py
backend/app/crud/telemetry.py
backend/app/schemas/telemetry.py
```

---

# 2. Secure Video Upload

Video uploads are now linked to authenticated devices.

---

## Database

Added:

```
device_id
```

Foreign Key:

```
videos.device_id
→ devices.id
```

---

## CRUD

Old

```python
create_video(...)
```

New

```python
create_video(
    db,
    device,
    filename,
    filepath,
    ...
)
```

---

## API

Video upload now requires:

```python
current_device: Device = Depends(get_current_device)
```

instead of anonymous uploads.

---

## Files Modified

```
backend/app/api/videos.py
backend/app/crud/video.py
backend/app/models/video.py
```

---

# 3. Secure Image Upload

Image upload security follows the same architecture used for telemetry and video uploads.

---

## Database Changes

Modified:

```
backend/app/models/image.py
```

Added:

```python
device_id = Column(
    Integer,
    ForeignKey("devices.id"),
    nullable=False,
)
```

---

## Alembic Migration

Created migration:

```
add_device_id_to_images
```

Added:

```
device_id INTEGER NOT NULL
```

Foreign Key:

```
images.device_id
→ devices.id
```

---

## CRUD Changes

Created:

```
backend/app/crud/image.py
```

Added:

```python
create_image(
    db,
    device,
    filename,
    filepath,
    file_size,
)
```

The CRUD layer automatically stores:

```python
device_id=device.id
```

---

## API

Created:

```
backend/app/api/images.py
```

Implemented:

```
POST /images/upload
```

Security:

```python
current_device: Device = Depends(get_current_device)
```

Image validation:

```
image/*
```

Storage:

```
uploads/images/
```

Unique filenames:

```
device_uuid_original_filename
```

---

## Router Registration

Registered:

```
backend/app/main.py
```

```
app.include_router(images_router)
```

---

# Database Ownership Model

All device-generated resources now contain:

Telemetry

```
device_id
```

Videos

```
device_id
```

Images

```
device_id
```

Every uploaded resource belongs to exactly one authenticated device.

---

# Security Improvements

Before Phase 5.2

```
Client

↓

device_id=7

↓

Backend
```

Anyone could impersonate another device.

---

After Phase 5.2

```
JWT

↓

get_current_device()

↓

Authenticated Device

↓

device.id

↓

Database
```

Device ownership is enforced by the backend.

---

# Testing Performed

## Device Registration

```
POST /devices/register
```

Verified:

- Device UUID generation
- Device Secret generation

---

## Device Authentication

```
POST /devices/auth
```

Verified:

- JWT generation
- Device lookup
- Secret verification

---

## Telemetry Upload

Verified:

- JWT validation
- Database insertion
- device_id ownership

---

## Video Upload

Verified:

- JWT validation
- Video upload
- Database insertion
- device ownership

---

## Image Upload

Verified:

```
POST /images/upload
```

Multipart upload:

```
image=@test.png
```

Verified:

- JWT authentication
- File upload
- Image storage
- Database insertion
- device ownership

---

# Database Verification

Telemetry

```sql
SELECT *
FROM telemetry;
```

Videos

```sql
SELECT *
FROM videos;
```

Images

```sql
SELECT *
FROM images;
```

Verified that every record contains the correct authenticated device_id.

---

# Major Debugging & Issues Resolved

## 1. Duplicate Telemetry Routes

Removed duplicated routes and obsolete schemas.

---

## 2. Video Migration

Added:

```
device_id
```

to videos.

---

## 3. Image Migration

Initially generated an empty Alembic migration.

Solution:

Manually implemented migration.

---

## 4. Docker Container Using Old Model

Container continued using an outdated Image model.

Solution:

Rebuilt backend container.

---

## 5. Missing device_id in Image Model

Image model was not updated after migration.

Solution:

Added:

```python
device_id
```

to the SQLAlchemy model.

---

## 6. Root-Owned uploads Directory

Docker created uploads as root.

Solution:

```
sudo chown -R drone:drone uploads
```

---

## 7. Swagger OAuth Limitation

Swagger attempted OAuth Password flow for Device authentication.

Result:

```
422 Unprocessable Entity
```

Resolution:

Used Device Authentication API directly for testing.

Future improvement:

Separate User OAuth and Device Bearer Authentication in OpenAPI.

---

# Files Modified

Telemetry

```
backend/app/api/v1/telemetry.py
backend/app/crud/telemetry.py
backend/app/schemas/telemetry.py
```

Videos

```
backend/app/api/videos.py
backend/app/crud/video.py
backend/app/models/video.py
```

Images

```
backend/app/api/images.py
backend/app/crud/image.py
backend/app/models/image.py
```

Security

```
app/core/security.py
```

Database

```
Alembic migrations

telemetry
videos
images
```

---

# Final Architecture

```
                 Edge Device
                        │
                        ▼
               Device Authentication
                        │
                        ▼
                  Device JWT
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
  Telemetry API    Video Upload    Image Upload
        │               │               │
        ▼               ▼               ▼
 get_current_device()  get_current_device()  get_current_device()
        │               │               │
        ▼               ▼               ▼
 telemetry.device_id videos.device_id images.device_id
```

---

# Current Security Status

Completed

- ✅ Device Registration
- ✅ Device Authentication
- ✅ Device JWT
- ✅ Secure Telemetry Upload
- ✅ Secure Video Upload
- ✅ Secure Image Upload
- ✅ Automatic Resource Ownership


# Outcome

Phase 5.2 successfully establishes secure ownership of every device-generated resource.

All telemetry packets, uploaded videos, and uploaded images are now cryptographically tied to the authenticated device through Device JWT authentication.

This architecture eliminates client-side device spoofing and provides a scalable foundation for future Raspberry Pi, Jetson Nano, and autonomous drone deployments.