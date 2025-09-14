#!/bin/bash

# Start script for PentryPal API on Railway
# This script handles the PORT environment variable properly

# Set default port if PORT is not set
PORT=${PORT:-8000}

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
