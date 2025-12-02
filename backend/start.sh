#!/bin/bash
set -e

echo "🚀 Starting Neusearch Backend..."

# Run database migrations and seed
if [ -n "$DATABASE_URL" ]; then
    echo "📦 Seeding database with demo products..."
    python seed_db.py "$DATABASE_URL" || echo "⚠️  Seed skipped or failed (non-fatal)"
fi

# Start the FastAPI server
# PORT is provided by Render/Railway; default to 8000 for local
PORT=${PORT:-8000}
echo "🌐 Starting server on port $PORT..."

exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
