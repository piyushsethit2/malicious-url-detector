# Malicious URL Detector

A comprehensive system for detecting malicious and phishing URLs using multiple detection methods including traditional heuristics, third-party threat intelligence, and advanced ML models.

## 🏗️ Architecture

The system consists of two main components:

1. **Java Spring Boot Backend**: Main API server with multiple detection services
2. **Python Flask Microservice**: ML inference service using HuggingFace transformers

## 📁 Project Structure

```
malicious-url-detector/
├── src/                          # Java Spring Boot application
│   └── main/
│       ├── java/com/example/malwaredetector/
│       │   ├── controller/       # REST API controllers
│       │   ├── service/          # Business logic and detection services
│       │   ├── model/           # Data models
│       │   └── repository/      # Database access
│       └── resources/
│           └── application.yml   # Configuration
├── python_microservice/          # ML inference service
│   ├── app.py                   # Flask application
│   ├── config.py                # Configuration settings
│   ├── model_manager.py         # Model management
│   ├── run.py                   # Entry point
│   ├── requirements.txt         # Python dependencies
│   └── README.md               # Microservice documentation
├── tests/                       # Test suite
│   ├── test_ml_microservice.py # Unit tests for ML service
│   ├── test_integration.py     # Integration tests
│   └── README.md               # Testing documentation
├── docs/                        # Documentation
│   ├── DETAILED_SYSTEM_DOCUMENTATION.md
│   ├── huggingface_phishing_models.txt
│   ├── detection_thresholds.yml
│   └── test_cases_expanded.txt
├── pom.xml                      # Maven configuration
└── MAIN_README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Java 17+** and Maven
- **Python 3.7+** and pip
- **Internet connection** (for model downloads)

### 1. Install Dependencies

**Java Backend**:
```bash
mvn clean install
```

**Python Microservice**:
```bash
cd python_microservice
pip install -r requirements.txt
```

### 2. Start Services

**Start Python ML Microservice**:
```bash
cd python_microservice
python run.py
```

**Start Java Backend** (in a new terminal):
```bash
mvn spring-boot:run
```

### 3. Test the System

```bash
# Test ML microservice
curl http://localhost:5001/health

# Test Java backend
curl http://localhost:8080/api/scan/health

# Scan a URL
curl -X POST "http://localhost:8080/api/scan?url=https://www.google.com"
```

## 🔧 Configuration

### Environment Variables

**Python Microservice**:
```bash
export PORT=5001
export HF_MODEL_NAME=distilbert-base-uncased
export DEVICE=cpu
```

**Java Backend** (in `application.yml`):
```yaml
ml:
  microservice:
    url: http://localhost:5001
    timeout: 10
    enabled: true
```

### Available Models

The system supports various HuggingFace models for URL classification:

- `distilbert-base-uncased` (default)
- `ealvaradob/bert-finetuned-phishing`
- `imanoop7/bert-phishing-detector`
- `shawhin/bert-phishing-classifier_teacher`

See `docs/huggingface_phishing_models.txt` for the complete list.

## 🧪 Testing

### Unit Tests

**ML Microservice**:
```bash
cd tests
python -m unittest test_ml_microservice.py -v
```

### Integration Tests

**Full System**:
```bash
cd tests
python test_integration.py
```

### Manual Testing

```bash
# Test safe URL
curl -X POST "http://localhost:8080/api/scan?url=https://www.google.com"

# Test malicious URL
curl -X POST "http://localhost:8080/api/scan?url=http://malware-test.com"

# Get detailed results
curl -X POST "http://localhost:8080/api/scan?url=https://www.facebook.com" | jq '.'
```

## 📊 API Endpoints

### Java Backend (`http://localhost:8080`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scan` | POST | Scan URL for malicious content |
| `/api/scan/health` | GET | Health check |
| `/api/scan/ml/health` | GET | ML service health |
| `/api/whitelist` | GET/POST | Manage whitelist |

### Python Microservice (`http://localhost:5001`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/info` | GET | Model information |
| `/predict` | POST | URL prediction |
| `/reload` | POST | Reload model |

## 🔍 Detection Methods

The system uses multiple detection approaches:

1. **URL Pattern Analysis**: Regex-based suspicious pattern detection
2. **Domain Reputation**: Check domain age, TLD, etc.
3. **Content Analysis**: Analyze webpage content for malicious indicators
4. **Dynamic Content Analysis**: Visit URLs and analyze content
5. **ML-based Detection**: Transformer models for classification
6. **Third-party Services**: VirusTotal, PhishTank, Google Safe Browsing
7. **Statistical Analysis**: Java-based statistical heuristics

## 📈 Performance Tuning

### Detection Thresholds

Adjust thresholds in `docs/detection_thresholds.yml`:

```yaml
comprehensive:
  malicious_count: 1
  confidence: 0.5

transformer_ml:
  threshold: 0.7
```

### Model Selection

Change the ML model:

```bash
# Set environment variable
export HF_MODEL_NAME=ealvaradob/bert-finetuned-phishing

# Or reload via API
curl -X POST http://localhost:5001/reload \
  -H "Content-Type: application/json" \
  -d '{"model_name": "ealvaradob/bert-finetuned-phishing"}'
```

## 🛠️ Development

### Adding New Detection Methods

1. **Create Detection Service**:
   ```java
   @Service
   public class NewDetectionService implements BaseDetectionService {
       @Override
       public DetectionResult detect(String url) {
           // Implementation
       }
   }
   ```

2. **Add to Orchestrator**:
   ```java
   @Autowired
   private NewDetectionService newDetectionService;
   ```

### Adding New ML Models

1. **Update Python Service**:
   ```python
   # In model_manager.py
   def load_model(self, model_name: str):
       # Load new model
   ```

2. **Test Model**:
   ```bash
   curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"url": "test-url"}'
   ```

## 📚 Documentation

- **System Documentation**: `docs/DETAILED_SYSTEM_DOCUMENTATION.md`
- **ML Models**: `docs/huggingface_phishing_models.txt`
- **Thresholds**: `docs/detection_thresholds.yml`
- **Test Cases**: `docs/test_cases_expanded.txt`
- **Microservice Docs**: `python_microservice/README.md`
- **Test Docs**: `tests/README.md`

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**:
   ```bash
   # Check ports in use
   lsof -i :5001
   lsof -i :8080
   
   # Kill processes
   kill -9 <PID>
   ```

2. **Model Loading Issues**:
   ```bash
   # Check model availability
   curl http://localhost:5001/info
   
   # Reload model
   curl -X POST http://localhost:5001/reload
   ```

3. **Java Compilation Errors**:
   ```bash
   # Clean and rebuild
   mvn clean compile
   ```

4. **Python Import Errors**:
   ```bash
   # Install dependencies
   cd python_microservice
   pip install -r requirements.txt
   ```

### Logs

**Java Backend**: Check console output for Spring Boot logs
**Python Microservice**: Check console output for Flask logs

### Health Checks

```bash
# Check all services
curl http://localhost:5001/health
curl http://localhost:8080/api/scan/health
curl http://localhost:8080/api/scan/ml/health
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Add tests for new functionality**
4. **Run all tests**: `cd tests && python test_integration.py`
5. **Submit a pull request**

## 📄 License

This project is part of the Malicious URL Detector system.

## 🙏 Acknowledgments

- HuggingFace for transformer models
- Spring Boot for the Java framework
- Flask for the Python microservice
- All contributors and testers

---

**For detailed technical documentation, see `docs/DETAILED_SYSTEM_DOCUMENTATION.md`** 