#!/bin/bash

set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    while ! pg_isready -h db -p 5432 -U tensorone; do
        sleep 1
    done
    echo "Database is ready!"
}

# Function to wait for Redis
wait_for_redis() {
    echo "Waiting for Redis to be ready..."
    while ! redis-cli -h redis ping > /dev/null 2>&1; do
        sleep 1
    done
    echo "Redis is ready!"
}

# Install PostgreSQL client if not available
if ! command -v pg_isready &> /dev/null; then
    echo "Installing PostgreSQL client..."
    apk add --no-cache postgresql-client
fi

# Install Redis client if not available
if ! command -v redis-cli &> /dev/null; then
    echo "Installing Redis client..."
    apk add --no-cache redis
fi

# Wait for dependencies
if [ "$NODE_ENV" = "production" ]; then
    wait_for_db
    wait_for_redis
fi

# Create logs directory
mkdir -p /app/logs

# Set proper permissions
chmod -R 755 /app/logs

echo "Starting application..."
exec "$@"