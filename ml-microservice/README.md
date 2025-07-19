# ML Microservice

A simple Flask-based microservice for malicious URL detection using basic ML features.

## Features

- **Simple ML Model**: Uses feature extraction and basic classification
- **API Endpoints**: `/predict`, `/health`
- **Port**: 5001
- **Model**: Dummy model with feature extraction

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python3 app.py
```

### Environment Variables

- `PORT`: Service port (default: 5001)
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
  "malicious": false,
  "confidence": 0.85,
  "details": "ML model confidence: 0.85"
}
```

### GET /health
Health check endpoint.

## Features Extracted

- URL length
- Digit count
- Special character count
- Suspicious word count
- Entropy
- Subdomain count

## Deployment

This service is configured for deployment on Render.com with the included `render.yaml` file.

## Dependencies

- Flask 2.3.3
- Transformers 4.35.0
- Torch 2.1.0
- NumPy 1.24.3
- Requests 2.31.0
- Scikit-learn 1.3.0 