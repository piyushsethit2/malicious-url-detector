#!/usr/bin/env python3
"""
Run script for ML Microservice
Simple entry point to start the Flask application
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run() 