# ⚡ Quick Deploy to Render.com

## 🚀 **Step-by-Step Deployment (5 minutes)**

### **Step 1: Prepare Your Code**
```bash
# Run the deployment script
./deploy-to-render.sh
```

### **Step 2: Create GitHub Repository**
1. Go to [GitHub.com](https://github.com/new)
2. Repository name: `malicious-url-detector`
3. Make it **PUBLIC** (required for Render free tier)
4. Don't initialize with README
5. Click "Create repository"

### **Step 3: Push to GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/malicious-url-detector.git
git branch -M main
git push -u origin main
```

### **Step 4: Deploy on Render**
1. Go to [Render.com](https://render.com)
2. Sign up with GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Select `malicious-url-detector`

### **Step 5: Configure Service**
- **Name**: `malicious-url-detector`
- **Environment**: `Docker`
- **Dockerfile Path**: `src/main/resources/Dockerfile`
- **Docker Context**: `.`

### **Step 6: Add Environment Variables**
- `SPRING_PROFILES_ACTIVE` = `render`
- `PORT` = `8080`
- `ML_API_ENABLED` = `true`

### **Step 7: Advanced Settings**
- **Health Check Path**: `/actuator/health`
- **Plan**: Free

### **Step 8: Deploy**
Click "Create Web Service"

## 🎯 **Your Service URL**
`https://malicious-url-detector.onrender.com`

## ⏱️ **Deployment Time**
- First build: 10-15 minutes
- Subsequent updates: 2-5 minutes

## 🧪 **Test Your Service**
```bash
# Health check
curl https://malicious-url-detector.onrender.com/actuator/health

# Test URL scanning
curl -X POST https://malicious-url-detector.onrender.com/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

## 🚨 **Important Notes**
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep may be slow (cold start)
- Service automatically redeploys when you push to GitHub

## 🔧 **Troubleshooting**
- Check build logs in Render dashboard
- Verify all environment variables are set
- Ensure GitHub repository is public

## 📞 **Need Help?**
- Render Docs: [docs.render.com](https://docs.render.com)
- Render Community: [community.render.com](https://community.render.com) 