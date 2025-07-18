#!/bin/bash

set -e

# Default health check endpoint
HEALTH_ENDPOINT=${HEALTH_ENDPOINT:-"http://localhost:3000/"}

# Function to check if the application is responding
check_app_health() {
    echo "Checking application health at $HEALTH_ENDPOINT..."
    
    # Use curl to check if the application is responding
    if curl -f -s "$HEALTH_ENDPOINT" > /dev/null 2>&1; then
        echo "Application is healthy"
        return 0
    else
        echo "Application is not responding"
        return 1
    fi
}

# Function to check database connectivity
check_db_health() {
    if [ -n "$DATABASE_URL" ] || [ -n "$POSTGRES_HOST" ]; then
        echo "Checking database connectivity..."
        
        # Use environment variables or defaults
        DB_HOST=${POSTGRES_HOST:-db}
        DB_PORT=${POSTGRES_PORT:-5432}
        DB_USER=${POSTGRES_USER:-tensorone}
        
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; then
            echo "Database is accessible"
            return 0
        else
            echo "Database is not accessible"
            return 1
        fi
    fi
    return 0
}

# Function to check Redis connectivity
check_redis_health() {
    if [ -n "$REDIS_URL" ] || [ -n "$REDIS_HOST" ]; then
        echo "Checking Redis connectivity..."
        
        REDIS_HOST=${REDIS_HOST:-redis}
        REDIS_PORT=${REDIS_PORT:-6379}
        
        if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping > /dev/null 2>&1; then
            echo "Redis is accessible"
            return 0
        else
            echo "Redis is not accessible"
            return 1
        fi
    fi
    return 0
}

# Main health check
main() {
    echo "Starting health check..."
    
    # Check application health
    if ! check_app_health; then
        exit 1
    fi
    
    # Check database health (optional)
    if ! check_db_health; then
        echo "Warning: Database health check failed"
    fi
    
    # Check Redis health (optional)
    if ! check_redis_health; then
        echo "Warning: Redis health check failed"
    fi
    
    echo "Health check completed successfully"
    exit 0
}

# Run health check
main