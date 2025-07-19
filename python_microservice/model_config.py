#!/usr/bin/env python3
"""
Model Configuration for URL Malicious Detection
Provides different model options and configurations
"""

import os
from typing import Dict, Any

# Available models for URL classification
AVAILABLE_MODELS = {
    "distilbert-base-uncased": {
        "description": "Fast and efficient BERT model",
        "max_length": 512,
        "fallback": True
    },
    "microsoft/DialoGPT-medium": {
        "description": "Microsoft's conversational model",
        "max_length": 512,
        "fallback": False
    },
    "bert-base-uncased": {
        "description": "Standard BERT model",
        "max_length": 512,
        "fallback": False
    },
    "roberta-base": {
        "description": "Robustly optimized BERT",
        "max_length": 512,
        "fallback": False
    }
}

# URL-specific feature patterns for better classification
SUSPICIOUS_PATTERNS = {
    "phishing_keywords": [
        r"login|signin|bank|pay|secure|verify|update|account",
        r"admin|administrator|wp-admin|wp-content",
        r"password|username|email|credit.?card|social.?security|ssn"
    ],
    "suspicious_domains": [
        r"\.tk|\.ml|\.ga|\.cf|\.gq",  # Free domains
        r"bit\.ly|goo\.gl|tinyurl|is\.gd",  # URL shorteners
        r"\.xyz|\.top|\.club|\.site|\.online"  # Suspicious TLDs
    ],
    "malicious_indicators": [
        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",  # IP addresses
        r"[a-zA-Z0-9]{20,}",  # Long random strings
        r"www[0-9]+",  # Numbered subdomains
        r"secure[0-9]*",  # Fake secure domains
        r"login[0-9]*",  # Fake login domains
    ],
    "obfuscation_techniques": [
        r"base64",
        r"\\\\x[0-9a-fA-F]{2}",
        r"&#x[0-9a-fA-F]+",
        r"%[0-9a-fA-F]{2}",
        r"javascript:",
        r"data:text/html"
    ]
}

# Confidence thresholds for different scenarios
CONFIDENCE_THRESHOLDS = {
    "high_risk": 0.8,
    "medium_risk": 0.6,
    "low_risk": 0.4,
    "suspicious_patterns": 0.5,
    "whitelist_override": 0.9
}

# Whitelist domains that should be trusted
WHITELIST_DOMAINS = {
    "google.com", "google.co.uk", "google.ca", "google.com.au",
    "facebook.com", "facebook.net",
    "amazon.com", "amazon.co.uk", "amazon.ca", "amazon.com.au",
    "microsoft.com", "microsoft.net",
    "apple.com", "icloud.com",
    "github.com", "github.io",
    "stackoverflow.com",
    "wikipedia.org",
    "youtube.com",
    "twitter.com", "x.com",
    "linkedin.com",
    "reddit.com",
    "netflix.com",
    "spotify.com",
    "discord.com",
    "slack.com",
    "zoom.us",
    "dropbox.com",
    "box.com",
    "salesforce.com",
    "adobe.com",
    "autodesk.com",
    "oracle.com",
    "ibm.com",
    "intel.com",
    "nvidia.com",
    "amd.com",
    "cisco.com",
    "dell.com",
    "hp.com",
    "lenovo.com",
    "samsung.com",
    "lg.com",
    "sony.com",
    "panasonic.com",
    "canon.com",
    "nikon.com",
    "fujifilm.com",
    "kodak.com",
    "polaroid.com",
    "instant.com",
    "polaroid.com",
    "fujifilm.com",
    "kodak.com",
    "canon.com",
    "nikon.com",
    "sony.com",
    "panasonic.com",
    "lg.com",
    "samsung.com",
    "lenovo.com",
    "hp.com",
    "dell.com",
    "cisco.com",
    "amd.com",
    "nvidia.com",
    "intel.com",
    "ibm.com",
    "oracle.com",
    "autodesk.com",
    "adobe.com",
    "salesforce.com",
    "box.com",
    "dropbox.com",
    "zoom.us",
    "slack.com",
    "discord.com",
    "spotify.com",
    "netflix.com",
    "reddit.com",
    "linkedin.com",
    "x.com",
    "twitter.com",
    "youtube.com",
    "wikipedia.org",
    "stackoverflow.com",
    "github.io",
    "github.com",
    "icloud.com",
    "apple.com",
    "microsoft.net",
    "microsoft.com",
    "amazon.com.au",
    "amazon.ca",
    "amazon.co.uk",
    "amazon.com",
    "facebook.net",
    "facebook.com",
    "google.com.au",
    "google.ca",
    "google.co.uk",
    "google.com"
}

def get_model_config(model_name: str = None) -> Dict[str, Any]:
    """
    Get configuration for a specific model
    """
    if model_name is None:
        model_name = os.getenv("HF_MODEL_NAME", "distilbert-base-uncased")
    
    if model_name in AVAILABLE_MODELS:
        return AVAILABLE_MODELS[model_name]
    else:
        # Return default model config
        return AVAILABLE_MODELS["distilbert-base-uncased"]

def is_whitelisted_domain(url: str) -> bool:
    """
    Check if a domain is in the whitelist
    """
    import re
    
    # Extract domain from URL
    domain_match = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url.lower())
    if domain_match:
        domain = domain_match.group(1)
        return domain in WHITELIST_DOMAINS
    
    return False

def get_suspicious_score(url: str) -> Dict[str, Any]:
    """
    Calculate suspicious score based on patterns
    """
    import re
    
    score = 0
    detected_patterns = []
    
    for category, patterns in SUSPICIOUS_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url, re.IGNORECASE):
                score += 1
                detected_patterns.append(f"{category}: {pattern}")
    
    return {
        "score": score,
        "patterns": detected_patterns,
        "max_score": sum(len(patterns) for patterns in SUSPICIOUS_PATTERNS.values()),
        "ratio": score / sum(len(patterns) for patterns in SUSPICIOUS_PATTERNS.values()) if sum(len(patterns) for patterns in SUSPICIOUS_PATTERNS.values()) > 0 else 0
    } 