# Finance Dashboard API

A backend system for managing financial records with role-based access control, built with FastAPI and SQLite.

## Tech Stack
- **Framework:** FastAPI (Python)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** Bcrypt

## Project Structure
finance-backend/
├── main.py                  # App entry point
├── database.py              # DB connection setup
├── requirements.txt         # All libraries
├── README.md                # Documentation
├── models/                  # Database tables
├── schemas/                 # Input/Output formats
├── routers/                 # API routes
├── services/                # Business logic
└── middleware/              # Auth and error handling

## Setup Instructions

### 1. Clone the project
```bash
cd finance-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Open API docs
http://127.0.0.1:8000/docspython -m http.server 5500

## API Endpoints

### Auth
- `POST /auth/register` - Create account (default: Viewer)
- `POST /auth/login` - Login and get JWT token

### Users
- `GET /users/me` - Get my profile
- `PATCH /users/me` - Update my profile
- `POST /users/request-role` - Request Analyst role

### Financial Records
- `POST /records/` - Create record (Admin only)
- `GET /records/` - View all records (pagination + filters)
- `GET /records/{id}` - View single record
- `PATCH /records/{id}` - Update record (Admin only)
- `DELETE /records/{id}` - Soft delete record (Admin only)

### Dashboard
- `GET /dashboard/summary` - Total income, expenses, balance
- `GET /dashboard/categories` - Category wise totals
- `GET /dashboard/trends` - Monthly trends
- `GET /dashboard/recent` - Recent activity

### Admin
- `GET /admin/users` - View all users
- `PATCH /admin/users/{id}/status` - Activate/Deactivate user
- `GET /admin/role-requests` - View pending requests
- `PATCH /admin/role-requests/{id}/approve` - Approve request
- `PATCH /admin/role-requests/{id}/reject` - Reject request
- `PATCH /admin/users/{id}/revoke` - Revoke analyst role

## Features
- ✅ JWT Authentication
- ✅ Role Based Access Control
- ✅ Soft Delete
- ✅ Pagination
- ✅ Dashboard with time period filters (1day, 1week, 1month, 3months, 6months, 1year, max)
- ✅ Input Validation
- ✅ Error Handling
- ✅ Auto API Documentation

## Assumptions
- Default role for new users is Viewer
- Only Viewers can request Analyst role
- Admin account is created manually for security
- Soft delete is used for records (data is never permanently lost)
- SQLite is used for simplicity (can be replaced with PostgreSQL for production)