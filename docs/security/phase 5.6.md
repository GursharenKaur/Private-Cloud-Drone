# Phase 5.6 — Upload Security & Secure Media Handling

**Project:** Private Cloud for Secure Drone Flight  
**Phase:** 5.6  
**Status:** ✅ Completed

---

# Objective

The objective of Phase 5.6 is to secure all media upload endpoints by implementing a centralized upload security framework.

Prior to this phase, both video and image uploads accepted files with minimal validation. This exposed the backend to multiple security risks including malicious file uploads, oversized payloads, spoofed content types, filename manipulation, and storage conflicts.

This phase introduces a reusable upload security layer that validates every uploaded file before it is stored in the system.

The implementation follows the existing layered security architecture established throughout Phase 5 and avoids duplicating validation logic across endpoints.

---

# Security Goals

The upload pipeline should guarantee that:

- Only supported file extensions are accepted.
- Only supported MIME types are accepted.
- Uploaded files remain within configured size limits.
- Stored filenames cannot be manipulated by clients.
- Upload validation is centralized.
- Existing architecture remains unchanged.

---

# Threat Model

This phase addresses several common upload vulnerabilities.

## 1. Malicious File Uploads

Attackers may rename executable files to appear as media.

Example:

```
malware.exe
↓

malware.mp4
```

Extension validation helps reject unsupported file types.

---

## 2. MIME Type Spoofing

Clients may attempt to upload unexpected content types.

Example:

```
application/octet-stream
```

instead of

```
video/webm
```

The backend now validates the received MIME type before processing uploads.

---

## 3. Oversized Uploads

Very large files may exhaust memory, disk space, or bandwidth.

Configured limits now prevent excessive uploads.

---

## 4. Filename Injection

Previously filenames originated directly from client input.

Examples:

```
../../../etc/passwd

recording.mp4

../../malware.exe
```

The backend now ignores client filenames and generates secure UUID-based filenames.

---

## 5. Filename Collisions

Uploading identical filenames previously caused collisions.

Example:

```
recording.webm

recording.webm
```

UUID filenames completely eliminate this problem.

---

# Architecture

The upload security layer follows the existing layered security model.

```
User / Device
        │
        ▼
Authentication
        │
        ▼
Authorization
        │
        ▼
Upload Security
        │
 ├── Extension Validation
 ├── MIME Validation
 ├── File Size Validation
 ├── Secure Filename Generation
        │
        ▼
Storage
        │
        ▼
Database
```

The validation layer is shared by both video and image uploads.

---

# Centralized Upload Security

A new reusable module was created:

```
app/core/upload_security.py
```

This module contains all upload-related security functions.

No endpoint performs upload validation independently.

---

# Implemented Features

## 1. File Extension Validation

Supported video extensions:

```
.webm
.mp4
.mov
```

Supported image extensions:

```
.jpg
.jpeg
.png
```

Validation function:

```python
validate_file_extension()
```

Uploads with unsupported extensions immediately return HTTP 400.

Example:

```
malware.exe

↓

400 Bad Request
```

---

## 2. MIME Type Validation

Supported video MIME types:

```
video/webm
video/mp4
video/quicktime
```

Supported image MIME types:

```
image/jpeg
image/png
```

Validation function:

```python
validate_mime_type()
```

This prevents clients from uploading unsupported content types.

---

## 3. File Size Validation

Maximum video size:

```
500 MB
```

Maximum image size:

```
10 MB
```

Validation function:

```python
validate_file_size()
```

After validation, the file pointer is reset using:

```python
await file.seek(0)
```

allowing the endpoint to read the file normally afterwards.

---

## 4. Secure Filename Generation

A centralized helper generates UUID filenames.

Function:

```python
generate_secure_filename()
```

Instead of storing

```
recording.webm
```

the backend stores

```
4d3cde62-b18b-4fd7-97fe-2f69fa58c55b.webm
```

Benefits:

