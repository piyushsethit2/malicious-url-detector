# Advanced ML Integration for Malicious URL Detection

This project now includes advanced Machine Learning capabilities using HuggingFace transformers for state-of-the-art phishing and malware URL detection.

## 🚀 Features

- **Python Flask Microservice**: Advanced transformer-based ML model
- **Java Integration**: Seamless integration with Spring Boot backend
- **Dynamic Content Analysis**: Analyzes both URL and webpage content
- **Configurable Models**: Easy to switch between different HuggingFace models
- **Health Monitoring**: Built-in health checks and model information endpoints

## 📋 Prerequisites

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Java Dependencies
The project already includes the necessary JSON parsing dependency.

## 🔧 Setup Instructions

### 1. Start the Python ML Microservice

```bash
# Option 1: Use default model (microsoft/URLNet)
python ml_microservice.py

# Option 2: Use a different HuggingFace model
HF_MODEL_NAME=microsoft/phishpedia-base python ml_microservice.py

# Option 3: Use a custom model
HF_MODEL_NAME=your-username/your-model python ml_microservice.py
```

The microservice will start on `http://localhost:5000`

### 2. Start the Java Backend

```bash
mvn spring-boot:run
```

The Java application will start on `http://localhost:8080`

### 3. Test the Integration

```bash
python test_ml_integration.py
```

## 🎯 Available HuggingFace Models

You can use any of these pre-trained models (or your own):

### Recommended Models for URL Classification:
- `microsoft/URLNet` (default) - Specialized for URL classification
- `microsoft/phishpedia-base` - Phishing detection
- `distilbert-base-uncased` - General purpose (fallback)
- `bert-base-uncased` - General purpose
- `roberta-base` - General purpose

### Custom Models:
- Any model from HuggingFace that supports text classification
- Your own fine-tuned models

## 🔧 Configuration

### Java Application Properties (`application.yml`)

```yaml
ml:
  microservice:
    url: http://localhost:5000
    timeout: 10
    enabled: true
```

### Environment Variables for Python Microservice

```bash
# Model configuration
HF_MODEL_NAME=microsoft/URLNet

# Service configuration
PORT=5000
HOST=0.0.0.0
```

## 📊 API Endpoints

### Java Backend Endpoints

#### Scan URL with ML Integration
```bash
POST /api/scan?url=https://example.com
```

#### ML Service Health Check
```bash
GET /api/scan/ml/health
```

#### ML Model Information
```bash
GET /api/scan/ml/info
```

### Python Microservice Endpoints

#### Predict Malicious URL
```bash
POST /predict
Content-Type: application/json

{
  "url": "https://example.com",
  "content": "<optional page content>"
}
```

#### Health Check
```bash
GET /health
```

#### Model Information
```bash
GET /info
```

## 🔍 How It Works

### 1. URL Processing
1. User submits URL to Java backend
2. Java backend calls Python microservice with URL and optional content
3. Python microservice preprocesses the input and runs ML prediction
4. Results are returned to Java backend

### 2. Content Analysis Integration
1. Java backend fetches webpage content using `DynamicContentAnalyzerService`
2. Both URL and content are sent to ML microservice
3. ML model analyzes the combined input for malicious patterns
4. Results are integrated with other detection methods

### 3. Decision Making
1. ML results are combined with traditional detection methods
2. Whitelist status is considered
3. Final decision is made based on multiple factors
4. Results are saved to database

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_ml_integration.py
```

### Test Individual Components

#### Test Python Microservice
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

#### Test Java Integration
```bash
curl -X POST "http://localhost:8080/api/scan?url=https://www.google.com"
```

#### Check ML Health
```bash
curl http://localhost:8080/api/scan/ml/health
```

## 📈 Performance Considerations

### Model Loading
- First request may be slower due to model loading
- Subsequent requests are fast
- Consider using GPU if available (`cuda`)

### Memory Usage
- Transformer models can be memory-intensive
- Consider using smaller models for production
- Monitor memory usage with large models

### Timeout Configuration
- Adjust timeouts based on model size and complexity
- Default timeout is 10 seconds
- Consider async processing for batch operations

## 🔧 Troubleshooting

### Common Issues

#### 1. Model Loading Errors
```bash
# Check if model exists
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

#### 2. Memory Issues
```bash
# Use smaller model
HF_MODEL_NAME=distilbert-base-uncased python ml_microservice.py
```

#### 3. Connection Issues
```bash
# Check if services are running
curl http://localhost:5000/health
curl http://localhost:8080/api/scan/health
```

#### 4. Timeout Issues
```bash
# Increase timeout in application.yml
ml:
  microservice:
    timeout: 30
```

## 🚀 Production Deployment

### Docker Support
```dockerfile
# Python microservice
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ml_microservice.py .
EXPOSE 5000
CMD ["python", "ml_microservice.py"]
```

### Kubernetes
- Deploy Python microservice as separate pod
- Use service discovery for communication
- Configure health checks and readiness probes

### Monitoring
- Monitor model performance and accuracy
- Track response times and error rates
- Set up alerts for service health

## 📚 Advanced Usage

### Custom Model Training
1. Prepare your dataset
2. Fine-tune a base model
3. Upload to HuggingFace
4. Use your model name in `HF_MODEL_NAME`

### Batch Processing
```python
# Process multiple URLs efficiently
urls = ["url1", "url2", "url3"]
results = []
for url in urls:
    result = ml_service.detect(url)
    results.append(result)
```

### Model Switching
```bash
# Switch models without restarting
# Update HF_MODEL_NAME and restart microservice
HF_MODEL_NAME=new-model python ml_microservice.py
```

## 🤝 Contributing

1. Test with different models
2. Improve preprocessing logic
3. Add new detection features
4. Optimize performance
5. Add more comprehensive tests

## 📄 License

This project is part of the malicious URL detection system. 