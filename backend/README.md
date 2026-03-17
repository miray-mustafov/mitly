# Mitly Backend - API & Business Logic

This directory contains the FastAPI backend for the Mitly URL shortener.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Validation**: Pydantic
- **Testing**: Pytest
- **Package Manager**: `uv`

## Folder Structure

```shell
backend/
├── requirements/     # dependencies
├── src/              # source code
│   └── app/          
│       ├── api/      # API endpoints (v1, v2)
│       ├── config/   # Environment settings
│       ├── crud/     # Business logic & DB operations
│       ├── db/       # Models & Database setup
│       ├── schemas/  # Pydantic models
│       └── main.py   # Entry point
└── tests/            # Automated tests
```

## Key Technical Implementation

### N-Tier Architecture
The project follows a layered architecture to ensure separation of concerns:
- **Presentation Layer**: `app/api/` and `app/schemas/` handle HTTP requests and data validation.
- **Business Logic & Data Access**: `app/crud/` contains the core logic for URL shortening and database interactions.
- **Persistence Layer**: `app/db/` defines the database schema and session management.

### Base62 Encoding
We use a custom Base62 algorithm to generate short, URL-friendly identifiers from auto-incrementing database IDs. This ensures uniqueness and efficient ID generation.

## Setup & Development

### 1. Environment
Ensure you have `uv` installed.
```shell
uv venv --python 3.13
.venv\Scripts\activate
```

### 2. Configuration
Create a `.env` file based on `.env.example`.

### 3. Run the App
```shell
uv run mitly
```

### 4. Run Tests
```shell
uv run pytest
```
