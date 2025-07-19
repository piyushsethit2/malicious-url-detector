# Python ML Microservice

A Flask-based microservice for malicious URL detection using machine learning models.

## Features

- **ML Model**: Uses DistilBERT for URL classification
- **API Endpoints**: `/predict`, `/health`, `/info`
- **Port**: 5002
- **Model**: distilbert-base-uncased

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python3 ml_microservice.py
```

### Environment Variables

- `PORT`: Service port (default: 5002)
- `HF_MODEL_NAME`: HuggingFace model name (default: distilbert-base-uncased)
- `PYTHON_VERSION`: Python version (3.9.18)

## API Endpoints

### POST /predict
Predict if a URL is malicious.

**Request:**
```json
{
  "url": "http://example.com"
}
```

**Response:**
```json
{
  "label": "safe",
  "probability": 0.85,
  "confidence": 0.85,
  "model": "distilbert-base-uncased"
}
```

### GET /health
Health check endpoint.

### GET /info
Model information endpoint.

## Deployment

This service is configured for deployment on Render.com with the included `render.yaml` file.

## Dependencies

- Flask 2.3.3
- Transformers 4.35.0
- Torch 2.1.0
- NumPy 1.24.3
- Requests 2.31.0
- Scikit-learn 1.3.0 