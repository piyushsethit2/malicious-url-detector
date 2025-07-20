#!/bin/bash

echo "🚀 Deploying Microservice Fixes"
echo "================================"

# Function to deploy a microservice
deploy_microservice() {
    local service_name=$1
    local service_path=$2
    
    echo "📦 Deploying $service_name..."
    echo "   Path: $service_path"
    
    if [ -d "$service_path" ]; then
        cd "$service_path"
        
        # Check if git repository exists
        if [ -d ".git" ]; then
            echo "   ✅ Git repository found"
            
            # Add all changes
            git add .
            
            # Commit changes
            git commit -m "Optimize for production: reduce timeouts, improve performance"
            
            # Push to remote
            echo "   📤 Pushing to remote repository..."
            git push origin main
            
            echo "   ✅ $service_name deployment initiated"
        else
            echo "   ❌ Git repository not found in $service_path"
        fi
        
        cd - > /dev/null
    else
        echo "   ❌ Directory not found: $service_path"
    fi
    
    echo ""
}

# Deploy Python ML Microservice
deploy_microservice "Python ML Microservice" "/Users/bootnext-55/Documents/projects/python-ml-microservice"

# Deploy Python App Microservice  
deploy_microservice "Python App Microservice" "/Users/bootnext-55/Documents/projects/python-app-microservice"

echo "🎯 Deployment Summary"
echo "===================="
echo "✅ Python ML Microservice: Deployment initiated"
echo "✅ Python App Microservice: Deployment initiated"
echo ""
echo "📋 Next Steps:"
echo "1. Monitor deployment on Render Dashboard"
echo "2. Wait 2-3 minutes for deployment to complete"
echo "3. Run: python3 test_microservices_status.py"
echo "4. Check main application logs for microservice status"
echo ""
echo "🔍 Monitor at: https://render.com/dashboard" 