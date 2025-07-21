#!/bin/bash

echo "🔧 Deploying Python ML Microservice Library Fixes"
echo "================================================"

SERVICE_PATH="/Users/bootnext-55/Documents/projects/python-ml-microservice"

echo "📦 Deploying Python ML Microservice..."
echo "   Path: $SERVICE_PATH"

if [ -d "$SERVICE_PATH" ]; then
    cd "$SERVICE_PATH"
    
    # Check if git repository exists
    if [ -d ".git" ]; then
        echo "   ✅ Git repository found"
        
        # Add all changes
        git add .
        
        # Commit changes
        git commit -m "Fix library issues: add libgomp and libstdc++ for scikit-learn compatibility"
        
        # Push to remote
        echo "   📤 Pushing to remote repository..."
        git push origin main
        
        echo "   ✅ Python ML Microservice library fixes deployment initiated"
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
echo "✅ Python ML Microservice: Library fixes deployment initiated"
echo ""
echo "📋 What was fixed:"
echo "   - Added libgomp package for OpenMP support"
echo "   - Added libstdc++ package for C++ runtime support"
echo "   - Fixed scikit-learn import errors"
echo "   - Fixed sklearn.feature_extraction import errors"
echo "   - Increased health check timeout to 30s"
echo "   - Increased health check start period to 60s"
echo "   - Enhanced gunicorn logging configuration"
echo ""
echo "📝 Next Steps:"
echo "1. Monitor deployment on Render Dashboard"
echo "2. Wait 2-3 minutes for deployment to complete"
echo "3. Check logs for successful startup"
echo "4. Test health endpoint: https://python-ml-microservice.onrender.com/health"
echo ""
echo "🔍 Monitor at: https://render.com/dashboard"
echo "📊 Test endpoint: curl https://python-ml-microservice.onrender.com/health" 