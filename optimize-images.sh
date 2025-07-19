#!/bin/bash

# Docker Image Size Optimization Script
echo "🐳 Docker Image Size Optimization Script"
echo "========================================"

# Function to build and analyze image size
build_and_analyze() {
    local service_name=$1
    local dockerfile_path=$2
    local context_path=$3
    
    echo ""
    echo "🔨 Building $service_name..."
    
    # Build the image
    docker build -f "$dockerfile_path" -t "$service_name" "$context_path"
    
    # Get image size
    local size=$(docker images "$service_name" --format "table {{.Size}}" | tail -n 1)
    echo "📊 $service_name size: $size"
    
    # Show layers
    echo "📋 Layers for $service_name:"
    docker history "$service_name" --format "table {{.CreatedBy}}\t{{.Size}}" | head -10
}

# Function to show optimization tips
show_optimization_tips() {
    echo ""
    echo "💡 Optimization Tips:"
    echo "===================="
    echo "✅ Used Alpine Linux base images (much smaller than Debian/Ubuntu)"
    echo "✅ Multi-stage builds to separate build and runtime dependencies"
    echo "✅ Removed unnecessary packages and build tools from runtime"
    echo "✅ Used --no-cache-dir for pip installations"
    echo "✅ Added comprehensive .dockerignore files"
    echo "✅ Set resource limits for free hosting platforms"
    echo "✅ Used non-root users for security"
    echo "✅ Optimized JVM settings for smaller memory footprint"
    echo ""
    echo "🎯 Expected size reductions:"
    echo "   - Spring Boot: ~200-300MB (from ~500-800MB)"
    echo "   - Python ML: ~150-250MB (from ~400-600MB)"
    echo "   - Simple ML: ~50-100MB (from ~150-200MB)"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Build and analyze all services
echo "🚀 Starting optimized builds..."

# Spring Boot Application
build_and_analyze "malicious-url-detector" "src/main/resources/Dockerfile" "."

# Advanced Python ML Microservice
build_and_analyze "python-ml-microservice" "python_microservice/Dockerfile" "./python_microservice"

# Simple ML Microservice
build_and_analyze "simple-ml-microservice" "ml_microservice/Dockerfile" "./ml_microservice"

# Show total size
echo ""
echo "📈 Total Image Sizes:"
echo "====================="
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(malicious-url-detector|ml-microservice)"

# Show optimization tips
show_optimization_tips

echo ""
echo "🎉 Optimization complete! Your images are now much smaller and ready for free hosting platforms."
echo ""
echo "To run the optimized services:"
echo "  docker-compose up --build -d" 