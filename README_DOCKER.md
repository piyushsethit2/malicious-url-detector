# Malicious URL Detector - Docker Setup

This document provides instructions for running the Malicious URL Detector application using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### Option 1: Using the provided script (Recommended)

```bash
./run-docker.sh
```

This script will:
- Stop any existing containers
- Build and start both services
- Wait for services to be ready
- Display health status
- Show available endpoints

### Option 2: Manual Docker Compose

```bash
# Build and start services
docker-compose up --build -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Services

The application consists of two services:

### 1. Spring Boot Application (Port 8080)
- Main API endpoint: `http://localhost:8080/api/scan`
- Health check: `http://localhost:8080/actuator/health`
- Container name: `malicious-url-detector`

### 2. ML Microservice (Port 5002)
- ML prediction endpoint: `http://localhost:5002/predict`
- Health check: `http://localhost:5002/health`
- Container name: `ml-microservice`

## Testing the Application

### Test a safe URL
```bash
curl -X POST "http://localhost:8080/api/scan?url=https://www.google.com"
```

### Test a potentially malicious URL
```bash
curl -X POST "http://localhost:8080/api/scan?url=br-icloud.com.br"
```

### Test the ML microservice directly
```bash
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

## Docker Images

### Spring Boot Application
- **Base Image**: `eclipse-temurin:21-jre`
- **Build Image**: `maven:3.9.6-eclipse-temurin-21`
- **Multi-stage build** for optimized image size
- **JVM Options**: `-Xmx512m -Xms256m`

### ML Microservice
- **Base Image**: `python:3.9-slim`
- **Dependencies**: Installed via `requirements.txt`
- **Health Check**: Automatic health monitoring
- **Model**: Downloads `distilbert-base-uncased` at runtime

## Environment Variables

### Spring Boot Application
- `SPRING_PROFILES_ACTIVE=docker`
- `ML_MICROSERVICE_URL=http://ml-microservice:5002`

### ML Microservice
- `PORT=5002`
- `HF_MODEL_NAME=distilbert-base-uncased`

## Troubleshooting

### Check container status
```bash
docker-compose ps
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs malicious-url-detector
docker-compose logs ml-microservice
```

### Restart services
```bash
docker-compose restart
```

### Clean up
```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete images
docker-compose down --rmi all

# Stop, remove containers, images, and volumes
docker-compose down --rmi all -v
```

## Development

### Rebuild after code changes
```bash
docker-compose up --build -d
```

### Access container shell
```bash
# Spring Boot container
docker-compose exec malicious-url-detector sh

# ML microservice container
docker-compose exec ml-microservice bash
```

## Performance

- **Memory**: Each container uses ~512MB RAM
- **Startup Time**: ~30-60 seconds for full initialization
- **Model Loading**: ML model downloads on first run (~268MB)

## Security Notes

- Services communicate over internal Docker network
- No sensitive data exposed in container images
- ML model downloaded from Hugging Face at runtime
- Health checks ensure service availability 