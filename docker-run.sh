#!/bin/bash

# Open-Invest Docker Management Script

set -e

case "$1" in
    "build")
        echo "Building Docker image..."
        docker-compose build
        ;;
    "up")
        echo "Starting application..."
        docker-compose up -d
        ;;
    "down")
        echo "Stopping application..."
        docker-compose down
        ;;
    "logs")
        echo "Showing logs..."
        docker-compose logs -f
        ;;
    "restart")
        echo "Restarting application..."
        docker-compose restart
        ;;
    "clean")
        echo "Cleaning up Docker resources..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        ;;
    "dev")
        echo "Starting in development mode..."
        docker-compose up --build -d
        ;;
    "status")
        echo "Container status:"
        docker-compose ps
        ;;
    "test")
        echo "Testing API endpoints..."
        curl -s http://localhost:8000/health || echo "Health check failed"
        curl -s http://localhost:8000/ || echo "Root endpoint failed"
        ;;
    *)
        echo "Usage: $0 {build|up|down|logs|restart|clean|dev|status|test}"
        echo ""
        echo "Commands:"
        echo "  build   - Build the Docker image"
        echo "  up      - Start the application"
        echo "  down    - Stop the application"
        echo "  logs    - View application logs"
        echo "  restart - Restart the application"
        echo "  clean   - Clean up Docker resources"
        echo "  dev     - Start in development mode with rebuild"
        echo "  status  - Show container status"
        echo "  test    - Test the API endpoints"
        exit 1
        ;;
esac
