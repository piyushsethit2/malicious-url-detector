#!/bin/bash

echo "⏱️  Deploying Health Check Timeout Fixes"
echo "========================================="

echo "📦 Deploying Main Java Application..."
echo "   Path: /Users/bootnext-55/Downloads/malicious-url-detector 2"

# Check if we're in the right directory
if [ -f "pom.xml" ]; then
    echo "   ✅ Maven project found"
    
    # Add all changes
    git add .
    
    # Commit changes
    git commit -m "Increase health check timeouts: Java app 30s, Docker 30s, microservices 30s"
    
    # Push to remote
    echo "   📤 Pushing to remote repository..."
    git push origin main
    
    echo "   ✅ Main Java application health check deployment initiated"
else
    echo "   ❌ Maven project not found in current directory"
fi

echo ""
echo "🎯 Deployment Summary"
echo "===================="
echo "✅ Main Java Application: Health check timeout deployment initiated"
echo ""
echo "📋 What was increased:"
echo "   - Java health check timeout: 10s → 30s"
echo "   - Docker health check timeout: 10s → 30s"
echo "   - Docker start period: 60s → 120s"
echo "   - Microservice timeouts: 10s → 30s"
echo "   - Malware detection timeout: 10s → 30s"
echo ""
echo "📝 Next Steps:"
echo "1. Monitor deployment on Render Dashboard"
echo "2. Wait 2-3 minutes for deployment to complete"
echo "3. Test health checks with increased timeouts"
echo "4. Monitor microservices status with new timeouts"
echo ""
echo "🔍 Monitor at: https://render.com/dashboard"
echo "📊 Test health checks: curl http://localhost:8080/api/microservices/status" 