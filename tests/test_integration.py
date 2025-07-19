"""
Integration tests for the complete malicious URL detection system
Tests both Python microservice and Java backend integration
"""
import unittest
import requests
import json
import time
import sys
import os

# Configuration
ML_SERVICE_URL = "http://localhost:5001"
JAVA_SERVICE_URL = "http://localhost:8080"

class TestMLMicroserviceIntegration(unittest.TestCase):
    """Integration tests for ML microservice"""
    
    def setUp(self):
        """Set up test environment"""
        self.ml_service_url = ML_SERVICE_URL
        self.test_urls = [
            "https://www.google.com",
            "https://www.facebook.com", 
            "http://malware-test.com",
            "http://phishing-scam.net"
        ]
    
    def test_ml_service_health(self):
        """Test ML service health endpoint"""
        try:
            response = requests.get(f"{self.ml_service_url}/health", timeout=10)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('status', data)
            self.assertIn('service', data)
            self.assertIn('model_loaded', data)
            
        except requests.exceptions.ConnectionError:
            self.skipTest("ML service not running")
    
    def test_ml_service_info(self):
        """Test ML service info endpoint"""
        try:
            response = requests.get(f"{self.ml_service_url}/info", timeout=10)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('service', data)
            self.assertIn('model_info', data)
            self.assertIn('config', data)
            
        except requests.exceptions.ConnectionError:
            self.skipTest("ML service not running")
    
    def test_ml_service_predictions(self):
        """Test ML service predictions"""
        try:
            for url in self.test_urls:
                response = requests.post(
                    f"{self.ml_service_url}/predict",
                    json={'url': url},
                    timeout=10
                )
                
                self.assertEqual(response.status_code, 200)
                
                data = response.json()
                self.assertIn('url', data)
                self.assertIn('prediction', data)
                self.assertIn('confidence', data)
                self.assertIn('model', data)
                
                # Validate prediction values
                self.assertIn(data['prediction'], ['safe', 'malicious'])
                self.assertGreaterEqual(data['confidence'], 0.0)
                self.assertLessEqual(data['confidence'], 1.0)
                
        except requests.exceptions.ConnectionError:
            self.skipTest("ML service not running")

class TestJavaBackendIntegration(unittest.TestCase):
    """Integration tests for Java backend"""
    
    def setUp(self):
        """Set up test environment"""
        self.java_service_url = JAVA_SERVICE_URL
        self.test_urls = [
            "https://www.google.com",
            "https://www.facebook.com",
            "http://malware-test.com",
            "http://phishing-scam.net"
        ]
    
    def test_java_service_health(self):
        """Test Java service health endpoint"""
        try:
            response = requests.get(f"{self.java_service_url}/api/scan/health", timeout=10)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('status', data)
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Java service not running")
    
    def test_java_service_ml_health(self):
        """Test Java service ML health endpoint"""
        try:
            response = requests.get(f"{self.java_service_url}/api/scan/ml/health", timeout=10)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('status', data)
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Java service not running")
    
    def test_java_service_url_scanning(self):
        """Test Java service URL scanning"""
        try:
            for url in self.test_urls:
                response = requests.post(
                    f"{self.java_service_url}/api/scan",
                    params={'url': url},
                    timeout=30
                )
                
                self.assertEqual(response.status_code, 200)
                
                data = response.json()
                self.assertIn('url', data)
                self.assertIn('overallStatus', data)
                self.assertIn('malicious', data)
                self.assertIn('detectionResults', data)
                
                # Validate response structure
                self.assertIsInstance(data['malicious'], bool)
                self.assertIn(data['overallStatus'], ['SAFE', 'MALICIOUS', 'SUSPICIOUS'])
                
        except requests.exceptions.ConnectionError:
            self.skipTest("Java service not running")

