# Workspace Setup Guide - All Microservices

## 📁 **Current Workspace Structure:**

```
/Users/bootnext-55/Documents/projects/
├── malicious-url-detector 2/     # Main Java Spring Boot app
├── ml-microservice/              # Python microservice 1 (Port 5001)
├── python-app-microservice/      # Python microservice 2 (Port 5000)
└── python-ml-microservice/       # Python microservice 3 (Port 5002)
```

## ✅ **Environment Variables Configuration**

All microservices are now configured with complete environment variables in their `render.yaml` files, just like the main Spring Boot app. **No manual configuration needed on Render!**

### **1. Main Java App (`malicious-url-detector 2`)**
```yaml
# render.yaml
envVars:
  - key: SPRING_PROFILES_ACTIVE
    value: render
  - key: PORT
    value: 8080
  - key: ML_API_ENABLED
    value: true
```

### **2. ML Microservice (`ml-microservice`)**
```yaml
# render.yaml
envVars:
  - key: PORT
    value: 5001
  - key: HOST
    value: 0.0.0.0
  - key: DEBUG
    value: false
```

### **3. Python App Microservice (`python-app-microservice`)**
```yaml
# render.yaml
envVars:
  - key: PORT
    value: 5000
  - key: HOST
    value: 0.0.0.0
  - key: HF_MODEL_NAME
    value: distilbert-base-uncased
  - key: DEVICE
    value: cpu
  - key: TIMEOUT
    value: 30
  - key: MAX_LENGTH
    value: 512
  - key: DEBUG
    value: false
  - key: LOG_LEVEL
    value: INFO
```

### **4. Python ML Microservice (`python-ml-microservice`)**
```yaml
# render.yaml
envVars:
  - key: PORT
    value: 5002
  - key: HOST
    value: 0.0.0.0
  - key: HF_MODEL_NAME
    value: distilbert-base-uncased
  - key: DEVICE
    value: cpu
  - key: DEBUG
    value: false
  - key: LOG_LEVEL
    value: INFO
```

## 🚀 **Deployment Steps**

### **Step 1: Deploy Python Microservices**

1. **ML Microservice:**
   ```bash
   cd /Users/bootnext-55/Documents/projects/ml-microservice
   git add .
   git commit -m "Add complete environment variables"
   git push origin main
   ```

2. **Python App Microservice:**
   ```bash
   cd /Users/bootnext-55/Documents/projects/python-app-microservice
   git add .
   git commit -m "Add complete environment variables"
   git push origin main
   ```

3. **Python ML Microservice:**
   ```bash
   cd /Users/bootnext-55/Documents/projects/python-ml-microservice
   git add .
   git commit -m "Add complete environment variables"
   git push origin main
   ```

### **Step 2: Deploy on Render**

1. Go to [Render Dashboard](https://render.com/dashboard)
2. Click "New +" → "Web Service"
3. Connect each GitHub repository
4. Render will auto-detect the `render.yaml` files and use Docker
5. **No manual environment variable configuration needed!**

### **Step 3: Get Service URLs**

After deployment, you'll get URLs like:
- `https://ml-microservice.onrender.com` (Port 5001)
- `https://python-app-microservice.onrender.com` (Port 5000)
- `https://python-ml-microservice.onrender.com` (Port 5002)

### **Step 4: Update Main Java App**

Update `src/main/resources/application-render.yml` with the actual URLs:

```yaml
ml:
  microservice:
    url: ${ML_MICROSERVICE_URL:https://python-ml-microservice.onrender.com}
  python-microservice:
    url: ${PYTHON_MICROSERVICE_URL:https://python-app-microservice.onrender.com}
  ml-microservice:
    url: ${ML_MICROSERVICE_3_URL:https://ml-microservice.onrender.com}
```

### **Step 5: Deploy Main Java App**

```bash
cd /Users/bootnext-55/Documents/projects/malicious-url-detector 2
git add .
git commit -m "Update microservice URLs"
git push origin main
```

## 🎯 **Benefits of This Setup**

### ✅ **Zero Manual Configuration**
- All environment variables are in `render.yaml` files
- No need to configure anything on Render dashboard
- Consistent configuration across all services

### ✅ **Easy Deployment**
- Just push to GitHub and Render auto-deploys
- Docker containers with all dependencies
- Health checks and monitoring included

### ✅ **Independent Services**
- Each microservice can be updated independently
- No interference between services
- Easy to scale individual services

### ✅ **Production Ready**
- Proper error handling
- Logging configuration
- Health check endpoints
- Docker optimization

## 🔧 **Local Testing**

You can test each service locally:

```bash
# ML Microservice
cd /Users/bootnext-55/Documents/projects/ml-microservice
python3 app.py

# Python App Microservice
cd /Users/bootnext-55/Documents/projects/python-app-microservice
python3 app.py

# Python ML Microservice
cd /Users/bootnext-55/Documents/projects/python-ml-microservice
python3 ml_microservice.py
```

## 📊 **Expected URLs After Deployment**

- **Main App**: `https://malicious-url-detector-2.onrender.com` (Port 8080)
- **ML Microservice**: `https://ml-microservice.onrender.com` (Port 5001)
- **Python App**: `https://python-app-microservice.onrender.com` (Port 5000)
- **Python ML**: `https://python-ml-microservice.onrender.com` (Port 5002)

All services are now ready for deployment with complete environment variable configuration! 🚀 