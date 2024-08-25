#!/bin/bash

echo "Starting migrations..."
alembic upgrade head
MIGRATION_STATUS=$?
if [ $MIGRATION_STATUS -ne 0 ]; then
  echo "Migrations failed with status $MIGRATION_STATUS"
  exit 1
fi

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
