#!/usr/bin/env python3
"""
Test script to verify improvements in malicious URL detection
Tests both safe and malicious URLs to check for reduced false positives
"""

import requests
import json
import time
from datetime import datetime

# Test URLs - mix of safe and malicious
TEST_URLS = {
    "safe": [
        "https://www.google.com",
        "https://www.facebook.com", 
        "https://www.amazon.com",
        "https://www.microsoft.com",
        "https://www.apple.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
        "https://www.paypal.com",
        "https://www.ebay.com",
        "https://www.netflix.com",
        "https://www.youtube.com",
        "https://www.linkedin.com",
        "https://www.twitter.com",
        "https://www.instagram.com"
    ],
    "malicious": [
        "http://malware-test.com",
        "http://phishing-scam.net",
        "http://virus-download.xyz",
        "http://hack-crack.tk",
        "http://trojan-spyware.ml",
        "http://fake-login.ga",
        "http://malicious-software.cf",
        "http://scam-website.gq",
        "http://fake-banking.top",
        "http://malware-download.club",
        "http://phishing-scam.net",  # Duplicate to test if it gets caught now
        "http://malware-download.xyz",
        "http://fake-paypal-login.com",
        "http://virus-download.tk",
        "http://hack-tools.ml"
    ]
}

def test_url(url, expected_type):
    """Test a single URL and return results"""
    try:
        # Send as query parameter, not JSON body
        response = requests.post(
            "http://localhost:8080/api/scan",
            params={"url": url},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            is_malicious = result.get("malicious", False)
            confidence = result.get("confidenceScore", 0.0)
            status = result.get("overallStatus", "UNKNOWN")
            
            # Check if result matches expectation
            correct = (is_malicious == (expected_type == "malicious"))
            
            return {
                "url": url,
                "expected": expected_type,
                "detected_malicious": is_malicious,
                "confidence": confidence,
                "status": status,
                "correct": correct,
                "success": True
            }
        else:
            return {
                "url": url,
                "expected": expected_type,
                "detected_malicious": None,
                "confidence": None,
                "status": f"HTTP {response.status_code}",
                "correct": False,
                "success": False
            }
    except Exception as e:
        return {
            "url": url,
            "expected": expected_type,
            "detected_malicious": None,
            "confidence": None,
            "status": f"Error: {str(e)}",
            "correct": False,
            "success": False
        }

def main():
    print("Testing Malicious URL Detector Improvements")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    print()
    
    all_results = []
    
    # Test safe URLs
    print("Testing SAFE URLs (should NOT be detected as malicious):")
    print("-" * 50)
    safe_results = []
    for url in TEST_URLS["safe"]:
        result = test_url(url, "safe")
        safe_results.append(result)
        all_results.append(result)
        
        status_icon = "✅" if result["correct"] else "❌"
        print(f"{status_icon} {url}")
        print(f"   Expected: SAFE, Detected: {'MALICIOUS' if result['detected_malicious'] else 'SAFE'}")
        confidence_str = f"{result['confidence']:.2f}" if result['confidence'] is not None else "N/A"
        print(f"   Confidence: {confidence_str}, Status: {result['status']}")
        print()
        time.sleep(0.5)  # Small delay between requests
    
    # Test malicious URLs
    print("Testing MALICIOUS URLs (should be detected as malicious):")
    print("-" * 50)
    malicious_results = []
    for url in TEST_URLS["malicious"]:
        result = test_url(url, "malicious")
        malicious_results.append(result)
        all_results.append(result)
        
        status_icon = "✅" if result["correct"] else "❌"
        print(f"{status_icon} {url}")
        print(f"   Expected: MALICIOUS, Detected: {'MALICIOUS' if result['detected_malicious'] else 'SAFE'}")
        confidence_str = f"{result['confidence']:.2f}" if result['confidence'] is not None else "N/A"
        print(f"   Confidence: {confidence_str}, Status: {result['status']}")
        print()
        time.sleep(0.5)  # Small delay between requests
    
    # Summary
    print("SUMMARY")
    print("=" * 50)
    
    # Safe URL results
    safe_correct = sum(1 for r in safe_results if r["correct"])
    safe_total = len(safe_results)
    safe_false_positives = safe_total - safe_correct
    
    print(f"Safe URLs:")
    print(f"  Total: {safe_total}")
    print(f"  Correctly identified as safe: {safe_correct}")
    print(f"  False positives (incorrectly flagged as malicious): {safe_false_positives}")
    print(f"  False positive rate: {(safe_false_positives/safe_total)*100:.1f}%")
    print()
    
    # Malicious URL results
    malicious_correct = sum(1 for r in malicious_results if r["correct"])
    malicious_total = len(malicious_results)
    malicious_false_negatives = malicious_total - malicious_correct
    
    print(f"Malicious URLs:")
    print(f"  Total: {malicious_total}")
    print(f"  Correctly identified as malicious: {malicious_correct}")
    print(f"  False negatives (missed malicious URLs): {malicious_false_negatives}")
    print(f"  Detection rate: {(malicious_correct/malicious_total)*100:.1f}%")
    print()
    
    # Overall results
    total_correct = safe_correct + malicious_correct
    total_tests = len(all_results)
    overall_accuracy = (total_correct / total_tests) * 100
    
    print(f"Overall Results:")
    print(f"  Total tests: {total_tests}")
    print(f"  Correct classifications: {total_correct}")
    print(f"  Overall accuracy: {overall_accuracy:.1f}%")
    print()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "test_timestamp": datetime.now().isoformat(),
            "summary": {
                "safe_urls": {
                    "total": safe_total,
                    "correct": safe_correct,
                    "false_positives": safe_false_positives,
                    "false_positive_rate": (safe_false_positives/safe_total)*100
                },
                "malicious_urls": {
                    "total": malicious_total,
                    "correct": malicious_correct,
                    "false_negatives": malicious_false_negatives,
                    "detection_rate": (malicious_correct/malicious_total)*100
                },
                "overall": {
                    "total_tests": total_tests,
                    "correct_classifications": total_correct,
                    "accuracy": overall_accuracy
                }
            },
            "detailed_results": all_results
        }, f, indent=2)
    
    print(f"Detailed results saved to: {filename}")
    
    # Recommendations
    print("\nRECOMMENDATIONS:")
    print("-" * 20)
    
    if safe_false_positives > 0:
        print(f"⚠️  {safe_false_positives} false positives detected. Consider:")
        print("   - Adding more domains to whitelist")
        print("   - Further reducing sensitivity thresholds")
        print("   - Adjusting pattern detection rules")
    else:
        print("✅ No false positives! Whitelist and threshold adjustments working well.")
    
    if malicious_false_negatives > 0:
        print(f"⚠️  {malicious_false_negatives} malicious URLs missed. Consider:")
        print("   - Adding more detection patterns")
        print("   - Lowering detection thresholds")
        print("   - Improving ML model features")
    else:
        print("✅ All malicious URLs detected! Detection sensitivity is good.")
    
    if overall_accuracy >= 90:
        print("🎉 Excellent overall accuracy! The system is working well.")
    elif overall_accuracy >= 80:
        print("👍 Good overall accuracy. Minor adjustments may be needed.")
    else:
        print("⚠️  Overall accuracy needs improvement. Review detection logic.")

if __name__ == "__main__":
    main() 