#!/usr/bin/env python3
"""
Test Script for Malicious Phish Dataset
Tests a representative sample from the malicious_phish.csv dataset
"""

import requests
import json
import time
import csv
import random
from datetime import datetime
from typing import Dict, List, Any
import sys

class MaliciousPhishTester:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.results = []
        self.stats = {
            'total_tests': 0,
            'successful_tests': 0,
            'failed_tests': 0,
            'enhanced_content_analysis_found': 0,
            'malicious_detected': 0,
            'safe_detected': 0,
            'average_response_time': 0,
            'total_response_time': 0,
            'by_type': {
                'phishing': {'total': 0, 'detected': 0, 'missed': 0},
                'malware': {'total': 0, 'detected': 0, 'missed': 0},
                'defacement': {'total': 0, 'detected': 0, 'missed': 0},
                'benign': {'total': 0, 'detected': 0, 'missed': 0}
            }
        }
    
    def load_dataset_sample(self, filename: str = "src/main/resources/malicious_phish.csv", sample_size: int = 1000):
        """Load a representative sample from the dataset"""
        print(f"📊 Loading sample of {sample_size} URLs from {filename}...")
        
        test_cases = []
        type_counts = {'phishing': 0, 'malware': 0, 'defacement': 0, 'benign': 0}
        target_per_type = sample_size // 4  # Equal distribution
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    url = row.get('url', '').strip()
                    url_type = row.get('type', '').strip().lower()
                    
                    # Skip invalid entries
                    if not url or not url_type or url_type not in type_counts:
                        continue
                    
                    # Add http:// if missing
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    
                    # Sample based on type quotas
                    if type_counts[url_type] < target_per_type:
                        test_cases.append({
                            'url': url,
                            'type': url_type
                        })
                        type_counts[url_type] += 1
                    
                    # Stop if we have enough samples
                    if len(test_cases) >= sample_size:
                        break
        
        except FileNotFoundError:
            print(f"❌ Dataset file '{filename}' not found!")
            return []
        except Exception as e:
            print(f"❌ Error reading dataset: {e}")
            return []
        
        print(f"✅ Loaded {len(test_cases)} test cases:")
        for url_type, count in type_counts.items():
            print(f"   {url_type}: {count}")
        
        return test_cases
    
    def test_url(self, url: str, expected_type: str) -> Dict[str, Any]:
        """Test a single URL and return detailed results"""
        start_time = time.time()
        
        try:
            # Make the API call
            response = requests.post(
                f"{self.base_url}/api/scan",
                params={'url': url},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract detection methods
                detection_methods = list(data.get('detectionResults', {}).keys())
                enhanced_content_found = 'Enhanced Content Analysis' in detection_methods
                
                # Count malicious detections
                malicious_count = sum(
                    1 for result in data.get('detectionResults', {}).values()
                    if result.get('detected', False)
                )
                
                # Determine overall classification
                overall_malicious = data.get('malicious', False)
                
                # Determine if detection was correct
                expected_malicious = expected_type in ['phishing', 'malware', 'defacement']
                detection_correct = overall_malicious == expected_malicious
                
                result = {
                    'url': url,
                    'expected_type': expected_type,
                    'expected_malicious': expected_malicious,
                    'response_time': round(response_time, 3),
                    'status_code': response.status_code,
                    'success': True,
                    'enhanced_content_analysis_found': enhanced_content_found,
                    'detection_methods': detection_methods,
                    'malicious_detections': malicious_count,
                    'overall_malicious': overall_malicious,
                    'detection_correct': detection_correct,
                    'detection_results': data.get('detectionResults', {}),
                    'error': None
                }
                
                # Update statistics
                self.stats['successful_tests'] += 1
                self.stats['total_response_time'] += response_time
                if enhanced_content_found:
                    self.stats['enhanced_content_analysis_found'] += 1
                if overall_malicious:
                    self.stats['malicious_detected'] += 1
                else:
                    self.stats['safe_detected'] += 1
                
                # Update type-specific statistics
                if expected_type in self.stats['by_type']:
                    self.stats['by_type'][expected_type]['total'] += 1
                    if detection_correct:
                        if expected_malicious:
                            self.stats['by_type'][expected_type]['detected'] += 1
                        else:
                            self.stats['by_type'][expected_type]['detected'] += 1
                    else:
                        self.stats['by_type'][expected_type]['missed'] += 1
                
            else:
                result = {
                    'url': url,
                    'expected_type': expected_type,
                    'expected_malicious': expected_type in ['phishing', 'malware', 'defacement'],
                    'response_time': round(response_time, 3),
                    'status_code': response.status_code,
                    'success': False,
                    'enhanced_content_analysis_found': False,
                    'detection_methods': [],
                    'malicious_detections': 0,
                    'overall_malicious': False,
                    'detection_correct': False,
                    'detection_results': {},
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                self.stats['failed_tests'] += 1
                
        except Exception as e:
            response_time = time.time() - start_time
            result = {
                'url': url,
                'expected_type': expected_type,
                'expected_malicious': expected_type in ['phishing', 'malware', 'defacement'],
                'response_time': round(response_time, 3),
                'status_code': None,
                'success': False,
                'enhanced_content_analysis_found': False,
                'detection_methods': [],
                'malicious_detections': 0,
                'overall_malicious': False,
                'detection_correct': False,
                'detection_results': {},
                'error': str(e)
            }
            self.stats['failed_tests'] += 1
        
        self.stats['total_tests'] += 1
        return result
    
    def run_dataset_test(self, sample_size: int = 1000):
        """Run test on the malicious phish dataset"""
        print("🚀 Starting Malicious Phish Dataset Test")
        print("=" * 60)
        
        # Load test dataset
        test_cases = self.load_dataset_sample(sample_size=sample_size)
        if not test_cases:
            print("❌ No test cases found. Exiting.")
            return
        
        print(f"📊 Testing {len(test_cases)} URLs from malicious_phish.csv")
        print()
        
        # Test each URL
        for i, test_case in enumerate(test_cases, 1):
            url = test_case['url']
            url_type = test_case['type']
            
            print(f"Testing {i}/{len(test_cases)}: {url[:60]}...")
            print(f"  Type: {url_type}")
            
            result = self.test_url(url, url_type)
            self.results.append(result)
            
            # Print result summary
            if result['success']:
                status = "✅ SUCCESS" if result['enhanced_content_analysis_found'] else "⚠️  NO ENHANCED ANALYSIS"
                malicious = "🔴 MALICIOUS" if result['overall_malicious'] else "🟢 SAFE"
                correct = "✅ CORRECT" if result['detection_correct'] else "❌ WRONG"
                print(f"  {status} | {malicious} | {correct} | {result['response_time']}s")
            else:
                print(f"  ❌ FAILED: {result['error']}")
            
            print()
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        # Calculate final statistics
        if self.stats['successful_tests'] > 0:
            self.stats['average_response_time'] = self.stats['total_response_time'] / self.stats['successful_tests']
        
        # Print comprehensive results
        self.print_dataset_results()
        
        # Save results to files
        self.save_results()
    
    def print_dataset_results(self):
        """Print comprehensive test results"""
        print("📈 MALICIOUS PHISH DATASET TEST RESULTS")
        print("=" * 60)
        
        # Overall statistics
        print(f"Total Tests: {self.stats['total_tests']}")
        print(f"Successful: {self.stats['successful_tests']}")
        print(f"Failed: {self.stats['failed_tests']}")
        print(f"Success Rate: {(self.stats['successful_tests'] / self.stats['total_tests'] * 100):.1f}%")
        print()
        
        # Enhanced Content Analysis statistics
        print(f"Enhanced Content Analysis Found: {self.stats['enhanced_content_analysis_found']}")
        print(f"Enhanced Content Analysis Rate: {(self.stats['enhanced_content_analysis_found'] / self.stats['successful_tests'] * 100):.1f}%")
        print()
        
        # Detection statistics
        print(f"Malicious Detected: {self.stats['malicious_detected']}")
        print(f"Safe Detected: {self.stats['safe_detected']}")
        print(f"Malicious Rate: {(self.stats['malicious_detected'] / self.stats['successful_tests'] * 100):.1f}%")
        print()
        
        # Performance statistics
        print(f"Average Response Time: {self.stats['average_response_time']:.3f}s")
        print(f"Total Response Time: {self.stats['total_response_time']:.3f}s")
        print()
        
        # Results by type
        print("📊 RESULTS BY TYPE")
        print("-" * 60)
        print(f"{'Type':<12} | {'Total':<6} | {'Detected':<9} | {'Missed':<7} | {'Accuracy':<8} | {'Precision':<9}")
        print("-" * 60)
        
        total_correct = 0
        total_tests = 0
        
        for url_type, stats in self.stats['by_type'].items():
            if stats['total'] > 0:
                accuracy = (stats['detected'] / stats['total'] * 100)
                precision = (stats['detected'] / stats['total'] * 100)  # Simplified precision
                total_correct += stats['detected']
                total_tests += stats['total']
                
                print(f"{url_type:<12} | {stats['total']:<6} | {stats['detected']:<9} | {stats['missed']:<7} | {accuracy:<8.1f}% | {precision:<9.1f}%")
        
        print("-" * 60)
        overall_accuracy = (total_correct / total_tests * 100) if total_tests > 0 else 0
        print(f"{'OVERALL':<12} | {total_tests:<6} | {total_correct:<9} | {(total_tests - total_correct):<7} | {overall_accuracy:<8.1f}% | {overall_accuracy:<9.1f}%")
        print()
        
        # Detection methods analysis
        print("🔍 DETECTION METHODS ANALYSIS")
        print("-" * 40)
        method_counts = {}
        for result in self.results:
            if result['success']:
                for method in result['detection_methods']:
                    method_counts[method] = method_counts.get(method, 0) + 1
        
        for method, count in sorted(method_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.stats['successful_tests'] * 100)
            print(f"{method:30} | {count:3} times ({percentage:5.1f}%)")
    
    def save_results(self):
        """Save results to CSV and JSON files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results to JSON
        json_filename = f"malicious_phish_test_results_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'statistics': self.stats,
                'results': self.results
            }, f, indent=2)
        
        # Save summary to CSV
        csv_filename = f"malicious_phish_test_summary_{timestamp}.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'URL', 'Expected Type', 'Expected Malicious', 'Success', 'Response Time', 'Status Code',
                'Enhanced Content Analysis', 'Detection Methods Count', 'Malicious Detections',
                'Overall Malicious', 'Detection Correct', 'Error'
            ])
            
            for result in self.results:
                writer.writerow([
                    result['url'],
                    result['expected_type'],
                    result['expected_malicious'],
                    result['success'],
                    result['response_time'],
                    result['status_code'],
                    result['enhanced_content_analysis_found'],
                    len(result['detection_methods']),
                    result['malicious_detections'],
                    result['overall_malicious'],
                    result['detection_correct'],
                    result['error'] or ''
                ])
        
        print(f"💾 Results saved to:")
        print(f"   JSON: {json_filename}")
        print(f"   CSV:  {csv_filename}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8080"
    
    if len(sys.argv) > 2:
        sample_size = int(sys.argv[2])
    else:
        sample_size = 1000  # Default sample size
    
    print(f"🎯 Testing against: {base_url}")
    print(f"📊 Sample size: {sample_size} URLs")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/actuator/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server health check failed: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running with: ./run.sh start")
        return
    
    # Run dataset test
    tester = MaliciousPhishTester(base_url)
    tester.run_dataset_test(sample_size)

if __name__ == "__main__":
    main() 