# Python Microservices Deployment Guide

## Current Status
- ✅ Main Java Application: Deployed at `malicious-url-detector-16nm.onrender.com`
- ❌ Python Microservices: Not deployed yet

## Option 1: Manual Deployment (Recommended)

### Step 1: Deploy Python ML Microservice
1. Go to [render.com/dashboard](https://render.com/dashboard)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `python-ml-microservice`
   - **Environment**: `Python`
   - **Build Command**: `cd python_microservice && pip install -r requirements.txt`
   - **Start Command**: `cd python_microservice && python ml_microservice.py`
   - **Environment Variables**:
     - `PORT`: `5002`
     - `HF_MODEL_NAME`: `distilbert-base-uncased`

### Step 2: Deploy Python App Microservice
1. Click "New +" → "Web Service"
2. Configure:
   - **Name**: `python-app-microservice`
   - **Environment**: `Python`
   - **Build Command**: `cd python_microservice && pip install -r requirements.txt`
   - **Start Command**: `cd python_microservice && python app.py`
   - **Environment Variables**:
     - `PORT`: `5000`
     - `HF_MODEL_NAME`: `distilbert-base-uncased`

### Step 3: Deploy ML Microservice
1. Click "New +" → "Web Service"
2. Configure:
   - **Name**: `ml-microservice`
   - **Environment**: `Python`
   - **Build Command**: `cd ml_microservice && pip install -r requirements.txt`
   - **Start Command**: `cd ml_microservice && python app.py`
   - **Environment Variables**:
     - `PORT`: `5001`
     - `HF_MODEL_NAME`: `distilbert-base-uncased`

## Option 2: Separate Repositories (Alternative)

If manual deployment doesn't work, you can:
1. Create separate GitHub repositories for each microservice
2. Copy the respective `render.yaml` files to each repository
3. Deploy each repository separately

## Expected URLs After Deployment
- `https://python-ml-microservice.onrender.com` (Port 5002)
- `https://python-app-microservice.onrender.com` (Port 5000)
- `https://ml-microservice.onrender.com` (Port 5001)

## Testing
Once deployed, test your main application again. The 404 errors should be resolved. 