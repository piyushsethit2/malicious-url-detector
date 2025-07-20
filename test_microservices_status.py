#!/usr/bin/env python3
"""
Test script to check the status of all microservices
"""

import requests
import json
import time
from datetime import datetime

# Microservice URLs
MICROSERVICES = {
    "Python ML Microservice": "https://python-ml-microservice.onrender.com",
    "Python App Microservice": "https://python-app-microservice.onrender.com", 
    "ML Microservice 3": "https://ml-microservice-nn4p.onrender.com"
}

def test_microservice(name, base_url):
    """Test a single microservice"""
    print(f"\n🔍 Testing {name}...")
    print(f"   URL: {base_url}")
    
    results = {}
    
    # Test health endpoint
    try:
        health_url = f"{base_url}/health"
        print(f"   Health check: {health_url}")
        
        response = requests.get(health_url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
                results["health"] = {
                    "status": "UP",
                    "status_code": response.status_code,
                    "response": data
                }
            except json.JSONDecodeError:
                print(f"   Response (text): {response.text[:200]}...")
                results["health"] = {
                    "status": "UP",
                    "status_code": response.status_code,
                    "response": response.text[:200]
                }
        else:
            print(f"   Error Response: {response.text[:200]}...")
            results["health"] = {
                "status": "DOWN",
                "status_code": response.status_code,
                "error": response.text[:200]
            }
            
    except requests.exceptions.RequestException as e:
        print(f"   Error: {str(e)}")
        results["health"] = {
            "status": "DOWN",
            "error": str(e)
        }
    
    # Test root endpoint
    try:
        print(f"   Root endpoint: {base_url}/")
        response = requests.get(base_url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
                results["root"] = {
                    "status": "UP",
                    "status_code": response.status_code,
                    "response": data
                }
            except json.JSONDecodeError:
                print(f"   Response (text): {response.text[:200]}...")
                results["root"] = {
                    "status": "UP",
                    "status_code": response.status_code,
                    "response": response.text[:200]
                }
        else:
            print(f"   Error Response: {response.text[:200]}...")
            results["root"] = {
                "status": "DOWN",
                "status_code": response.status_code,
                "error": response.text[:200]
            }
            
    except requests.exceptions.RequestException as e:
        print(f"   Error: {str(e)}")
        results["root"] = {
            "status": "DOWN",
            "error": str(e)
        }
    
    return results

def main():
    print("🚀 Microservices Status Check")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    all_results = {}
    
    for name, url in MICROSERVICES.items():
        results = test_microservice(name, url)
        all_results[name] = results
        
        # Determine overall status
        health_status = results.get("health", {}).get("status", "UNKNOWN")
        root_status = results.get("root", {}).get("status", "UNKNOWN")
        
        if health_status == "UP" or root_status == "UP":
            print(f"   ✅ {name}: UP")
        else:
            print(f"   ❌ {name}: DOWN")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    up_count = 0
    for name, results in all_results.items():
        health_status = results.get("health", {}).get("status", "UNKNOWN")
        root_status = results.get("root", {}).get("status", "UNKNOWN")
        
        if health_status == "UP" or root_status == "UP":
            up_count += 1
            print(f"✅ {name}: UP")
        else:
            print(f"❌ {name}: DOWN")
    
    print(f"\nOverall Status: {up_count}/{len(MICROSERVICES)} UP")
    
    if up_count == len(MICROSERVICES):
        print("🎉 All microservices are running!")
    elif up_count > 0:
        print("⚠️  Some microservices are down")
    else:
        print("🚨 All microservices are down!")

if __name__ == "__main__":
    main() 