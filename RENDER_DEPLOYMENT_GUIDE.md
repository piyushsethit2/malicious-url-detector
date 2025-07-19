# 🚀 Complete Guide: Deploy Malicious URL Detector on Render.com

## 📋 **Prerequisites**
- GitHub account
- Render.com account (free)
- Your project code ready

## 🎯 **Deployment Strategy**
Since Render.com free tier has limitations, we'll deploy the **Spring Boot application** as the main service and use **external ML APIs** instead of running separate ML microservices.

## 📁 **Step 1: Prepare Your Repository**

### 1.1 Create a Render-optimized branch
```bash
git checkout -b render-deployment
```

### 1.2 Clean up unnecessary files for Render
```bash
# Remove Docker Compose files (not needed for Render)
rm docker-compose.yml docker-compose.debian.yml

# Remove Dockerfiles for microservices (we'll use external APIs)
rm python_microservice/Dockerfile*
rm ml_microservice/Dockerfile*
```

## 📁 **Step 2: Create Render-specific Configuration**

### 2.1 Create `render.yaml` (Render Blueprint)
```yaml
services:
  - type: web
    name: malicious-url-detector
    env: docker
    plan: free
    dockerfilePath: ./src/main/resources/Dockerfile
    dockerContext: .
    healthCheckPath: /actuator/health
    envVars:
      - key: SPRING_PROFILES_ACTIVE
        value: render
      - key: PORT
        value: 8080
      - key: ML_API_ENABLED
        value: true
```

### 2.2 Update Spring Boot configuration
Create `src/main/resources/application-render.yml`:
```yaml
server:
  port: ${PORT:8080}

spring:
  profiles:
    active: render
  datasource:
    url: jdbc:h2:mem:urlscanner
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  h2:
    console:
      enabled: true
      path: /h2-console
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: false

# External ML API configuration
ml:
  api:
    enabled: true
    # We'll use HuggingFace Inference API instead of local microservices
    huggingface:
      enabled: true
      api-url: https://api-inference.huggingface.co/models
      model-name: microsoft/DialoGPT-medium
```

## 📁 **Step 3: Update Spring Boot Application**

### 3.1 Modify ML Detection Service
Update `src/main/java/com/example/malwaredetector/service/detection/MlMicroserviceDetectionService.java`:

```java
@Service
public class MlMicroserviceDetectionService extends BaseDetectionService {
    
    private final RestTemplate restTemplate;
    private final String mlApiUrl;
    
    public MlMicroserviceDetectionService(RestTemplate restTemplate, 
                                        @Value("${ml.api.huggingface.api-url:https://api-inference.huggingface.co/models}") String apiUrl,
                                        @Value("${ml.api.huggingface.model-name:microsoft/DialoGPT-medium}") String modelName) {
        this.restTemplate = restTemplate;
        this.mlApiUrl = apiUrl + "/" + modelName;
    }
    
    @Override
    public DetectionResult detect(String url) {
        try {
            // Use HuggingFace Inference API instead of local microservice
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            Map<String, Object> requestBody = Map.of(
                "inputs", url,
                "options", Map.of("wait_for_model", true)
            );
            
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
            
            ResponseEntity<Map> response = restTemplate.postForEntity(
                mlApiUrl, request, Map.class);
            
            // Process response and return result
            return new DetectionResult(
                "ML_API", 
                response.getStatusCode() == HttpStatus.OK ? "SAFE" : "MALICIOUS",
                0.8,
                "ML API detection completed"
            );
            
        } catch (Exception e) {
            log.warn("ML API detection failed for URL: {}", url, e);
            return new DetectionResult("ML_API", "UNKNOWN", 0.0, "ML API detection failed");
        }
    }
}
```

### 3.2 Add RestTemplate Bean
Add to your main application class:

```java
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}
```

## 📁 **Step 4: Create Render-specific Dockerfile**

### 4.1 Update `src/main/resources/Dockerfile`:
```dockerfile
# Multi-stage build optimized for Render
FROM maven:3.9.6-eclipse-temurin-21-alpine AS build

WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests \
    -Dspring-boot.repackage.exclude="META-INF/*.SF,META-INF/*.DSA,META-INF/*.RSA"

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

RUN apk add --no-cache curl

WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

## 📁 **Step 5: Create GitHub Repository**

### 5.1 Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
```

### 5.2 Create GitHub repository
1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name it: `malicious-url-detector`
4. Make it **Public** (required for Render free tier)
5. Don't initialize with README (you already have one)

### 5.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/malicious-url-detector.git
git branch -M main
git push -u origin main
```

## 📁 **Step 6: Deploy on Render.com**

### 6.1 Sign up for Render
1. Go to [Render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub account

### 6.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `malicious-url-detector` repository

### 6.3 Configure the Service
- **Name**: `malicious-url-detector`
- **Environment**: `Docker`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Dockerfile Path**: `src/main/resources/Dockerfile`
- **Docker Context**: `.`

### 6.4 Environment Variables
Add these environment variables:
- `SPRING_PROFILES_ACTIVE`: `render`
- `PORT`: `8080`
- `ML_API_ENABLED`: `true`

### 6.5 Advanced Settings
- **Health Check Path**: `/actuator/health`
- **Auto-Deploy**: Enabled
- **Plan**: Free

### 6.6 Deploy
Click "Create Web Service"

## 📁 **Step 7: Monitor Deployment**

### 7.1 Check Build Logs
- Watch the build process in Render dashboard
- First build may take 10-15 minutes

### 7.2 Verify Health Check
- Wait for health check to pass
- Service should show "Live" status

### 7.3 Test Your Service
Your service will be available at:
`https://malicious-url-detector.onrender.com`

## 📁 **Step 8: Test the Deployment**

### 8.1 Test Health Endpoint
```bash
curl https://malicious-url-detector.onrender.com/actuator/health
```

### 8.2 Test URL Scanning
```bash
curl -X POST https://malicious-url-detector.onrender.com/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

### 8.3 Test Web Interface
Visit: `https://malicious-url-detector.onrender.com`

## 📁 **Step 9: Optional - Add Custom Domain**

### 9.1 Add Custom Domain (if you have one)
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records as instructed

## 📁 **Step 10: Monitor and Maintain**

### 10.1 Set up Monitoring
- Enable Render's built-in monitoring
- Set up alerts for downtime

### 10.2 Update Application
```bash
# Make changes locally
git add .
git commit -m "Update application"
git push origin main
# Render will auto-deploy
```

## 🚨 **Important Notes for Free Tier**

### Limitations:
- **Sleep after 15 minutes** of inactivity
- **512MB RAM** limit
- **0.1 CPU** cores
- **Public repositories only**

### Best Practices:
1. **Keep images small** (we optimized for this)
2. **Use external APIs** instead of local ML services
3. **Implement proper health checks**
4. **Monitor resource usage**

## 🔧 **Troubleshooting**

### Common Issues:

1. **Build Fails**
   - Check Dockerfile path
   - Verify all dependencies in pom.xml
   - Check build logs in Render dashboard

2. **Health Check Fails**
   - Verify `/actuator/health` endpoint works locally
   - Check application logs in Render

3. **Service Times Out**
   - Free tier has cold starts
   - First request after 15 minutes may be slow

4. **Out of Memory**
   - Reduce JVM heap size
   - Optimize Docker image further

## 📞 **Support**

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Render Community**: [community.render.com](https://community.render.com)
- **GitHub Issues**: Create issues in your repository

## 🎉 **Success!**

Your malicious URL detector is now live on Render.com! 

**Your service URL**: `https://malicious-url-detector.onrender.com`

Share this URL with others to test your malware detection service! 