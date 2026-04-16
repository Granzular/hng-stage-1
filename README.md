# hng-stage-1
This repository contains HNG internship stage 1 project. This is the task given for stage 1


# Backend Wizards – Stage 1: Data Persistence & API Design

## Overview
This project implements a backend service that:
- Accepts a name as input
- Fetches data from three external APIs
- Applies classification logic
- Stores the result in a database
- Exposes RESTful endpoints to manage the data

The system enforces **idempotency**, ensuring that duplicate names do not create multiple records.

---

## Repository
https://github.com/Granzular/hng-stage-1

---

## External APIs Used

- Genderize: https://api.genderize.io?name={name}
- Agify: https://api.agify.io?name={name}
- Nationalize: https://api.nationalize.io?name={name}

---

## Features

- Multi-API integration
- Data persistence with a relational database
- Idempotent profile creation
- Filtering support on list endpoint
- Strict error handling and response format
- UUID v7 for primary keys
- UTC ISO 8601 timestamps

---

## Data Model

**Profile**
- `id` (UUID v7)
- `name` (unique, case-insensitive)
- `gender`
- `gender_probability`
- `sample_size`
- `age`
- `age_group`
- `country_id`
- `country_probability`
- `created_at` (UTC timestamp)

---

## Classification Logic

### Age Group (from Agify)
- 0–12 → child
- 13–19 → teenager
- 20–59 → adult
- 60+ → senior

### Nationality (from Nationalize)
- Select the country with the highest probability

---

## API Endpoints

### 1. Create Profile
**POST** `/api/profiles`

**Request Body**
```json
{ "name": "ella" }
```

**Success (201 Created)**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "DRC",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

**If profile already exists**
```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { ... }
}
```

---

### 2. Get Single Profile
**GET** `/api/profiles/{id}`

**Success (200)**
```json
{
  "status": "success",
  "data": { ... }
}
```

---

### 3. Get All Profiles
**GET** `/api/profiles`

**Query Parameters (optional)**
- `gender`
- `country_id`
- `age_group`

**Example**
```
/api/profiles?gender=male&country_id=NG
```

**Success (200)**
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "id-1",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG"
    }
  ]
}
```

---

### 4. Delete Profile
**DELETE** `/api/profiles/{id}`

**Success**
- `204 No Content`

---

## Error Handling

All errors follow this structure:
```json
{ "status": "error", "message": "<error message>" }
```

### Error Types

- **400 Bad Request** → Missing or empty name
- **422 Unprocessable Entity** → Invalid type
- **404 Not Found** → Profile not found
- **502 Bad Gateway** → External API failure

### External API Failure Format
```json
{ "status": "error", "message": "Genderize returned an invalid response" }
```

---

## Edge Case Handling

- Genderize returns `gender = null` or `count = 0` → reject
- Agify returns `age = null` → reject
- Nationalize returns no country data → reject

No data is stored if any external API response is invalid.

---

## Idempotency

- Profiles are unique by `name`
- Duplicate requests return existing data instead of creating a new record

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Granzular/hng-stage-1
cd hng-stage-1
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Run Server
```bash
python manage.py runserver
```

---

## CORS Configuration

```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

## Deployment

The application can be deployed on:
- Railway
- Vercel
- AWS
- Heroku

Ensure:
- The API is publicly accessible
- All endpoints are tested
- CORS is properly configured

---

## Testing

You can test endpoints using:
- Postman
- curl
- Browser (for GET endpoints)

---

## Submission

Provide:
- API Base URL
- GitHub Repository Link

Ensure the server is live and accessible before submission.

---

## Notes

- All timestamps are in UTC (ISO 8601)
- Response structure must match specification exactly
- UUID v7 is used for all IDs
- Filtering is case-insensitive

---
