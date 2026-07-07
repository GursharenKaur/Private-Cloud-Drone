# Phase 4 – Video Recording, Storage & Recording Management

---

# Overview

The objective of Phase 4 was to transform the existing WebRTC live streaming application into a complete video recording and management system.

This phase introduced:

- Live stream recording
- Automatic video uploads
- Video storage on the server
- PostgreSQL metadata storage
- Recording archive
- Video playback
- Video download
- Video deletion
- Dashboard navigation
- Recording statistics

At the end of this phase, the application supports the complete lifecycle of recorded drone footage.

---

# Phase 4 Architecture

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
Recorded Video (.webm)
      │
      ▼
Automatic Upload
      │
      ▼
FastAPI
      │
      ├────────────► uploads/
      │
      ▼
PostgreSQL
      │
      ▼
Recording Archive
      │
      ├────────► Play
      ├────────► Download
      └────────► Delete
```

---

# 1. Live Stream Recording

## Objective

Allow the dashboard to record the incoming WebRTC video stream.

## Features Implemented

- Added **Start Recording** button.
- Added **Stop Recording** button.
- Integrated MediaRecorder API.
- Recorded the remote WebRTC stream.
- Captured data chunks using `ondataavailable`.
- Combined chunks into a `.webm` video Blob.

### Workflow

```
Remote Stream
      │
      ▼
MediaRecorder
      │
      ▼
Video Chunks
      │
      ▼
Blob (.webm)
```

---

# 2. Automatic Download

## Objective

Allow users to immediately download every recording.

## Features Implemented

- Created Blob URLs.
- Triggered automatic browser download.
- Verified downloaded recordings.

Workflow

```
Stop Recording
      │
      ▼
Create Blob
      │
      ▼
Download Video
```

---

# 3. Automatic Upload

## Objective

Upload recordings automatically without Swagger.

## Features Implemented

- Created FormData.
- Uploaded using Fetch API.
- Removed manual upload workflow.

Workflow

```
Recording
     │
     ▼
FormData
     │
     ▼
POST /videos/upload
```

---

# 4. Backend Video Upload API

Created:

```
POST /videos/upload
```

Features

- UploadFile support
- Automatic server-side storage
- Upload confirmation
- Unique filenames

Videos are stored inside:

```
uploads/
```

---

# 5. Unique Timestamped Filenames

Originally recordings were saved as:

```
recording.webm
```

which caused every new upload to overwrite the previous recording.

This was improved by generating timestamp-based filenames.

Example

```
20260707_163522_recording.webm
```

Benefits

- Prevents overwriting
- Preserves recording history
- Easier identification

---

# 6. PostgreSQL Integration

Every uploaded recording automatically creates a database record.

Stored metadata

| Field | Status |
|--------|--------|
| id | ✅ |
| filename | ✅ |
| filepath | ✅ |
| file_size | ✅ |
| uploaded_at | ✅ |
| duration | Placeholder |
| resolution | Placeholder |

Workflow

```
Upload
   │
   ▼
Save File
   │
   ▼
Create SQLAlchemy Object
   │
   ▼
Insert PostgreSQL Record
```

---

# 7. Recording Retrieval API

Created

```
GET /videos/
```

Purpose

Return every stored recording.

Returned information

- id
- filename
- filepath
- upload time
- size
- duration
- resolution

---

# 8. Video Streaming API

Created

```
GET /videos/{video_id}/stream
```

Purpose

Play recordings directly inside the application.

Instead of downloading recordings, the frontend now streams them using HTML5 Video.

Workflow

```
Click Play
      │
      ▼
GET /videos/{id}/stream
      │
      ▼
FastAPI
      │
      ▼
HTML5 Video Player
```

---

# 9. Video Delete API

Created

```
DELETE /videos/{video_id}
```

Features

Deletes:

- physical video file
- PostgreSQL metadata

Workflow

```
Delete Request
       │
       ▼
Find Video
       │
       ▼
Delete uploads/video.webm
       │
       ▼
Delete Database Row
```

---

# 10. Docker & Nginx Integration

Updated backend image.

Rebuilt Docker containers.

Configured

```nginx
client_max_body_size 100M;
```

Resolved

```
413 Request Entity Too Large
```

---

# 11. Dashboard Improvements

The dashboard now contains

- Live video
- Start Recording
- Stop Recording
- Connection Status
- View Recordings navigation button

The dashboard is dedicated to live monitoring.

---

# 12. Recordings Archive

Created an entirely new page

```
/recordings
```

Purpose

Separate recording management from live monitoring.

Features

- Recording archive
- Video playback
- Download
- Delete
- Statistics

---

# 13. Recording Statistics

Implemented dashboard statistics.

Displayed information

- Total recordings
- Total storage used

Statistics update automatically after upload or deletion.

---

# 14. Embedded Video Player

Added HTML5 Video Player.

Features

- Stream recordings
- No download required
- Play inside browser

Workflow

```
Select Recording
      │
      ▼
Load Stream URL
      │
      ▼
Play Video
```

---

# 15. Recording Download

Added Download button.

Workflow

```
Download Button
       │
       ▼
GET /videos/{id}/stream
       │
       ▼
Browser Download
```

---

# 16. Recording Deletion

Added Delete button.

Features

- Confirmation dialog
- Deletes recording
- Removes database record
- Removes physical file
- Refreshes UI
- Updates statistics

Workflow

```
Delete
   │
   ▼
DELETE API
   │
   ▼
Backend
   │
   ▼
Delete File
   │
   ▼
Delete Database Row
   │
   ▼
Reload Archive
```

---

# 17. Frontend Improvements

Dashboard

- Clean monitoring interface
- Navigation to recordings

Recordings Page

- Professional recording cards
- Statistics
- Embedded player
- Download button
- Delete button
- Responsive layout

---

# 18. Overall Recording Lifecycle

```
Phone Camera
      │
      ▼
WebRTC Stream
      │
      ▼
Dashboard
      │
      ▼
Start Recording
      │
      ▼
MediaRecorder
      │
      ▼
Stop Recording
      │
      ▼
Video Blob
      │
      ▼
Automatic Upload
      │
      ▼
FastAPI
      │
      ├────────► uploads/
      │
      ▼
PostgreSQL
      │
      ▼
Recordings Page
      │
      ├────────► Play
      ├────────► Download
      └────────► Delete
```

---

# Technologies Used

- WebRTC
- MediaRecorder API
- HTML5 Video
- JavaScript (ES6)
- Fetch API
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Nginx
- Swagger / OpenAPI

---

# Phase 4 Outcome

Phase 4 successfully transformed the project from a live video streaming application into a complete video recording and management platform.

The application now supports:

- Live drone monitoring
- Video recording
- Automatic upload
- Server-side storage
- Database metadata
- Recording archive
- Embedded playback
- Video download
- Video deletion
- Recording statistics
- Full CRUD management for recorded videos