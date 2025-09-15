#!/bin/bash

# Start script for PentryPal API on Railway
# This script handles the PORT environment variable properly

# Set default port if PORT is not set
if [ -z "$PORT" ]; then
    PORT=8000
fi

# Debug: Print the PORT value (remove this line after confirming it works)
echo "Using PORT: $PORT"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
