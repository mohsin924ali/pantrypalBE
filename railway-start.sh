#!/bin/bash
set -e  # Exit on any error

echo "🚀 Starting PentryPal Backend on Railway..."

# Set port from Railway environment
PORT=${PORT:-8000}
echo "📡 Using PORT: $PORT"

# Wait for database to be ready (with timeout)
echo "🔄 Waiting for database..."
python3 -c "
import time
import sys
sys.path.insert(0, '.')

from app.core.config import settings
from sqlalchemy import create_engine, text

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        print('✅ Database is ready!')
        break
    except Exception as e:
        retry_count += 1
        print(f'⏳ Database not ready (attempt {retry_count}/{max_retries}): {str(e)}')
        if retry_count >= max_retries:
            print('❌ Database timeout - starting anyway')
            break
        time.sleep(2)
"

# Run migrations (with error handling)
echo "🔄 Running database migrations..."
python -m alembic upgrade head || echo "⚠️ Migration failed, continuing..."

# Initialize database with default data (with error handling) 
echo "🔄 Initializing database..."
python init_db.py || echo "⚠️ Database initialization failed, continuing..."

echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
