#!/bin/bash

echo "🚀 Starting Malicious URL Detector System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed or not in PATH"
    exit 1
fi

# Check if Maven is available
if ! command -v mvn &> /dev/null; then
    print_error "Maven is not installed or not in PATH"
    exit 1
fi

# Check if curl is available
if ! command -v curl &> /dev/null; then
    print_error "curl is not installed or not in PATH"
    exit 1
fi

print_success "Prerequisites check passed"

# Kill any existing processes
print_status "Stopping existing services..."

# Kill processes on specific ports
for port in 8080 5000 5001 5002; do
    if lsof -ti tcp:${port} > /dev/null 2>&1; then
        print_warning "Killing process on port ${port}"
        lsof -ti tcp:${port} | xargs kill -9 2>/dev/null || true
    fi
done

# Kill any old python ML microservice processes
pkill -f "python3.*ml_microservice.py" 2>/dev/null || true

# Kill any Spring Boot processes
pkill -f "spring-boot:run" 2>/dev/null || true

sleep 3

# Check if python_microservice directory exists
if [ ! -d "python_microservice" ]; then
    print_error "python_microservice directory not found"
    exit 1
fi

# Check if ml_microservice.py exists
if [ ! -f "python_microservice/ml_microservice.py" ]; then
    print_error "ml_microservice.py not found in python_microservice directory"
    exit 1
fi

# Check if requirements are installed
print_status "Checking Python dependencies..."
cd python_microservice
if ! python3 -c "import flask, transformers, torch" 2>/dev/null; then
    print_warning "Python dependencies not found. Installing..."
    pip3 install flask transformers torch requests 2>/dev/null || {
        print_error "Failed to install Python dependencies"
        exit 1
    }
fi
cd ..

print_success "Dependencies check passed"

# Start the ML microservice on port 5002
print_status "Starting ML microservice on port 5002..."
cd python_microservice
nohup python3 ml_microservice.py --port 5002 > ../ml_microservice.log 2>&1 &
ML_PID=$!
cd ..

# Wait for ML microservice to be ready
print_status "Waiting for ML microservice to be ready..."
for i in {1..15}; do
    sleep 2
    if curl -s http://localhost:5002/health > /dev/null 2>&1; then
        print_success "ML microservice is up and running on port 5002"
        break
    fi
    if [ $i -eq 15 ]; then
        print_error "ML microservice failed to start within 30 seconds"
        print_status "Checking ML microservice logs..."
        tail -n 10 ml_microservice.log 2>/dev/null || echo "No log file found"
        exit 1
    fi
done

# Test ML microservice with a simple request
print_status "Testing ML microservice..."
TEST_RESPONSE=$(curl -s -X POST "http://localhost:5002/predict" \
    -H "Content-Type: application/json" \
    -d '{"url":"https://www.google.com"}' 2>/dev/null)

if echo "$TEST_RESPONSE" | grep -q "label"; then
    print_success "ML microservice is responding correctly"
else
    print_warning "ML microservice test failed, but continuing..."
fi

# Start the Spring Boot app
print_status "Starting Spring Boot application..."
nohup mvn spring-boot:run > springboot.log 2>&1 &
SPRING_PID=$!

# Wait for Spring Boot to be ready
print_status "Waiting for Spring Boot application to be ready..."
for i in {1..20}; do
    sleep 3
    if curl -s http://localhost:8080/actuator/health > /dev/null 2>&1 || \
       curl -s http://localhost:8080/api/scan?url=https://www.google.com > /dev/null 2>&1; then
        print_success "Spring Boot application is up and running on port 8080"
        break
    fi
    if [ $i -eq 20 ]; then
        print_error "Spring Boot application failed to start within 60 seconds"
        print_status "Checking Spring Boot logs..."
        tail -n 20 springboot.log 2>/dev/null || echo "No log file found"
        exit 1
    fi
done

# Test the complete system
print_status "Testing the complete system..."
TEST_URL="https://www.google.com"
TEST_RESPONSE=$(curl -s -X POST "http://localhost:8080/api/scan?url=${TEST_URL}" 2>/dev/null)

if echo "$TEST_RESPONSE" | grep -q "status"; then
    print_success "System is working correctly!"
    echo "$TEST_RESPONSE" | jq '.' 2>/dev/null || echo "$TEST_RESPONSE"
else
    print_warning "System test failed, but services are running"
    print_status "Spring Boot response:"
    echo "$TEST_RESPONSE"
fi

# Print service information
echo ""
print_success "🎉 All services are running!"
echo ""
echo "📊 Service Status:"
echo "  • ML Microservice: http://localhost:5002 (PID: $ML_PID)"
echo "  • Spring Boot App: http://localhost:8080 (PID: $SPRING_PID)"
echo ""
echo "📝 Log Files:"
echo "  • ML Microservice: ml_microservice.log"
echo "  • Spring Boot: springboot.log"
echo ""
echo "🧪 Test Endpoints:"
echo "  • Health Check: curl http://localhost:5002/health"
echo "  • ML Predict: curl -X POST http://localhost:5002/predict -H 'Content-Type: application/json' -d '{\"url\":\"https://www.google.com\"}'"
echo "  • URL Scan: curl -X POST 'http://localhost:8080/api/scan?url=https://www.google.com'"
echo ""
echo "🛑 To stop all services: pkill -f 'python3.*ml_microservice.py' && pkill -f 'spring-boot:run'"
echo "" 