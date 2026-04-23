#!/usr/bin/env bash
set -o errexit

alembic upgrade head
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT