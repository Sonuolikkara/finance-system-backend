# Finance System Backend

A simple finance tracking backend built with Python. Track income, expenses, users with different roles, and view financial summaries.

## What's in here?

- **Transaction CRUD** - Add, edit, delete, view your transactions
- **Filtering** - Filter by type, category, or date range
- **Financial Summary** - See total income, expenses, and balance at a glance
- **Multiple users with roles** - Viewer (read-only), Analyst (can filter and analyze), Admin (full control)
- **Simple API** - REST API with automatic documentation
- **SQLite database** - No setup needed, database is created automatically

## Tech Stack

- FastAPI (Python web framework)
- SQLite (database)
- SQLAlchemy (database ORM)
- Pydantic (validation)

## Setup & Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the server
```bash
python -m uvicorn main:app --reload
```

The API will be running at `http://localhost:8000`

Visit `http://localhost:8000/docs` to see the interactive API documentation where you can test everything.

## API Endpoints

### Users (Admin only)
- `POST /users/` - Create user
- `GET /users/` - List all users
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user role
- `DELETE /users/{id}` - Delete user

### Transactions
- `POST /transactions/` - Add transaction (admin)
- `GET /transactions/` - List user's transactions (all roles)
- `GET /transactions/{id}` - Get transaction details (all roles)
- `PUT /transactions/{id}` - Edit transaction (admin)
- `DELETE /transactions/{id}` - Delete transaction (admin)
- `GET /transactions/filter?category=food&type=expense` - Filter transactions (analyst+)

### Analytics (Analyst+)
- `GET /analytics/summary?user_id=1` - Total income, expenses, balance
- `GET /analytics/category-wise?user_id=1` - Breakdown by category
- `GET /analytics/monthly?user_id=1` - Breakdown by month

## User Roles

- **Viewer**: Can view transactions only. No filtering or analytics access.
- **Analyst**: Can view, filter transactions, and access analytics.
- **Admin**: Full access. Can create/edit/delete anything.

Pass the role in the request: `?user_role=admin`

## How it's organized

- `main.py` - FastAPI app setup
- `models.py` - User and Transaction database models
- `schemas.py` - Validation schemas
- `database.py` - Database config
- `crud.py` - Database operations
- `routes/` - API endpoints
- `utils/auth.py` - Role permission checks

## Notes

- Using SQLite so there's no setup needed. Database file is created automatically.
- Role is passed as a query parameter (for simplicity in this project)
- Amount must be positive
- Type must be either "income" or "expense"
- All endpoints return proper HTTP status codes (200, 201, 400, 403, 404, etc.)