- Prevents filename collisions.
- Removes trust in client filenames.
- Prevents filename manipulation.
- Keeps original extension.

---

# Video Upload Security

The video upload endpoint now performs:

```
Authenticate User
        │
Authorize Device
        │
Validate Extension
        │
Validate MIME Type
        │
Validate File Size
        │
Generate Secure Filename
        │
Store File
        │
Create Database Record
```

---

# Image Upload Security

The image upload endpoint now performs:

```
Authenticate Device
        │
Authorize Device
        │
Validate Extension
        │
Validate MIME Type
        │
Validate File Size
        │
Generate Secure Filename
        │
Store File
        │
Create Database Record
```

---

# Files Modified

## Core

```
app/core/upload_security.py
```

Added:

- Extension validation
- MIME validation
- File size validation
- UUID filename generation

---

## Video API

```
app/api/videos.py
```

Integrated:

- Extension validation
- MIME validation
- File size validation
- UUID filenames

---

## Image API

```
app/api/images.py
```

Integrated:

- Extension validation
- MIME validation
- File size validation
- UUID filenames

---

# Security Flow

## Video Upload

```
Upload Request
        │
Authenticate User
        │
Authorize Device
        │
Extension Validation
        │
MIME Validation
        │
File Size Validation
        │
UUID Filename
        │
Store File
        │
Database Entry
```

---

## Image Upload

```
Upload Request
        │
Authenticate Device
        │
Authorize Device
        │
Extension Validation
        │
MIME Validation
        │
File Size Validation
        │
UUID Filename
        │
Store File
        │
Database Entry
```

---

# Testing Performed

## Video Upload

### Valid Upload

Result:

✅ Successful upload

---

### Invalid Extension

Uploaded:

```
malware.exe
```

Result:

```
Unsupported file extension
```

---

### Invalid MIME Type

Uploaded:

```
application/octet-stream
```

Result:

```
Unsupported MIME type
```

---

### Oversized Upload

Uploaded:

```
600 MB
```

Result:

```
File size exceeds maximum allowed limit
```

---

### Secure Filename

Original:

```
recording.webm
```

Stored:

```
4d3cde62-b18b-4fd7-97fe-2f69fa58c55b.webm
```

---

# Image Upload

### Valid Upload

Result:

✅ Successful upload

---

### Invalid Extension

Uploaded:

```
malware.exe
```

Result:

```
Unsupported file extension
```

---

### Oversized Image

Uploaded:

```
20 MB
```

Result:

```
File size exceeds maximum allowed limit
```

---

### Secure Filename

Original:

```
Screenshot.png
```

Stored:

```
cd0fceeb-4908-40f1-96b1-ed2d50a4e706.png
```

---

# Security Improvements Achieved

This phase introduces:

- Centralized upload validation.
- Reusable validation helpers.
- Secure UUID-based storage.
- Protection against filename manipulation.
- Protection against oversized uploads.
- Consistent validation for both media types.
- Reduced code duplication.

---

# Limitations

Current MIME validation relies on the client-provided `Content-Type` header.

Although this blocks many invalid uploads, it should not be considered fully trustworthy because clients can spoof MIME types.

---

# Future Improvements (Phase 5.7+)

Potential enhancements include:

- Magic byte (file signature) validation.
- Antivirus scanning before storage.
- Malware detection pipeline.
- Content hashing (SHA-256).
- Duplicate file detection.
- Object storage integration (MinIO/S3).
- Quarantine area for suspicious uploads.
- Upload rate limiting.
- Audit logging for uploads.
- Background media processing.

---

# Outcome

Phase 5.6 successfully introduces a centralized and reusable upload security framework for the Private Cloud Drone platform.

All media uploads are now validated before storage using a consistent pipeline that enforces extension checks, MIME validation, file size limits, and secure UUID-based filenames.

This implementation integrates cleanly with the authentication and authorization layers developed in previous phases and establishes a strong foundation for future security hardening.