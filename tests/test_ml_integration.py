#!/usr/bin/env python3
"""
Test script for ML microservice integration
Tests the Python Flask microservice and Java backend integration
"""

import requests
import json
import time
import subprocess
import sys
from datetime import datetime

# Configuration
ML_SERVICE_URL = "http://localhost:5001"
JAVA_SERVICE_URL = "http://localhost:8080"

def test_ml_microservice():
    """Test the Python ML microservice directly"""
    print("🔍 Testing ML Microservice...")
    
    # Test URLs
    test_urls = [
        "https://www.google.com",  # Safe
        "https://www.facebook.com",  # Safe
        "http://malware-test.com",  # Malicious
        "http://phishing-scam.net",  # Malicious
        "https://www.amazon.com",  # Safe
        "http://virus-download.xyz"  # Malicious
    ]
    
    results = []
    
    for url in test_urls:
        try:
            payload = {"url": url}
            response = requests.post(f"{ML_SERVICE_URL}/predict", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "url": url,
                    "label": result.get("label", "unknown"),
                    "confidence": result.get("confidence", 0.0),
                    "model": result.get("model", "unknown"),
                    "status": "success"
                })
                print(f"✅ {url}: {result.get('label')} (confidence: {result.get('confidence', 0.0):.3f})")
            else:
                results.append({
                    "url": url,
                    "label": "error",
                    "confidence": 0.0,
                    "model": "unknown",
                    "status": f"HTTP {response.status_code}"
                })
                print(f"❌ {url}: HTTP {response.status_code}")
                
        except Exception as e:
            results.append({
                "url": url,
                "label": "error",
                "confidence": 0.0,
                "model": "unknown",
                "status": str(e)
            })
            print(f"❌ {url}: {e}")
    
    return results

def test_java_integration():
    """Test the Java backend with ML integration"""
    print("\n🔍 Testing Java Backend with ML Integration...")
    
    test_urls = [
        "https://www.google.com",
        "https://www.facebook.com", 
        "http://malware-test.com",
        "http://phishing-scam.net",
        "https://www.amazon.com",
        "http://virus-download.xyz"
    ]
    
    results = []
    
    for url in test_urls:
        try:
            response = requests.post(f"{JAVA_SERVICE_URL}/api/scan", params={"url": url}, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "url": url,
                    "malicious": result.get("malicious", False),
                    "confidence": result.get("confidenceScore", 0.0),
                    "status": result.get("overallStatus", "unknown"),
                    "sources": [det.get("method", "") for det in result.get("detectionResults", {}).values()],
                    "java_status": "success"
                })
                print(f"✅ {url}: {result.get('overallStatus')} (confidence: {result.get('confidenceScore', 0.0):.3f})")
            else:
                results.append({
                    "url": url,
                    "malicious": False,
                    "confidence": 0.0,
                    "status": "error",
                    "sources": [],
                    "java_status": f"HTTP {response.status_code}"
                })
                print(f"❌ {url}: HTTP {response.status_code}")
                
        except Exception as e:
            results.append({
                "url": url,
                "malicious": False,
                "confidence": 0.0,
                "status": "error",
                "sources": [],
                "java_status": str(e)
            })
            print(f"❌ {url}: {e}")
    
    return results

def test_ml_health():
    """Test ML service health endpoints"""
    print("\n🔍 Testing ML Service Health...")
    
    # Test Python microservice health
    try:
        response = requests.get(f"{ML_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Python ML Service: {health.get('status', 'unknown')}")
            print(f"   Model: {health.get('model', 'unknown')}")
            print(f"   Device: {health.get('device', 'unknown')}")
        else:
            print(f"❌ Python ML Service: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Python ML Service: {e}")
    
    # Test Java ML health endpoint
    try:
        response = requests.get(f"{JAVA_SERVICE_URL}/api/scan/ml/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Java ML Integration: {health.get('healthy', False)}")
        else:
            print(f"❌ Java ML Integration: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Java ML Integration: {e}")

def test_model_info():
    """Test model information endpoints"""
    print("\n🔍 Testing Model Information...")
    
    # Test Python microservice info
    try:
        response = requests.get(f"{ML_SERVICE_URL}/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Model Info:")
            print(f"   Model: {info.get('model_name', 'unknown')}")
            print(f"   Device: {info.get('device', 'unknown')}")
            print(f"   Max Length: {info.get('max_length', 'unknown')}")
        else:
            print(f"❌ Model Info: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Model Info: {e}")

def save_results(ml_results, java_results):
    """Save test results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ml_integration_test_{timestamp}.json"
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "ml_microservice_results": ml_results,
        "java_integration_results": java_results,
        "summary": {
            "ml_tests": len(ml_results),
            "java_tests": len(java_results),
            "ml_success": len([r for r in ml_results if r["status"] == "success"]),
            "java_success": len([r for r in java_results if r["java_status"] == "success"])
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to: {filename}")
    return results

def main():
    """Main test function"""
    print("🚀 Starting ML Integration Tests...")
    print("=" * 50)
    
    # Check if services are running
    print("🔍 Checking service availability...")
    
    try:
        ml_health = requests.get(f"{ML_SERVICE_URL}/health", timeout=5)
        print(f"✅ Python ML Service: Running on {ML_SERVICE_URL}")
    except:
        print(f"❌ Python ML Service: Not running on {ML_SERVICE_URL}")
        print("   Please start the ML microservice: python ml_microservice.py")
        return
    
    try:
        java_health = requests.get(f"{JAVA_SERVICE_URL}/api/scan/health", timeout=5)
        print(f"✅ Java Backend: Running on {JAVA_SERVICE_URL}")
    except:
        print(f"❌ Java Backend: Not running on {JAVA_SERVICE_URL}")
        print("   Please start the Java application: mvn spring-boot:run")
        return
    
    print("\n" + "=" * 50)
    
    # Run tests
    ml_results = test_ml_microservice()
    java_results = test_java_integration()
    test_ml_health()
    test_model_info()
    
    # Save results
    results = save_results(ml_results, java_results)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    ml_success = len([r for r in ml_results if r["status"] == "success"])
    java_success = len([r for r in java_results if r["java_status"] == "success"])
    
    print(f"ML Microservice Tests: {ml_success}/{len(ml_results)} successful")
    print(f"Java Integration Tests: {java_success}/{len(java_results)} successful")
    
    if ml_success == len(ml_results) and java_success == len(java_results):
        print("🎉 All tests passed! ML integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the results for details.")

if __name__ == "__main__":
    main() 