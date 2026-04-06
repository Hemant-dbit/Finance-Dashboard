# Finance Dashboard API

A RESTful Finance Management API built with Django and Django REST Framework. It provides secure authentication, transaction tracking, role-based access control, and analytics for income and expenses.

---

## 📌 Live API Documentation

https://finance-dashboard-2uu5.onrender.com/api/docs/

---

## 🚀 Features

- JWT Authentication (Login / Register / Refresh)
- Income & Expense tracking
- Role-based access control (Viewer, Analyst, Admin)
- Category-based transaction organization
- Filtering, searching, and ordering support
- Financial dashboard analytics
- Soft delete support for safer data handling

---

## 🛠 Tech Stack

- Django 5.x
- Django REST Framework
- SimpleJWT (Authentication)
- PostgreSQL (Production), SQLite (Development)
- Gunicorn (Server)
- django-filter
- python-decouple

## Project Structure

```
finance-dashboard/backend/
├── config/
│   ├── settings/
│   │   ├── base.py         (shared settings)
│   │   ├── development.py  (DEBUG=True, SQLite)
│   │   └── production.py   (PostgreSQL, no DEBUG)
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/          (BaseModel, permissions, exceptions)
│   ├── users/         (User auth, roles)
│   ├── transactions/  (Transaction CRUD, categories)
│   └── analytics/     (Dashboard, summaries)
├── manage.py
├── requirements.txt
├── pytest.ini
├── db.sqlite3
├── .env.example
└── runtime.txt
```

---

## Quick Start

### Prerequisites
- Python 3.11+, pip, virtualenv, Git

### Installation

```bash
# Clone repository
git clone <repo-url>
cd finance-dashboard

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r backend/requirements.txt

# Setup environment
cd backend
cp .env.example .env
# Edit .env with your config

# Create database & run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

API available at: `http://localhost:8000/api/v1/`  
Admin panel: `http://localhost:8000/admin/`

---

## User Roles

| Role | Permissions |
|------|-------------|
| **VIEWER** | View own transactions |
| **ANALYST** | View all transactions + analytics |
| **ADMIN** | Full CRUD + user management |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login/` | Obtain JWT access & refresh tokens |
| POST | `/auth/refresh/` | Refresh expired access token |
| POST | `/users/register/` | Register new user |
| GET | `/users/` | List all users (admin only) |
| GET | `/users/{id}/` | Get user details |
| PATCH | `/users/{id}/role/` | Update user role (admin only) |
| POST | `/transactions/` | Create transaction (admin only) |
| GET | `/transactions/` | List transactions (filtered by role) |
| PUT | `/transactions/{id}/` | Update transaction (admin only) |
| DELETE | `/transactions/{id}/` | Delete transaction - soft delete (admin only) |
| GET | `/dashboard/` | Get analytics & summary |

---





## Contributing

```bash
# Create feature branch
git checkout -b feature/your-feature

# Run tests
pytest

# Commit & push
git commit -m "Add feature"
git push origin feature/your-feature
```

---

## Resources

- **Django:** https://docs.djangoproject.com/
- **DRF:** https://www.django-rest-framework.org/
- **JWT:** https://django-rest-framework-simplejwt.readthedocs.io/


