# ML Microservice

A Flask-based microservice for malicious URL detection using HuggingFace transformer models.

## Features

- **Model Management**: Easy model loading and switching
- **RESTful API**: Simple HTTP endpoints for predictions
- **Health Monitoring**: Health check and model info endpoints
- **Configurable**: Environment-based configuration
- **Error Handling**: Robust error handling and fallbacks

## Project Structure

```
python_microservice/
├── __init__.py          # Package initialization
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── model_manager.py    # Model loading and prediction logic
├── run.py             # Simple run script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation

1. **Install Dependencies**:
   ```bash
   cd python_microservice
   pip install -r requirements.txt
   ```

2. **Environment Variables** (optional):
   ```bash
   export PORT=5001
   export HF_MODEL_NAME=distilbert-base-uncased
   export DEVICE=cpu
   export DEBUG=False
   ```

## Usage

### Starting the Service

**Option 1: Using the run script**
```bash
cd python_microservice
python run.py
```

**Option 2: Using the app directly**
```bash
cd python_microservice
python app.py
```

**Option 3: With custom configuration**
```bash
PORT=5001 HF_MODEL_NAME=distilbert-base-uncased python app.py
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:5001/health
```
Response:
```json
{
  "status": "healthy",
  "service": "ml-microservice",
  "model_loaded": true
}
```

#### Model Information
```bash
curl http://localhost:5001/info
```
Response:
```json
{
  "service": "ml-microservice",
  "model_info": {
    "model_name": "distilbert-base-uncased",
    "device": "cpu",
    "max_length": 512,
    "loaded": true
  },
  "config": {
    "host": "0.0.0.0",
    "port": 5001,
    "timeout": 30
  }
}
```

#### URL Prediction
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```
Response:
```json
{
  "url": "https://www.google.com",
  "prediction": "safe",
  "confidence": 0.506,
  "model": "distilbert-base-uncased"
}
```

#### Model Reload
```bash
curl -X POST http://localhost:5001/reload \
  -H "Content-Type: application/json" \
  -d '{"model_name": "new-model-name"}'
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5001` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `HF_MODEL_NAME` | `distilbert-base-uncased` | HuggingFace model name |
| `DEVICE` | `cpu` | Device for inference (`cpu` or `cuda`) |
| `DEBUG` | `False` | Enable debug mode |
| `TIMEOUT` | `30` | Request timeout |
| `MAX_LENGTH` | `512` | Maximum token length |
| `LOG_LEVEL` | `INFO` | Logging level |

### Available Models

The service supports any HuggingFace model compatible with `AutoModelForSequenceClassification`. Some recommended models for URL classification:

- `distilbert-base-uncased` (default)
- `ealvaradob/bert-finetuned-phishing`
- `imanoop7/bert-phishing-detector`
- `shawhin/bert-phishing-classifier_teacher`

## Development

### Running Tests

```bash
cd tests
python -m unittest test_ml_microservice.py
```

### Code Structure

- **`config.py`**: Centralized configuration management
- **`model_manager.py`**: Model loading, prediction, and management
- **`app.py`**: Flask application with API endpoints
- **`run.py`**: Simple entry point for running the service

### Adding New Features

1. **New Endpoints**: Add routes to `app.py`
2. **Model Enhancements**: Extend `ModelManager` class
3. **Configuration**: Add new options to `Config` class

## Troubleshooting

### Common Issues

1. **Model Loading Fails**:
   - Check internet connection
   - Verify model name exists on HuggingFace
   - Check available disk space

2. **Port Already in Use**:
   - Change port via `PORT` environment variable
   - Kill existing process: `lsof -ti:5001 | xargs kill`

3. **CUDA Out of Memory**:
   - Set `DEVICE=cpu` for CPU-only inference
   - Use smaller models

4. **Import Errors**:
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

### Logs

The service logs to stdout with the following format:
```
2024-01-01 12:00:00 - app - INFO - Starting ML microservice on 0.0.0.0:5001
2024-01-01 12:00:00 - model_manager - INFO - Model loaded successfully: distilbert-base-uncased
```

## Integration with Java Backend

This microservice is designed to work with the Java Spring Boot backend. The Java service calls this microservice for ML-based URL classification.

### Java Configuration

Update `application.yml` in the Java project:
```yaml
ml:
  microservice:
    url: http://localhost:5001
    timeout: 10
    enabled: true
```

## License

This project is part of the Malicious URL Detector system. 