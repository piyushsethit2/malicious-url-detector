#!/usr/bin/env python3
"""
Test script to trigger logs on Python App Microservice
"""

import requests
import json
import time
from datetime import datetime

# Python App Microservice URL
PYTHON_APP_URL = "https://python-app-microservice.onrender.com"

def test_python_app_logs():
    """Test the Python App Microservice and trigger logs"""
    print("🔍 Testing Python App Microservice Logs")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"URL: {PYTHON_APP_URL}")
    
    # Test 1: Health check (should trigger logs)
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{PYTHON_APP_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Root endpoint (should trigger logs)
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{PYTHON_APP_URL}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Root endpoint successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Root endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
    
    # Test 3: Detection endpoint with safe URL (should trigger logs)
    print("\n3️⃣ Testing Detection with Safe URL...")
    try:
        safe_url = "https://www.google.com"
        data = {"url": safe_url}
        response = requests.post(f"{PYTHON_APP_URL}/detect", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Detection successful")
            print(f"   URL: {safe_url}")
            print(f"   Malicious: {result.get('is_malicious')}")
            print(f"   Confidence: {result.get('confidence')}")
            print(f"   Issues: {len(result.get('issues', []))}")
        else:
            print(f"   ❌ Detection failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Detection error: {e}")
    
    # Test 4: Detection endpoint with suspicious URL (should trigger more logs)
    print("\n4️⃣ Testing Detection with Suspicious URL...")
    try:
        suspicious_url = "http://malware-test.com/download.exe"
        data = {"url": suspicious_url}
        response = requests.post(f"{PYTHON_APP_URL}/detect", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Detection successful")
            print(f"   URL: {suspicious_url}")
            print(f"   Malicious: {result.get('is_malicious')}")
            print(f"   Confidence: {result.get('confidence')}")
            print(f"   Issues: {result.get('issues', [])}")
        else:
            print(f"   ❌ Detection failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Detection error: {e}")
    
    # Test 5: Detection endpoint with empty URL (should trigger error logs)
    print("\n5️⃣ Testing Detection with Empty URL...")
    try:
        data = {"url": ""}
        response = requests.post(f"{PYTHON_APP_URL}/detect", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Error handling successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error test failed: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Summary")
    print("=" * 50)
    print("✅ All tests completed")
    print("📝 Check Render logs for the following:")
    print("   - Startup logs")
    print("   - Health check logs")
    print("   - Root endpoint logs")
    print("   - Detection processing logs")
    print("   - Pattern matching logs")
    print("   - Error handling logs")
    print("\n🔍 To view logs on Render:")
    print("   1. Go to https://render.com/dashboard")
    print("   2. Click on 'python-app-microservice'")
    print("   3. Click on 'Logs' tab")
    print("   4. Look for the log entries from these tests")

if __name__ == "__main__":
    test_python_app_logs() 