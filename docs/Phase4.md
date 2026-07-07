# Phase 4 - Video Recording & Storage Documentation

## Overview

The objective of this phase was to extend the existing WebRTC live streaming system by introducing a complete video recording and storage pipeline. This phase enables the dashboard to record the incoming live video stream, automatically upload the recorded video to the backend, store the video on the server, and maintain its metadata inside PostgreSQL for future retrieval and management.

---

# 1. Video Recording

### Objective
Enable recording of the live WebRTC stream directly from the dashboard.

### Features Implemented

- Added **Start Recording** button on the dashboard.
- Added **Stop Recording** button on the dashboard.
- Integrated the browser's **MediaRecorder API**.
- Configured MediaRecorder to record the incoming **WebRTC remote stream** instead of the local camera stream.
- Captured recorded data in small chunks using the `ondataavailable` event.
- Combined all recorded chunks into a single `.webm` Blob once recording stops.

### Working Flow

```
Remote WebRTC Stream
          │
          ▼
    MediaRecorder
          │
          ▼
Collect Video Chunks
          │
          ▼
Combine Chunks
          │
          ▼
recording.webm Blob
```

---

# 2. Download Recorded Video

### Objective

Allow users to immediately download the recorded video after recording is completed.

### Features Implemented

- Automatically generated a downloadable `.webm` file.
- Created a Blob URL for the recorded video.
- Triggered automatic file download once recording stopped.
- Verified that the downloaded recording plays correctly.

### Workflow

```
Stop Recording
       │
       ▼
Create Blob
       │
       ▼
Generate Blob URL
       │
       ▼
Automatic Download
```

---

# 3. Backend Video Upload API

### Objective

Allow the dashboard to upload recorded videos directly to the backend.

### Features Implemented

Created a dedicated Videos API.

Implemented:

```
POST /videos/upload
```

The API:

- Accepts uploaded videos using FastAPI's `UploadFile`.
- Saves uploaded videos inside the server's `uploads/` directory.
- Returns upload confirmation to the frontend.

### Upload Workflow

```
Dashboard
     │
     ▼
POST /videos/upload
     │
     ▼
FastAPI
     │
     ▼
uploads/
```

---

# 4. FastAPI Integration

### Objective

Integrate the Videos API into the existing backend.

### Features Implemented

- Registered the Videos router inside `main.py`.
- Included the Videos API in Swagger documentation (`/docs`).
- Resolved router registration issues.
- Fixed endpoint routing errors.
- Fixed HTTP 404 errors during upload requests.

---

# 5. Docker & Nginx Integration

### Objective

Allow large recorded videos to be uploaded successfully through Nginx.

### Features Implemented

- Updated Docker backend with the newly created Videos API.
- Rebuilt the backend container after code modifications.
- Configured Nginx to support larger upload sizes.

Added:

```nginx
client_max_body_size 100M;
```

This eliminated the previous upload limitation that caused:

```
413 Request Entity Too Large
```

### Result

Large video recordings can now be uploaded successfully through the Nginx reverse proxy.

---

# 6. Automatic Upload from Dashboard

### Objective

Remove the manual upload process and automate video uploading after recording.

### Features Implemented

After the user clicks **Stop Recording**:

- Recording Blob is created.
- Blob is wrapped inside a `FormData` object.
- JavaScript `fetch()` automatically uploads the video.
- Upload response is displayed on the dashboard.

### Complete Workflow

```
Stop Recording
        │
        ▼
Create Blob
        │
        ▼
Create FormData
        │
        ▼
fetch()
        │
        ▼
POST /videos/upload
```

This completely removes the need for manual uploads using Swagger.

---

# 7. PostgreSQL Integration

### Objective

Store metadata for every uploaded recording inside PostgreSQL.

### Features Implemented

- Used the existing SQLAlchemy configuration.
- Added `create_video()` to the CRUD layer.
- Inserted video metadata into the `videos` table after every successful upload.

### Metadata Stored

| Field | Status |
|--------|--------|
| filename | ✅ |
| filepath | ✅ |
| file_size | ✅ |
| uploaded_at | ✅ |
| duration | ⏳ Currently NULL |
| resolution | ⏳ Currently NULL |

### Database Workflow

```
Video Upload
      │
      ▼
Save Video File
      │
      ▼
Create Video Object
      │
      ▼
Insert into PostgreSQL
```

---

# 8. Database Verification

### Objective

Verify that uploaded recordings are successfully stored inside PostgreSQL.

### Features Implemented

- Connected to the PostgreSQL Docker container.
- Executed SQL queries using `psql`.
- Verified entries inside the `videos` table.
- Confirmed that every successful upload automatically creates a new database record.

Example Query

```sql
SELECT * FROM videos;
```

Example Result

```
id | filename | filepath | file_size | uploaded_at
--------------------------------------------------
1  | recording.webm | uploads/recording.webm | 2086283 | ...
2  | recording.webm | uploads/recording.webm | 1042311 | ...
```

---

# Overall System Architecture

```
Phone Camera
      │
      ▼
WebRTC Live Stream
      │
      ▼
Dashboard
      │
      ▼
MediaRecorder
      │
      ▼
Recorded Blob (.webm)
      │
      ▼
Automatic Upload (fetch)
      │
      ▼
FastAPI Upload API
      │
      ├────────────► uploads/
      │
      ▼
PostgreSQL
      │
      ▼
Video Metadata
```

---

# Technologies Used

- WebRTC
- MediaRecorder API
- JavaScript (Fetch API)
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Nginx
- Swagger/OpenAPI
