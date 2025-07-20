#!/bin/bash

# Malicious URL Detector - Local Development Script
# This script manages all microservices for local testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SPRING_APP_PORT=8080
PYTHON_APP_PORT=5000
PYTHON_ML_PORT=5002
PYTHON_APP_DIR="/Users/bootnext-55/Documents/projects/python-app-microservice"
PYTHON_ML_DIR="/Users/bootnext-55/Documents/projects/python-ml-microservice"
ML_MICROSERVICE_DIR="/Users/bootnext-55/Documents/projects/ml-microservice"

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

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    if check_port $port; then
        print_status "Killing process on port $port"
        lsof -ti:$port | xargs kill -9
        sleep 2
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            print_success "$service_name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start within $((max_attempts * 2)) seconds"
    return 1
}

# Function to start Python microservice
start_python_service() {
    local service_dir=$1
    local port=$2
    local service_name=$3
    local app_file=$4
    
    if [ ! -d "$service_dir" ]; then
        print_error "Directory $service_dir not found!"
        return 1
    fi
    
    print_status "Starting $service_name on port $port..."
    
    cd "$service_dir"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment for $service_name..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Start the service
    nohup python $app_file > "/tmp/${service_name}.log" 2>&1 &
    cd - > /dev/null
    
    # Wait for service to be ready
    wait_for_service "http://localhost:$port/health" "$service_name"
}

# Function to start Spring Boot application
start_spring_app() {
    print_status "Starting Spring Boot application on port $SPRING_APP_PORT..."
    
    # Build the application
    print_status "Building Spring Boot application..."
    mvn clean compile -q
    
    # Start the application
    nohup mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Dserver.port=$SPRING_APP_PORT" > spring-app.log 2>&1 &
    
    # Wait for service to be ready
    wait_for_service "http://localhost:$SPRING_APP_PORT/actuator/health" "Spring Boot Application"
}

# Function to stop all services
stop_all() {
    print_status "Stopping all services..."
    
    # Kill processes on specific ports
    kill_port $SPRING_APP_PORT
    kill_port $PYTHON_APP_PORT
    kill_port $PYTHON_ML_PORT
    
    # Kill any remaining Java processes (Spring Boot)
    pkill -f "spring-boot:run" || true
    pkill -f "java.*malicious-url-detector" || true
    
    # Kill any remaining Python processes
    pkill -f "python.*app.py" || true
    
    print_success "All services stopped"
}

# Function to start all services
start_all() {
    print_status "Starting all microservices..."
    
    # Stop any existing services first
    stop_all
    
    # Start Python microservices
    start_python_service "$PYTHON_APP_DIR" $PYTHON_APP_PORT "Python App Microservice" "app.py"
    start_python_service "$PYTHON_ML_DIR" $PYTHON_ML_PORT "Python ML Microservice" "ml_microservice.py"
    start_python_service "$ML_MICROSERVICE_DIR" 5001 "ML Microservice" "app.py"
    
    # Start Spring Boot application
    start_spring_app
    
    print_success "All services started successfully!"
    echo
    echo "Service URLs:"
    echo "  Spring Boot App: http://localhost:$SPRING_APP_PORT"
    echo "  Python App MS:   http://localhost:$PYTHON_APP_PORT"
    echo "  Python ML MS:    http://localhost:$PYTHON_ML_PORT"
    echo "  ML Microservice: http://localhost:5001"
    echo
    echo "Log files:"
    echo "  Spring App:      spring-app.log"
    echo "  Python App MS:   /tmp/Python App Microservice.log"
    echo "  Python ML MS:    /tmp/Python ML Microservice.log"
    echo "  ML Microservice: /tmp/ML Microservice.log"
}

# Function to test the system
test_system() {
    print_status "Testing the system..."
    
    # Test URLs
    local test_urls=(
        "https://google.com"
        "https://malware-test.com/virus.exe"
        "https://10.0.0.1/malware"
        "https://suspicious-domain-12345.com"
        "https://bit.ly/suspicious-link"
    )
    
    for url in "${test_urls[@]}"; do
        print_status "Testing URL: $url"
        response=$(curl -s -X POST "http://localhost:$SPRING_APP_PORT/api/scan?url=$url" -H "Content-Type: application/json")
        
        # Extract detection methods
        methods=$(echo "$response" | jq -r '.detectionResults | keys[]' 2>/dev/null || echo "Error parsing response")
        
        if [[ "$methods" == *"Enhanced Content Analysis"* ]]; then
            print_success "Enhanced Content Analysis found for $url"
        else
            print_warning "Enhanced Content Analysis NOT found for $url"
            echo "Available methods: $methods"
        fi
        
        echo "---"
    done
}

# Function to show status
show_status() {
    print_status "Service Status:"
    
    if check_port $SPRING_APP_PORT; then
        print_success "Spring Boot App: RUNNING (port $SPRING_APP_PORT)"
    else
        print_error "Spring Boot App: STOPPED"
    fi
    
    if check_port $PYTHON_APP_PORT; then
        print_success "Python App MS: RUNNING (port $PYTHON_APP_PORT)"
    else
        print_error "Python App MS: STOPPED"
    fi
    
    if check_port $PYTHON_ML_PORT; then
        print_success "Python ML MS: RUNNING (port $PYTHON_ML_PORT)"
    else
        print_error "Python ML MS: STOPPED"
    fi
    
    if check_port 5001; then
        print_success "ML Microservice: RUNNING (port 5001)"
    else
        print_error "ML Microservice: STOPPED"
    fi
}

# Function to show logs
show_logs() {
    local service=$1
    
    case $service in
        "spring")
            if [ -f "spring-app.log" ]; then
                tail -f spring-app.log
            else
                print_error "Spring app log not found"
            fi
            ;;
        "python-app")
            if [ -f "${PYTHON_APP_DIR}.log" ]; then
                tail -f ${PYTHON_APP_DIR}.log
            else
                print_error "Python app log not found"
            fi
            ;;
        "python-ml")
            if [ -f "${PYTHON_ML_DIR}.log" ]; then
                tail -f ${PYTHON_ML_DIR}.log
            else
                print_error "Python ML log not found"
            fi
            ;;
        *)
            print_error "Unknown service: $service"
            print_status "Available services: spring, python-app, python-ml"
            ;;
    esac
}

# Main script logic
case "${1:-help}" in
    "start")
        start_all
        ;;
    "stop")
        stop_all
        ;;
    "restart")
        stop_all
        sleep 2
        start_all
        ;;
    "status")
        show_status
        ;;
    "test")
        test_system
        ;;
    "logs")
        show_logs "$2"
        ;;
    "help"|*)
        echo "Malicious URL Detector - Local Development Script"
        echo
        echo "Usage: $0 {start|stop|restart|status|test|logs}"
        echo
        echo "Commands:"
        echo "  start     - Start all microservices"
        echo "  stop      - Stop all microservices"
        echo "  restart   - Restart all microservices"
        echo "  status    - Show status of all services"
        echo "  test      - Test the system with sample URLs"
        echo "  logs      - Show logs for a specific service"
        echo "  help      - Show this help message"
        echo
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 test"
        echo "  $0 logs spring"
        echo "  $0 logs python-app"
        echo "  $0 logs python-ml"
        ;;
esac 