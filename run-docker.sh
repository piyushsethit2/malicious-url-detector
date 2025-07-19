#!/bin/bash

# Malicious URL Detector - Docker Runner Script

echo "🚀 Starting Malicious URL Detector with Docker Compose..."

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start the services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."

# Check Spring Boot app
if curl -s http://localhost:8080/actuator/health > /dev/null; then
    echo "✅ Spring Boot application is running on http://localhost:8080"
else
    echo "❌ Spring Boot application is not responding"
fi

# Check ML microservice
if curl -s http://localhost:5002/health > /dev/null; then
    echo "✅ ML microservice is running on http://localhost:5002"
else
    echo "❌ ML microservice is not responding"
fi

echo ""
echo "🎉 Services are ready!"
echo ""
echo "📋 Available endpoints:"
echo "   • Main API: http://localhost:8080/api/scan"
echo "   • ML Service: http://localhost:5002/predict"
echo "   • Health Check: http://localhost:8080/actuator/health"
echo ""
echo "🧪 Test with: curl -X POST 'http://localhost:8080/api/scan?url=https://www.google.com'"
echo ""
echo "🛑 To stop: docker-compose down" 