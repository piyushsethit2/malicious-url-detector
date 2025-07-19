# Proper Repository Separation Instructions

## ✅ Correct Approach: Microservices in Workspace

### Current Structure:
```
malicious-url-detector/
├── src/                    # Java Spring Boot application
├── microservices/          # Python microservices (in workspace)
│   ├── python-ml-microservice/
│   ├── python-app-microservice/
│   └── ml-microservice/
├── render.yaml            # Main app only
└── ... (other files)
```

## Step 1: Create GitHub Repositories

Create 3 new repositories on GitHub:
- `python-ml-microservice`
- `python-app-microservice`
- `ml-microservice`

## Step 2: Initialize Each Repository

### 2.1 Python ML Microservice
```bash
cd microservices/python-ml-microservice
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/python-ml-microservice.git
git push -u origin main
```

### 2.2 Python App Microservice
```bash
cd ../python-app-microservice
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/python-app-microservice.git
git push -u origin main
```

### 2.3 ML Microservice
```bash
cd ../ml-microservice
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ml-microservice.git
git push -u origin main
```

## Step 3: Deploy on Render

### 3.1 Deploy each repository:
1. Go to [Render Dashboard](https://render.com/dashboard)
2. Click "New +" → "Web Service"
3. Connect each GitHub repository
4. Render will auto-detect the `render.yaml` files and use Docker

### 3.2 Expected URLs:
- `https://python-ml-microservice.onrender.com` (Port 5002)
- `https://python-app-microservice.onrender.com` (Port 5000)
- `https://ml-microservice.onrender.com` (Port 5001)

## Step 4: Update Main App

### 4.1 Update URLs in main app:
Edit `src/main/resources/application-render.yml` with the new service URLs.

### 4.2 Clean up main repository:
```bash
rm -rf microservices/
```

## Environment Variables Configuration

All microservices are configured with environment variables in their `render.yaml` files, just like the main Spring Boot app. No manual configuration needed on Render!

### Python ML Microservice:
- PORT=5002
- HOST=0.0.0.0
- HF_MODEL_NAME=distilbert-base-uncased
- DEVICE=cpu
- DEBUG=false
- LOG_LEVEL=INFO

### Python App Microservice:
- PORT=5000
- HOST=0.0.0.0
- HF_MODEL_NAME=distilbert-base-uncased
- DEVICE=cpu
- TIMEOUT=30
- MAX_LENGTH=512
- DEBUG=false
- LOG_LEVEL=INFO

### ML Microservice:
- PORT=5001
- HOST=0.0.0.0
- DEBUG=false

## Why This Approach is Better:

### ✅ **No Nested Git Repositories**
- Each repository is completely independent
- No git conflicts or confusion
- Clean separation of concerns

### ✅ **Independent Development**
- Each microservice can be developed separately
- Different teams can work on different services
- Independent versioning and releases

### ✅ **Clean Deployment**
- Each service deploys independently
- No interference between services
- Easy to scale individual services

### ✅ **Better Organization**
- Clear separation of Java and Python code
- Each repository has its own purpose
- Easier to maintain and understand

## Final Result:
- 4 completely independent repositories
- Each with its own git history
- Each with its own deployment pipeline
- Clean and maintainable codebase 