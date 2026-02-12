# TrustScore KYC Decision & Document Workflow Platform

## 🚀 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Enigma1303/TrustScoreKYC
cd TrustScoreKYC
```

---

### 2. Create Environment File

Create a `.env` file in the project root with the following variables:

```env
DEBUG=1
SECRET_KEY=replace-me

DB_NAME=complaint_db
DB_USER=complaint_user
DB_PASSWORD=complaint_pass
DB_HOST=db
DB_PORT=5432
```

---

### 3. Build Docker Containers

```bash
docker-compose build
```

---

### 4. Start Services

```bash
docker-compose up
```

To run in detached mode(In Case Web Not starting):

```bash
docker-compose up -d
```

---

### 5. Apply Database Migrations

```bash
docker-compose exec web python manage.py migrate
```

---

### 6. Create Superuser (Admin)

```bash
docker-compose exec web python manage.py createsuperuser
```

---

### 7. Access API Documentation (Swagger)

Open in browser:

```
http://localhost:8000/swagger/
```

---

### 8. Run Test Suite

```bash
docker-compose exec web python manage.py test
```

---

## 📌 Notes

- Ensure Docker and Docker Compose are installed.
- If the `web` service is not running, start it using:

```bash
docker-compose up -d
```

- View application logs using:

```bash
docker-compose logs -f web
```

- View Stored files information 

```bash
docker-compose exec web ls /app/media/luc_documents
```

- To view stored files in browser
```bash
http://localhost:8000/media/luc_documents/<DocName>
```
---



# 📖 Project Documentation

## 🧩 Overview

This project simulates a production-style fintech KYC (Know Your Customer) backend system.

It implements:

- Role-based(USER/ADMIN) authentication using JWT
- KYC application workflow
- Document upload and media handling
- Trust score decision engine
- Status transition validation
- Audit History logging
- Advanced ordering, filtering and search
- Automated test coverage

---

## 🔐 Authentication & Roles

Authentication is implemented using **SimpleJWT**.

Supported roles:

- USER
- ADMIN

| Action | USER | ADMIN |
|--------|------|--------|
| Submit KYC | ✅ | ✅ |
| Upload Documents | ✅ | ✅ |
| View Own Applications | ✅ | ✅ |
| View All Applications | ❌ | ✅ |
| Change Status | ❌ | ✅ |
| Add Reviewer Comment | ❌ | ✅ |

---

## 🗂 Database Models


### 🛠 Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- MySQL (Dockerized)
- SimpleJWT (JWT Authentication)
- django-filter (Filtering & Search)
- drf-spectacular (OpenAPI / Swagger Documentation)
- Docker & Docker Compose


### User
- email
- password
- role (ADMIN / USER)

### KYCApplication
- user (ForeignKey)
- current_status
- created_at
- trust_score
- risk_level

### DocumentUpload
- application (ForeignKey)
- document_type
- file
- uploaded_at

### StatusHistory (Audit Log)
- application (ForeignKey)
- old_status
- new_status
- changed_by
- changed_at

### ReviewerComment
- application (ForeignKey)
- reviewer (Admin ForeignKey)
- comment_text
- created_at

---

## 🔄 Workflow States

Applications move through the following states:

- SUBMITTED
- IN_REVIEW
- APPROVED
- REJECTED

Status transitions are validated using defined business rules in the services folder

## 🔄 Allowed Workflow Transitions

| Current Status | Allowed Next Status |
|----------------|---------------------|
| SUBMITTED     | IN_REVIEW           |
| IN_REVIEW     | APPROVED, REJECTED  |
| APPROVED      | — (Final State)     |
| REJECTED      | SUBMITTED           |


All status changes are recorded in `StatusHistory`.

---

## 👤 User Features

- Submit new KYC application
- Upload multiple documents
- View application status
- View decision history
- Resubmit rejected applications

---

## 🛡 Admin Features

- View all submitted applications
- Filter,Order and search applications
- View pending reviews (SUBMITTED + IN_REVIEW)
- Change application status
- Add reviewer comments
- All actions logged in StatusHistory

---

## 🏗 Infrastructure & Database

The application is containerized using Docker Compose.

Services:

- **Web Service** – Django REST Framework API
- **Database Service** – MySQL 8.0 (Official Docker Image)

The database runs inside a Docker container and is configured via environment variables defined in the `.env` file.


## 🖼 Image Upload & Media Handling

- Multipart file upload supported
- Files stored using Django media storage inside Docker
- File URLs returned in API responses

---

## 📊 Trust Score Decision Engine

Trust score is calculated automatically based on:

1. Document completion ratio(Number of Documents submitted)
2. Number of resubmissions (penalty)
3. Profile consistency (account age-How old the account is)

### Example Output

```json
{
  "trust_score": 72,
  "risk_level": "MEDIUM"
}
```

### Risk Levels

- 80+ → LOW
- 50–79 → MEDIUM
- Below 50 → HIGH

---

## 🔎 Filtering & Querying & Ordering

Supported query features:

- Filter by `current_status`
- Sort by `created_at` or `trust_score`
- Search by user email
- Admin dashboard endpoint for pending applications

---

## 📝 Logging & Error Handling

- Structured logging configured
- Business validation errors return 4xx responses
- System errors logged and return 500 responses
- No silent exception handling
- Logs viewable using:

```bash
docker-compose logs -f web
```

---

## 🧪 Testing

Automated tests cover:

- User Authentication 
- User obtaining jwt token
- Submission workflow transitions
- Document upload functionality
- Status transition rules enforcement
- Admin vs User permission validation
- Trust score calculation logic


Run tests with:

```bash
docker-compose exec web python manage.py test
```

---

## 📚 API Documentation

Swagger UI available at:

```
http://localhost:8000/swagger/
```

Use Swagger to:

1. Register a user
2. Login to obtain JWT tokens
3. Authorize requests
4. Test the complete KYC workflow

---

## 🏁 Conclusion

This project demonstrates a production-style backend implementation of a KYC decision workflow platform with structured architecture, a decision engine, audit logging, role-based access control, and complete API documentation.
