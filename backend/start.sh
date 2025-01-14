#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Initializing the database..."
cd /app
python init_db.py

echo "Starting the FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