class TestFullSystemIntegration(unittest.TestCase):
    """Full system integration tests"""
    
    def setUp(self):
        """Set up test environment"""
        self.ml_service_url = ML_SERVICE_URL
        self.java_service_url = JAVA_SERVICE_URL
        
        # Test cases with expected results
        self.test_cases = [
            {
                'url': 'https://www.google.com',
                'expected_status': 'SAFE',
                'expected_malicious': False
            },
            {
                'url': 'https://www.facebook.com',
                'expected_status': 'SAFE', 
                'expected_malicious': False
            },
            {
                'url': 'http://malware-test.com',
                'expected_status': 'MALICIOUS',
                'expected_malicious': True
            },
            {
                'url': 'http://phishing-scam.net',
                'expected_status': 'MALICIOUS',
                'expected_malicious': True
            }
        ]
    
    def test_full_system_workflow(self):
        """Test complete system workflow"""
        try:
            # Test ML service is available
            ml_health = requests.get(f"{self.ml_service_url}/health", timeout=10)
            self.assertEqual(ml_health.status_code, 200)
            
            # Test Java service is available
            java_health = requests.get(f"{self.java_service_url}/api/scan/health", timeout=10)
            self.assertEqual(java_health.status_code, 200)
            
            # Test complete workflow
            for test_case in self.test_cases:
                url = test_case['url']
                
                # Test ML service prediction
                ml_response = requests.post(
                    f"{self.ml_service_url}/predict",
                    json={'url': url},
                    timeout=10
                )
                self.assertEqual(ml_response.status_code, 200)
                
                # Test Java service scan
                java_response = requests.post(
                    f"{self.java_service_url}/api/scan",
                    params={'url': url},
                    timeout=30
                )
                self.assertEqual(java_response.status_code, 200)
                
                java_data = java_response.json()
                
                # Verify ML integration is working
                if 'TransformerML' in java_data.get('detectionResults', {}):
                    ml_result = java_data['detectionResults']['TransformerML']
                    self.assertIn('status', ml_result)
                    self.assertIn('confidence', ml_result)
                
        except requests.exceptions.ConnectionError:
            self.skipTest("Services not running")
    
    def test_error_handling(self):
        """Test error handling in the system"""
        try:
            # Test invalid URL
            response = requests.post(
                f"{self.java_service_url}/api/scan",
                params={'url': 'invalid-url'},
                timeout=10
            )
            
            # Should still return 200 but with appropriate status
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('url', data)
            self.assertIn('overallStatus', data)
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Java service not running")

def run_integration_tests():
    """Run all integration tests"""
    print("Running Integration Tests...")
    print("=" * 50)
    
    # Test ML Microservice
    print("\n1. Testing ML Microservice...")
    ml_tests = unittest.TestLoader().loadTestsFromTestCase(TestMLMicroserviceIntegration)
    ml_result = unittest.TextTestRunner(verbosity=2).run(ml_tests)
    
    # Test Java Backend
    print("\n2. Testing Java Backend...")
    java_tests = unittest.TestLoader().loadTestsFromTestCase(TestJavaBackendIntegration)
    java_result = unittest.TextTestRunner(verbosity=2).run(java_tests)
    
    # Test Full System
    print("\n3. Testing Full System Integration...")
    system_tests = unittest.TestLoader().loadTestsFromTestCase(TestFullSystemIntegration)
    system_result = unittest.TextTestRunner(verbosity=2).run(system_tests)
    
    # Summary
    print("\n" + "=" * 50)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    total_tests = ml_result.testsRun + java_result.testsRun + system_result.testsRun
    total_errors = len(ml_result.errors) + len(java_result.errors) + len(system_result.errors)
    total_failures = len(ml_result.failures) + len(java_result.failures) + len(system_result.failures)
    total_skipped = len(ml_result.skipped) + len(java_result.skipped) + len(system_result.skipped)
    
    print(f"Total Tests: {total_tests}")
    print(f"Errors: {total_errors}")
    print(f"Failures: {total_failures}")
    print(f"Skipped: {total_skipped}")
    print(f"Success Rate: {((total_tests - total_errors - total_failures) / total_tests * 100):.1f}%")
    
    if total_errors == 0 and total_failures == 0:
        print("\n✅ All integration tests passed!")
    else:
        print("\n❌ Some integration tests failed!")
    
    return total_errors == 0 and total_failures == 0

if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1) 