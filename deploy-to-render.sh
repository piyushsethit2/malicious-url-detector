#!/bin/bash

# 🚀 Render Deployment Script for Malicious URL Detector
echo "🚀 Starting Render Deployment Process..."
echo "========================================"

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

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "pom.xml" ]; then
    print_error "pom.xml not found. Please run this script from the project root directory."
    exit 1
fi

print_status "Checking current Git status..."

# Check if git repository exists
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
    print_success "Git repository initialized"
else
    print_status "Git repository already exists"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    print_warning "You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Update for Render deployment"
    print_success "Changes committed"
fi

# Check if remote origin exists
if ! git remote get-url origin &> /dev/null; then
    print_status "No remote origin found. You'll need to add your GitHub repository."
    echo ""
    echo "📋 Next Steps:"
    echo "1. Create a new repository on GitHub: https://github.com/new"
    echo "2. Name it: malicious-url-detector"
    echo "3. Make it PUBLIC (required for Render free tier)"
    echo "4. Don't initialize with README"
    echo "5. Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/malicious-url-detector.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "6. Then continue with Render deployment"
    echo ""
    exit 0
fi

print_status "Checking remote repository..."
REMOTE_URL=$(git remote get-url origin)
print_success "Remote repository: $REMOTE_URL"

# Check if we can push to remote
if ! git ls-remote --exit-code origin &> /dev/null; then
    print_error "Cannot access remote repository. Please check your GitHub credentials."
    exit 1
fi

print_status "Pushing to GitHub..."
git push origin main
if [ $? -eq 0 ]; then
    print_success "Code pushed to GitHub successfully"
else
    print_error "Failed to push to GitHub"
    exit 1
fi

echo ""
echo "🎉 GitHub Setup Complete!"
echo "========================="
echo ""
echo "📋 Next Steps for Render Deployment:"
echo ""
echo "1. 🌐 Go to Render.com: https://render.com"
echo "2. 🔐 Sign up/Login with your GitHub account"
echo "3. ➕ Click 'New +' → 'Web Service'"
echo "4. 🔗 Connect your GitHub repository"
echo "5. 📁 Select: malicious-url-detector"
echo ""
echo "⚙️  Configuration Settings:"
echo "   • Name: malicious-url-detector"
echo "   • Environment: Docker"
echo "   • Region: Choose closest to you"
echo "   • Branch: main"
echo "   • Root Directory: (leave empty)"
echo "   • Dockerfile Path: src/main/resources/Dockerfile"
echo "   • Docker Context: ."
echo ""
echo "🔧 Environment Variables:"
echo "   • SPRING_PROFILES_ACTIVE = render"
echo "   • PORT = 8080"
echo "   • ML_API_ENABLED = true"
echo ""
echo "⚡ Advanced Settings:"
echo "   • Health Check Path: /actuator/health"
echo "   • Auto-Deploy: Enabled"
echo "   • Plan: Free"
echo ""
echo "🚀 Click 'Create Web Service' to deploy!"
echo ""
echo "⏱️  First deployment may take 10-15 minutes"
echo "🔍 Monitor progress in the Render dashboard"
echo ""
echo "🌐 Your service will be available at:"
echo "   https://malicious-url-detector.onrender.com"
echo ""

print_success "Deployment script completed successfully!" 