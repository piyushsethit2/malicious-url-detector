#!/bin/bash

echo "📝 Deploying Python App Microservice Logging Fixes"
echo "=================================================="

SERVICE_PATH="/Users/bootnext-55/Documents/projects/python-app-microservice"

echo "📦 Deploying Python App Microservice..."
echo "   Path: $SERVICE_PATH"

if [ -d "$SERVICE_PATH" ]; then
    cd "$SERVICE_PATH"
    
    # Check if git repository exists
    if [ -d ".git" ]; then
        echo "   ✅ Git repository found"
        
        # Add all changes
        git add .
        
        # Commit changes
        git commit -m "Enhanced logging: add detailed logs for Render visibility"
        
        # Push to remote
        echo "   📤 Pushing to remote repository..."
        git push origin main
        
        echo "   ✅ Python App Microservice logging deployment initiated"
    else
        echo "   ❌ Git repository not found in $SERVICE_PATH"
    fi
    
    cd - > /dev/null
else
    echo "   ❌ Directory not found: $SERVICE_PATH"
fi

echo ""
echo "🎯 Deployment Summary"
echo "===================="
echo "✅ Python App Microservice: Logging deployment initiated"
echo ""
echo "📋 What was fixed:"
echo "   - Enhanced logging configuration"
echo "   - Added Flask app logging"
echo "   - Added detailed endpoint logging"
echo "   - Added pattern matching logs"
echo "   - Added error handling logs"
echo "   - Updated render.yaml with logging env vars"
echo "   - Updated Dockerfile with gunicorn logging"
echo ""
echo "📝 Next Steps:"
echo "1. Monitor deployment on Render Dashboard"
echo "2. Wait 2-3 minutes for deployment to complete"
echo "3. Run: python3 test_python_app_logs.py"
echo "4. Check Render logs for detailed logging"
echo ""
echo "🔍 Monitor at: https://render.com/dashboard"
echo "📊 Test logs with: python3 test_python_app_logs.py" 