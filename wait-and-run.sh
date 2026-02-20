#!/bin/bash

# -------------------------------------------------------
# Wait for PostgreSQL to be ready, then run SQL commands
# -------------------------------------------------------

# Database connection variables (should match your Compose .env)
HOST="${POSTGRES_HOST:-db}"
PORT="${POSTGRES_PORT:-5432}"
USER="${POSTGRES_USER}"
DB="${POSTGRES_DB}"
PASS="${POSTGRES_PASSWORD}"

export PGPASSWORD="$PASS"

echo "Waiting for PostgreSQL at $HOST:$PORT ..."

# Loop until we can connect and run a simple command
until psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" -c "\q" > /dev/null 2>&1; do
  echo "PostgreSQL is unavailable — retrying in 1s..."
  sleep 1
done

echo "PostgreSQL is up! Running SQL …"

# Now run your SQL to create the vector extension
psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" \
     -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "Extension ensured, finishing script."
