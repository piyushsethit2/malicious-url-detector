#!/usr/bin/env python3
"""
Ultra-lightweight ML Microservice for URL Malware Detection
Uses simple heuristics instead of heavy transformers for maximum size reduction
"""

import os
import re
import logging
from flask import Flask, request, jsonify
from urllib.parse import urlparse
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LightweightURLDetector:
    """Lightweight URL malware detector using heuristics"""
    
    def __init__(self):
        self.suspicious_patterns = [
            r'bit\.ly|goo\.gl|tinyurl\.com',  # URL shorteners
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
            r'[a-zA-Z0-9]{20,}',  # Very long random strings
            r'[^a-zA-Z0-9.-]',  # Special characters
            r'(login|signin|account|secure|verify)',  # Suspicious keywords
            r'\.(tk|ml|ga|cf|gq)',  # Suspicious TLDs
        ]
        
        self.safe_patterns = [
            r'google\.com|facebook\.com|amazon\.com|microsoft\.com',
            r'\.(com|org|net|edu|gov)$',
            r'https://',
        ]
    
    def extract_features(self, url):
        """Extract lightweight features from URL"""
        features = {
            'length': len(url),
            'has_https': url.startswith('https://'),
            'has_http': url.startswith('http://'),
            'domain_length': len(urlparse(url).netloc) if urlparse(url).netloc else 0,
            'path_length': len(urlparse(url).path),
            'query_length': len(urlparse(url).query),
            'suspicious_patterns': 0,
            'safe_patterns': 0,
        }
        
        # Count suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                features['suspicious_patterns'] += 1
        
        # Count safe patterns
        for pattern in self.safe_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                features['safe_patterns'] += 1
        
        return features
    
    def predict(self, url):
        """Make prediction using lightweight heuristics"""
        features = self.extract_features(url)
        
        # Simple scoring system
        score = 0.5  # Base score
        
        # Adjust based on features
        if features['has_https']:
            score += 0.1
        if features['safe_patterns'] > 0:
            score += 0.1 * features['safe_patterns']
        if features['suspicious_patterns'] > 0:
            score -= 0.15 * features['suspicious_patterns']
        if features['length'] > 100:
            score -= 0.1
        if features['domain_length'] > 50:
            score -= 0.1
        
        # Clamp between 0 and 1
        score = max(0.0, min(1.0, score))
        
        return {
            'is_malicious': score > 0.5,
            'confidence': score,
            'features': features
        }

# Initialize detector
detector = LightweightURLDetector()

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if URL is malicious"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        logger.info(f"Prediction request for: {url}")
        
        # Make prediction
        result = detector.predict(url)
        
        response = {
            'url': url,
            'is_malicious': result['is_malicious'],
            'confidence': result['confidence'],
            'model': 'lightweight-heuristic',
            'features': result['features']
        }
        
        logger.info(f"Prediction for {url}: {'malicious' if result['is_malicious'] else 'safe'} (confidence: {result['confidence']:.3f})")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing prediction: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'lightweight-ml-microservice',
        'model': 'heuristic-based'
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Lightweight ML Microservice',
        'version': '1.0.0',
        'endpoints': {
            'predict': 'POST /predict',
            'health': 'GET /health'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    logger.info(f"Starting lightweight ML microservice on 0.0.0.0:{port}")
    logger.info("Model: heuristic-based")
    app.run(host='0.0.0.0', port=port, debug=False) 