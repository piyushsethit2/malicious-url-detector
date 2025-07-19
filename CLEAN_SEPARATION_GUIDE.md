# Clean Repository Separation Guide

## Current Structure
```
malicious-url-detector/
├── src/                    # Java Spring Boot application
├── repositories/           # Python microservices ready for separation
│   ├── python-ml-microservice/
│   │   ├── ml_microservice.py    # Original code
│   │   ├── requirements.txt      # Dependencies
│   │   ├── Dockerfile           # Docker configuration
│   │   ├── .dockerignore        # Docker ignore rules
│   │   ├── render.yaml          # Render config (Docker)
│   │   └── README.md            # Documentation
│   ├── python-app-microservice/
│   │   ├── app.py               # Original code
│   │   ├── config.py            # Original code
│   │   ├── model_manager.py     # Original code
│   │   ├── __init__.py          # Original code
│   │   ├── requirements.txt     # Dependencies
│   │   ├── Dockerfile           # Docker configuration
│   │   ├── .dockerignore        # Docker ignore rules
│   │   ├── render.yaml          # Render config (Docker)
│   │   └── README.md            # Documentation
│   └── ml-microservice/
│       ├── app.py               # Original code
│       ├── requirements.txt     # Dependencies
│       ├── Dockerfile           # Docker configuration
│       ├── .dockerignore        # Docker ignore rules
│       ├── render.yaml          # Render config (Docker)
│       └── README.md            # Documentation
├── render.yaml            # Main app only (cleaned)
└── CLEAN_SEPARATION_GUIDE.md  # This guide
```

## Step 1: Create GitHub Repositories

### 1.1 Create 3 new repositories on GitHub:
- `python-ml-microservice`
- `python-app-microservice` 
- `ml-microservice`

## Step 2: Separate Each Repository

### 2.1 Python ML Microservice
```bash
cd repositories/python-ml-microservice
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
rm -rf repositories/
rm -rf python_microservice/
rm -rf ml_microservice/
rm requirements.txt
```

## Docker Benefits

### ✅ Why Docker for Each Microservice:
- **Consistent Environment**: Same Python 3.9.18 across all deployments
- **Isolation**: Each service runs in its own container
- **Portability**: Easy to deploy anywhere (Render, AWS, GCP, etc.)
- **Dependencies**: All dependencies bundled in container
- **Version Control**: Exact Python and package versions

### ✅ Docker Features:
- **Multi-stage builds**: Optimized for production
- **Security**: Non-root user execution
- **Caching**: Faster builds with layer caching
- **Health checks**: Built-in container health monitoring

## Result: 4 Independent Repositories
1. `malicious-url-detector` - Java Spring Boot (Port 8080)
2. `python-ml-microservice` - Python ML (Port 5002) - Docker
3. `python-app-microservice` - Python App (Port 5000) - Docker
4. `ml-microservice` - Simple ML (Port 5001) - Docker 