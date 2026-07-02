# Phase 2 Documentation
# DroneCloud Backend Development – Telemetry Management API

**Phase:** 2 – Telemetry Management API  
**Framework:** FastAPI  
**Database:** PostgreSQL  
**ORM:** SQLAlchemy  
**Authentication:** JWT Authentication  

---

# 1. Objective

The objective of Phase 2 was to develop a complete Telemetry Management API for the DroneCloud backend.

The telemetry module allows authenticated users to:

- Upload telemetry data
- View all telemetry
- View telemetry for a specific drone
- Retrieve the latest telemetry
- Update telemetry
- Delete telemetry

All endpoints are protected using JWT authentication.

---

# 2. Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Swagger UI
- JWT Authentication
- Pydantic

---

# 3. Folder Structure

```
backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── telemetry.py
│   │
│   ├── crud/
│   │       └── telemetry.py
│   │
│   ├── models/
│   │       └── telemetry.py
│   │
│   ├── schemas/
│   │       └── telemetry.py
│   │
│   └── database.py
│
├── Dockerfile
└── requirements.txt
```

---

# 4. Database Schema

Initially the telemetry table contained:

| Column |
|----------|
| id |
| latitude |
| longitude |
| altitude |
| speed |
| heading |
| battery |
| timestamp |

During development, two additional columns became necessary:

```
device_id
battery_level
```

Final schema:

| Column | Type |
|---------|------|
| id | Integer |
| device_id | Integer |
| latitude | Float |
| longitude | Float |
| altitude | Float |
| speed | Float |
| heading | Float |
| battery | Integer |
| battery_level | Integer |
| timestamp | Timestamp |

---

# 5. APIs Implemented

---

## 5.1 Create Telemetry

### Endpoint

```
POST /telemetry/
```

### Purpose

Stores telemetry received from a drone.

### Request Body

```json
{
    "device_id":3,
    "latitude":31.634,
    "longitude":74.872,
    "altitude":120.5,
    "battery_level":85
}
```

### Response

```json
{
    "id":1,
    "device_id":3,
    "latitude":31.634,
    "longitude":74.872,
    "altitude":120.5,
    "battery_level":85,
    "timestamp":"..."
}
```

---

## 5.2 Get All Telemetry

### Endpoint

```
GET /telemetry/
```

### Purpose

Returns every telemetry record stored in the database.

---

## 5.3 Get Latest Telemetry

### Endpoint

```
GET /telemetry/device/{device_id}/latest
```

### Purpose

Returns the newest telemetry entry for a particular drone.

Example:

```
GET /telemetry/device/3/latest
```

---

## 5.4 Get Device Telemetry

### Endpoint

```
GET /telemetry/device/{device_id}
```

### Purpose

Returns every telemetry record belonging to a particular drone.

---

## 5.5 Update Telemetry

### Endpoint

```
PUT /telemetry/{telemetry_id}
```

### Purpose

Updates an existing telemetry record.

---

## 5.6 Delete Telemetry

### Endpoint

```
DELETE /telemetry/{telemetry_id}
```

### Purpose

Deletes a telemetry record.

---

# 6. CRUD Functions Developed

Inside

```
app/crud/telemetry.py
```

the following functions were implemented.

```
create_telemetry()

get_all_telemetry()

get_latest_telemetry()

get_device_telemetry()

update_telemetry()

delete_telemetry()
```

---

# 7. Authentication

Every endpoint requires authentication.

Dependency used:

```python
current_user: User = Depends(get_current_user)
```

JWT Bearer token is supplied through Swagger Authorize button.

---

# 8. Testing

Testing was performed using Swagger UI.

Each endpoint was tested for:

- Successful request (200)
- Record not found (404)
- Unauthorized access (401)
- Internal server errors (500)

---

# 9. Major Problems Faced

## Problem 1

### Error

```
AttributeError:
Telemetry has no attribute device_id
```

### Cause

Telemetry model did not contain

```
device_id
```

### Solution

Added

```python
device_id = Column(
    Integer,
    ForeignKey("devices.id"),
    nullable=False
)
```

to

```
models/telemetry.py
```

---

## Problem 2

