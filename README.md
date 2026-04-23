# AidMatch Backend

AidMatch is a friction-based donation platform backend built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT auth, and Firebase Cloud Messaging.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT Auth
- Firebase Cloud Messaging

## Features

- Admin authentication
- Donor authentication
- Campaign creation and lookup by public code
- Item requirement management
- Donation recommendation engine
- Donation submission flow
- Admin receive / reject / mark used
- Item stock + remaining need calculation
- Notification storage + optional FCM push

## Project Structure

See the app folders for:
- core config
- models
- schemas
- APIs
- services
- utilities
- seed script

## Run locally

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate