# 🚀 Quick Start Guide - Optimized Docker Images

## 🎯 **Choose Your Optimization Level**

### **Option 1: Debian Slim (Recommended)**
Best balance of size reduction and compatibility.

```bash
# Build and run with Debian Slim versions
docker-compose -f docker-compose.debian.yml up --build -d
```

**Expected Sizes:**
- Spring Boot: ~200-300MB
- Python ML: ~300-400MB  
- Simple ML: ~100-150MB

### **Option 2: Ultra-Lightweight (Smallest)**
Maximum size reduction using heuristic-based ML.

```bash
# Use the optimization script
./optimize-images-fixed.sh
# Choose option 3 (Ultra-lightweight)

# Or manually build ultra-lightweight
docker build -f python_microservice/Dockerfile.ultralight -t python-ml-ultralight ./python_microservice
```

**Expected Sizes:**
- Spring Boot: ~200-300MB
- Python ML: ~50-100MB (heuristic-based)
- Simple ML: ~50-100MB

### **Option 3: Alpine Linux (Smallest Base)**
Smallest base images but may have compatibility issues.

```bash
# Use the optimization script
./optimize-images-fixed.sh
# Choose option 1 (Alpine Linux)
```

## 🔧 **Quick Commands**

### **Build All Optimized Images**
```bash
# Debian Slim (recommended)
docker-compose -f docker-compose.debian.yml up --build -d

# Original (if you want to compare)
docker-compose up --build -d
```

### **Check Image Sizes**
```bash
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(malicious-url-detector|ml-microservice)"
```

### **Monitor Resource Usage**
```bash
docker stats
```

### **View Logs**
```bash
# All services
docker-compose -f docker-compose.debian.yml logs -f

# Specific service
docker-compose -f docker-compose.debian.yml logs -f python-ml-microservice
```

## 📊 **Size Comparison**

| Version | Spring Boot | Python ML | Simple ML | Total |
|---------|-------------|-----------|-----------|-------|
| **Original** | ~500-800MB | ~400-600MB | ~150-200MB | ~1-1.6GB |
| **Debian Slim** | ~200-300MB | ~300-400MB | ~100-150MB | ~600-850MB |
| **Ultra-light** | ~200-300MB | ~50-100MB | ~50-100MB | ~300-500MB |
| **Alpine** | ~200-300MB | ~150-250MB | ~50-100MB | ~400-650MB |

## 🎯 **Free Hosting Platform Compatibility**

### **Railway** (512MB RAM limit)
✅ **Recommended:** Debian Slim or Ultra-lightweight

### **Render** (512MB RAM limit)
✅ **Recommended:** Debian Slim or Ultra-lightweight

### **Fly.io** (256MB RAM limit)
✅ **Recommended:** Ultra-lightweight only

### **Heroku** (Free tier)
✅ **Recommended:** Ultra-lightweight only

## 🚀 **Deploy to Free Platforms**

### **Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### **Render**
1. Connect your GitHub repo to Render
2. Render will auto-detect `docker-compose.debian.yml`
3. Deploy automatically

### **Fly.io**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

## 🔍 **Troubleshooting**

### **If Alpine builds fail:**
```bash
# Use Debian Slim instead
docker-compose -f docker-compose.debian.yml up --build -d
```

### **If images are still too large:**
```bash
# Use ultra-lightweight version
./optimize-images-fixed.sh
# Choose option 3
```

### **If services don't start:**
```bash
# Check logs
docker-compose -f docker-compose.debian.yml logs

# Check resource limits
docker stats
```

## 🎉 **Success Indicators**

✅ **Spring Boot starts** - Port 8080 accessible  
✅ **Python ML responds** - `curl http://localhost:5002/health`  
✅ **Simple ML responds** - `curl http://localhost:5001/health`  
✅ **All services healthy** - No error logs  

## 📞 **Need Help?**

1. Check the logs: `docker-compose -f docker-compose.debian.yml logs`
2. Verify Docker is running: `docker info`
3. Check resource usage: `docker stats`
4. Try the ultra-lightweight version if others fail

---

**Happy deploying! 🚀** 