### Error

```
column telemetry.device_id does not exist
```

### Cause

The SQLAlchemy model had been updated, but the PostgreSQL table schema had not.

### Solution

Added a new database column:

```sql
ALTER TABLE telemetry
ADD COLUMN device_id INTEGER;
```

---

## Problem 3

### Error

```
column battery_level does not exist
```

### Cause

Model used

```
battery_level
```

while database still contained

```
battery
```

### Solution

Added:

```sql
ALTER TABLE telemetry
ADD COLUMN battery_level INTEGER;
```

Copied existing values:

```sql
UPDATE telemetry
SET battery_level = battery;
```

---

## Problem 4

### Error

```
UPDATE 0
```

### Cause

Telemetry table contained zero records.

### Solution

Inserted sample telemetry manually.

---

## Problem 5

### Error

```
No telemetry found
```

### Cause

No telemetry rows existed.

### Solution

Inserted sample telemetry.

---

## Problem 6

### Error

```
RecursionError:
maximum recursion depth exceeded
```

### Cause

API function

```
get_device_telemetry()
```

had the same name as the imported CRUD function, causing the endpoint to recursively call itself.

### Solution

Renamed the API function to:

```python
get_telemetry_by_device()
```

while keeping the CRUD function name unchanged.

---

## Problem 7

### Error

```
role "postgres" does not exist
```

### Cause

Attempted to connect using the wrong PostgreSQL user.

### Solution

Checked the `.env` file and found:

```
POSTGRES_USER=droneadmin
```

Connected using:

```bash
docker compose exec postgres psql \
-U droneadmin \
-d dronecloud
```

---

## Problem 8

### Error

```
column name does not exist
```

### Cause

The `devices` table did not contain a `name` column.

### Solution

Inspected the table:

```sql
\d devices
```

Used the correct column:

```
device_name
```

---

## Problem 9

### Empty Telemetry Table

Verified using:

```sql
SELECT COUNT(*) FROM telemetry;
```

Result:

```
0
```

Solution:

Inserted sample telemetry manually.

---

# 10. SQL Commands Used

## View telemetry schema

```sql
\d telemetry
```

---

## View devices schema

```sql
\d devices
```

---

## Count telemetry records

```sql
SELECT COUNT(*) FROM telemetry;
```

---

## View available devices

```sql
SELECT id, device_name FROM devices;
```

---

## Insert telemetry

```sql
INSERT INTO telemetry (
device_id,
latitude,
longitude,
altitude,
battery_level
)
VALUES (
3,
31.634,
74.872,
120.5,
85
);
```

---

## Update telemetry

```sql
UPDATE telemetry
SET battery_level = battery;
```

---

## Assign device IDs

```sql
UPDATE telemetry
SET device_id = 3
WHERE device_id IS NULL;
```

---

# 11. Docker Commands Used

Restart backend

```bash
docker compose restart backend
```

View logs

```bash
docker compose logs backend --tail=30
```

Open PostgreSQL

```bash
docker compose exec postgres \
psql -U droneadmin -d dronecloud
```

---

# 12. Verification

The following endpoints were successfully tested:

- ✅ POST /telemetry
- ✅ GET /telemetry
- ✅ GET /telemetry/device/{id}
- ✅ GET /telemetry/device/{id}/latest
- ✅ PUT /telemetry/{id}
- ✅ DELETE /telemetry/{id}

---

# 13. Learning Outcomes

During this phase the following concepts were learned:

- FastAPI API development
- SQLAlchemy CRUD operations
- Pydantic schema validation
- Dependency Injection
- JWT authentication
- PostgreSQL integration
- Docker container debugging
- Swagger API testing
- Database schema modification
- SQL debugging
- SQLAlchemy relationship mapping
- REST API design
- Error diagnosis using backend logs
- Recursive function debugging

---

# 14. Phase 2 Summary

Phase 2 successfully implemented a complete Telemetry Management module for DroneCloud. The module supports full CRUD operations with authentication, database integration, and Swagger testing. Several database schema mismatches and runtime issues were identified and resolved, resulting in a stable and functional telemetry API.

**Status:** ✅ Phase 2 Completed
