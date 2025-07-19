# Repository Separation Guide

## Overview
This guide will help you separate your monolithic repository into 4 independent repositories for better deployment and maintenance.

## Repository Structure
1. **Main Repository**: `malicious-url-detector` (Java Spring Boot)
2. **Python ML Microservice**: `python-ml-microservice`
3. **Python App Microservice**: `python-app-microservice`
4. **ML Microservice**: `ml-microservice`

---

## Step 1: Create New GitHub Repositories

### 1.1 Create Python ML Microservice Repository
1. Go to [GitHub](https://github.com)
2. Click **"New repository"**
3. **Repository name**: `python-ml-microservice`
4. **Description**: `Python ML Microservice for malicious URL detection`
5. **Visibility**: Public
6. **Initialize**: Don't initialize with README (we'll add our own)
7. Click **"Create repository"**

### 1.2 Create Python App Microservice Repository
1. Click **"New repository"**
2. **Repository name**: `python-app-microservice`
3. **Description**: `Python App Microservice for malicious URL detection`
4. **Visibility**: Public
5. **Initialize**: Don't initialize with README
6. Click **"Create repository"**

### 1.3 Create ML Microservice Repository
1. Click **"New repository"**
2. **Repository name**: `ml-microservice`
3. **Description**: `Simple ML Microservice for malicious URL detection`
4. **Visibility**: Public
5. **Initialize**: Don't initialize with README
6. Click **"Create repository"**

---

## Step 2: Prepare Python ML Microservice Repository

### 2.1 Clone the new repository
```bash
git clone https://github.com/YOUR_USERNAME/python-ml-microservice.git
cd python-ml-microservice
```

### 2.2 Copy files from main repository
```bash
# Copy the Python ML microservice files
cp -r ../malicious-url-detector/python_microservice/ml_microservice.py .
cp -r ../malicious-url-detector/python_microservice/requirements.txt .
```

### 2.3 Copy configuration files
```bash
# Copy the configuration files we created
cp -r ../malicious-url-detector/python-ml-microservice/* .
```

### 2.4 Initialize and push
```bash
git add .
git commit -m "Initial commit: Python ML Microservice"
git push origin main
```

---

## Step 3: Prepare Python App Microservice Repository

### 3.1 Clone the new repository
```bash
git clone https://github.com/YOUR_USERNAME/python-app-microservice.git
cd python-app-microservice
```

### 3.2 Copy files from main repository
```bash
# Copy the Python app microservice files
cp -r ../malicious-url-detector/python_microservice/app.py .
cp -r ../malicious-url-detector/python_microservice/config.py .
cp -r ../malicious-url-detector/python_microservice/model_manager.py .
cp -r ../malicious-url-detector/python_microservice/__init__.py .
cp -r ../malicious-url-detector/python_microservice/requirements.txt .
```

### 3.3 Copy configuration files
```bash
# Copy the configuration files we created
cp -r ../malicious-url-detector/python-app-microservice/* .
```

### 3.4 Initialize and push
```bash
git add .
git commit -m "Initial commit: Python App Microservice"
git push origin main
```

---

## Step 4: Prepare ML Microservice Repository

### 4.1 Clone the new repository
```bash
git clone https://github.com/YOUR_USERNAME/ml-microservice.git
cd ml-microservice
```

### 4.2 Copy files from main repository
```bash
# Copy the ML microservice files
cp -r ../malicious-url-detector/ml_microservice/app.py .
cp -r ../malicious-url-detector/ml_microservice/requirements.txt .
```

### 4.3 Copy configuration files
```bash
# Copy the configuration files we created
cp -r ../malicious-url-detector/ml-microservice/* .
```

### 4.4 Initialize and push
```bash
git add .
git commit -m "Initial commit: ML Microservice"
git push origin main
```

---

## Step 5: Update Main Repository

### 5.1 Remove Python microservice directories
```bash
cd ../malicious-url-detector
rm -rf python_microservice
rm -rf ml_microservice
rm -rf python-ml-microservice
rm -rf python-app-microservice
rm -rf ml-microservice
```

### 5.2 Update main repository configuration
```bash
# Remove the Python microservices from render.yaml
# Keep only the main Java application
```

### 5.3 Commit changes
```bash
git add .
git commit -m "Remove Python microservices - now in separate repositories"
git push origin main
```

---

## Step 6: Deploy Each Repository on Render

### 6.1 Deploy Python ML Microservice
1. Go to [Render Dashboard](https://render.com/dashboard)
2. Click **"New +"** → **"Web Service"**
3. **Connect GitHub repository**: `python-ml-microservice`
4. **Name**: `python-ml-microservice`
5. **Environment**: `Python`
6. **Build Command**: `pip install -r requirements.txt`
7. **Start Command**: `python3 ml_microservice.py`
8. **Environment Variables**:
   - `PORT`: `5002`
   - `HF_MODEL_NAME`: `distilbert-base-uncased`
   - `PYTHON_VERSION`: `3.9.18`
9. Click **"Create Web Service"**

### 6.2 Deploy Python App Microservice
1. Click **"New +"** → **"Web Service"**
2. **Connect GitHub repository**: `python-app-microservice`
3. **Name**: `python-app-microservice`
4. **Environment**: `Python`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python3 app.py`
7. **Environment Variables**:
   - `PORT`: `5000`
   - `HF_MODEL_NAME`: `distilbert-base-uncased`
   - `PYTHON_VERSION`: `3.9.18`
8. Click **"Create Web Service"**

### 6.3 Deploy ML Microservice
1. Click **"New +"** → **"Web Service"**
2. **Connect GitHub repository**: `ml-microservice`
3. **Name**: `ml-microservice`
4. **Environment**: `Python`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python3 app.py`
7. **Environment Variables**:
   - `PORT`: `5001`
   - `HF_MODEL_NAME`: `distilbert-base-uncased`
   - `PYTHON_VERSION`: `3.9.18`
8. Click **"Create Web Service"**

---

## Step 7: Update Main Application URLs

### 7.1 Get the deployed URLs
After deployment, note the URLs:
- `https://python-ml-microservice.onrender.com`
- `https://python-app-microservice.onrender.com`
- `https://ml-microservice.onrender.com`

### 7.2 Update main application configuration
Update `src/main/resources/application-render.yml` with the new URLs.

### 7.3 Deploy main application
The main Java application should automatically redeploy with the new URLs.

---

## Step 8: Testing

### 8.1 Test each microservice individually
```bash
# Test Python ML Microservice
curl -X POST https://python-ml-microservice.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "http://example.com"}'

# Test Python App Microservice
curl -X POST https://python-app-microservice.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "http://example.com"}'

# Test ML Microservice
curl -X POST https://ml-microservice.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "http://example.com"}'
```

### 8.2 Test main application
Visit your main application and test URL scanning.

---

## Benefits of Repository Separation

1. **✅ Independent Deployment**: Each service can be deployed separately
2. **✅ Better Resource Management**: Each service gets its own resources
3. **✅ Easier Maintenance**: Changes to one service don't affect others
4. **✅ Scalability**: Each service can scale independently
5. **✅ Clear Ownership**: Each repository has a single responsibility
6. **✅ Better CI/CD**: Each service can have its own deployment pipeline

---

## Troubleshooting

### Common Issues:
1. **Import Errors**: Make sure all required files are copied
2. **Port Conflicts**: Each service should use different ports
3. **Environment Variables**: Ensure all required variables are set
4. **Dependencies**: Check that requirements.txt includes all needed packages

### Support:
- Check Render logs for each service
- Verify GitHub repository connections
- Ensure all environment variables are set correctly 