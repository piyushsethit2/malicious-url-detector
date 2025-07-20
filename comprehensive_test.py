#!/usr/bin/env python3
"""
Comprehensive Test Script for Malicious URL Detection System
Tests all URLs in the dataset and generates detailed results
"""

import requests
import json
import time
import csv
from datetime import datetime
from typing import Dict, List, Any
import sys

class ComprehensiveTester:
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
            'total_response_time': 0
        }
    
    def test_url(self, url: str, expected_category: str = "unknown") -> Dict[str, Any]:
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
                    if result.get('isMalicious', False)
                )
                
                # Determine overall classification
                overall_malicious = malicious_count > 0
                
                result = {
                    'url': url,
                    'expected_category': expected_category,
                    'response_time': round(response_time, 3),
                    'status_code': response.status_code,
                    'success': True,
                    'enhanced_content_analysis_found': enhanced_content_found,
                    'detection_methods': detection_methods,
                    'malicious_detections': malicious_count,
                    'overall_malicious': overall_malicious,
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
                
            else:
                result = {
                    'url': url,
                    'expected_category': expected_category,
                    'response_time': round(response_time, 3),
                    'status_code': response.status_code,
                    'success': False,
                    'enhanced_content_analysis_found': False,
                    'detection_methods': [],
                    'malicious_detections': 0,
                    'overall_malicious': False,
                    'detection_results': {},
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                self.stats['failed_tests'] += 1
                
        except Exception as e:
            response_time = time.time() - start_time
            result = {
                'url': url,
                'expected_category': expected_category,
                'response_time': round(response_time, 3),
                'status_code': None,
                'success': False,
                'enhanced_content_analysis_found': False,
                'detection_methods': [],
                'malicious_detections': 0,
                'overall_malicious': False,
                'detection_results': {},
                'error': str(e)
            }
            self.stats['failed_tests'] += 1
        
        self.stats['total_tests'] += 1
        return result
    
    def load_test_dataset(self, filename: str = "test_dataset.txt") -> List[Dict[str, str]]:
        """Load test dataset from file"""
        test_cases = []
        current_category = "unknown"
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        # Extract category from comment
                        if 'Safe URLs' in line:
                            current_category = "safe"
                        elif 'Suspicious URLs' in line or 'High-risk URLs' in line:
                            current_category = "suspicious"
                        elif 'URL shortening services' in line:
                            current_category = "url_shortener"
                        elif 'Private IP addresses' in line:
                            current_category = "private_ip"
                        elif 'Suspicious file extensions' in line:
                            current_category = "suspicious_extension"
                        elif 'Obfuscated URLs' in line:
                            current_category = "obfuscated"
                        elif 'Legitimate but potentially suspicious keywords' in line:
                            current_category = "suspicious_keywords"
                        elif 'Random-looking domains' in line:
                            current_category = "random_domain"
                        continue
                    
                    if line.startswith('http'):
                        test_cases.append({
                            'url': line,
                            'category': current_category
                        })
        
        except FileNotFoundError:
            print(f"Error: Test dataset file '{filename}' not found!")
            return []
        
        return test_cases
    
    def run_comprehensive_test(self, dataset_file: str = "test_dataset.txt"):
        """Run comprehensive test on all URLs in the dataset"""
        print("🚀 Starting Comprehensive Malicious URL Detection Test")
        print("=" * 60)
        
        # Load test dataset
        test_cases = self.load_test_dataset(dataset_file)
        if not test_cases:
            print("❌ No test cases found. Exiting.")
            return
        
        print(f"📊 Loaded {len(test_cases)} test cases from {dataset_file}")
        print()
        
        # Test each URL
        for i, test_case in enumerate(test_cases, 1):
            url = test_case['url']
            category = test_case['category']
            
            print(f"Testing {i}/{len(test_cases)}: {url}")
            print(f"  Category: {category}")
            
            result = self.test_url(url, category)
            self.results.append(result)
            
            # Print result summary
            if result['success']:
                status = "✅ SUCCESS" if result['enhanced_content_analysis_found'] else "⚠️  NO ENHANCED ANALYSIS"
                malicious = "🔴 MALICIOUS" if result['overall_malicious'] else "🟢 SAFE"
                print(f"  {status} | {malicious} | {result['response_time']}s | {len(result['detection_methods'])} methods")
            else:
                print(f"  ❌ FAILED: {result['error']}")
            
            print()
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        # Calculate final statistics
        if self.stats['successful_tests'] > 0:
            self.stats['average_response_time'] = self.stats['total_response_time'] / self.stats['successful_tests']
        
        # Print comprehensive results
        self.print_comprehensive_results()
        
        # Save results to files
        self.save_results()
    
    def print_comprehensive_results(self):
        """Print comprehensive test results"""
        print("📈 COMPREHENSIVE TEST RESULTS")
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
        
        # Category breakdown
        print("📊 RESULTS BY CATEGORY")
        print("-" * 40)
        categories = {}
        for result in self.results:
            if result['success']:
                category = result['expected_category']
                if category not in categories:
                    categories[category] = {'total': 0, 'malicious': 0, 'enhanced': 0}
                categories[category]['total'] += 1
                if result['overall_malicious']:
                    categories[category]['malicious'] += 1
                if result['enhanced_content_analysis_found']:
                    categories[category]['enhanced'] += 1
        
        for category, stats in categories.items():
            malicious_rate = (stats['malicious'] / stats['total'] * 100) if stats['total'] > 0 else 0
            enhanced_rate = (stats['enhanced'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"{category:20} | {stats['total']:3} tests | {stats['malicious']:2} malicious ({malicious_rate:5.1f}%) | {stats['enhanced']:2} enhanced ({enhanced_rate:5.1f}%)")
        
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
        json_filename = f"test_results_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'statistics': self.stats,
                'results': self.results
            }, f, indent=2)
        
        # Save summary to CSV
        csv_filename = f"test_summary_{timestamp}.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'URL', 'Category', 'Success', 'Response Time', 'Status Code',
                'Enhanced Content Analysis', 'Detection Methods Count',
                'Malicious Detections', 'Overall Malicious', 'Error'
            ])
            
            for result in self.results:
                writer.writerow([
                    result['url'],
                    result['expected_category'],
                    result['success'],
                    result['response_time'],
                    result['status_code'],
                    result['enhanced_content_analysis_found'],
                    len(result['detection_methods']),
                    result['malicious_detections'],
                    result['overall_malicious'],
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
        dataset_file = sys.argv[2]
    else:
        dataset_file = "test_dataset.txt"
    
    print(f"🎯 Testing against: {base_url}")
    print(f"📁 Using dataset: {dataset_file}")
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
    
    # Run comprehensive test
    tester = ComprehensiveTester(base_url)
    tester.run_comprehensive_test(dataset_file)

if __name__ == "__main__":
    main() 