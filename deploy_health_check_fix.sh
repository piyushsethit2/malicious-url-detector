#!/bin/bash

# Deploy Health Check Fix for Python ML Microservice
# Fixes the missing analyze_url method issue

echo "🚀 Deploying Health Check Fix for Python ML Microservice..."

# Navigate to the Python ML microservice directory
cd /Users/bootnext-55/Documents/projects/python-ml-microservice

echo "📁 Current directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "ml_microservice.py" ]; then
    echo "❌ Error: ml_microservice.py not found in current directory"
    exit 1
fi

# Check git status
echo "📊 Git status:"
git status --porcelain

# Add all changes
echo "➕ Adding changes..."
git add .

# Commit with descriptive message
echo "💾 Committing changes..."
git commit -m "Fix health check: Use detect_malicious instead of analyze_url

- Fixed health check endpoint to use correct method name
- Changed ai_detector.analyze_url() to ai_detector.detect_malicious()
- Resolves 'AIMalwareDetector' object has no attribute 'analyze_url' error
- Health check should now pass successfully"

# Push to remote repository
echo "🚀 Pushing to remote repository..."
git push origin main

echo "✅ Health check fix deployed successfully!"
echo ""
echo "📋 Summary of changes:"
echo "   - Fixed health check method call in ml_microservice.py"
echo "   - Changed from analyze_url() to detect_malicious()"
echo "   - This resolves the AttributeError in health checks"
echo ""
echo "🔍 Monitor the deployment on Render:"
echo "   - Check logs for successful health checks"
echo "   - Verify service status is UP"
echo "   - Test /health endpoint returns 200 OK" 