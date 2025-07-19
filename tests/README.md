# Tests

This directory contains all test files for the malicious URL detection system.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── README.md               # This file
├── test_ml_microservice.py # Unit tests for ML microservice
└── test_integration.py     # Integration tests for full system
```

## Test Categories

### 1. Unit Tests (`test_ml_microservice.py`)

Tests individual components of the ML microservice:

- **ModelManager**: Model loading, prediction, and management
- **Config**: Configuration settings and environment variables
- **Flask App**: API endpoints and request handling

**Running Unit Tests**:
```bash
cd tests
python -m unittest test_ml_microservice.py -v
```

### 2. Integration Tests (`test_integration.py`)

Tests the complete system integration:

- **ML Microservice Integration**: Health checks, predictions, model info
- **Java Backend Integration**: URL scanning, health endpoints
- **Full System Integration**: Complete workflow testing

**Running Integration Tests**:
```bash
cd tests
python test_integration.py
```

## Prerequisites

### For Unit Tests
- Python 3.7+
- Required packages: `flask`, `torch`, `transformers`, `unittest`

### For Integration Tests
- Python 3.7+
- Required packages: `requests`, `unittest`
- **Running Services**:
  - ML Microservice on `http://localhost:5001`
  - Java Backend on `http://localhost:8080`

## Running All Tests

### 1. Start Services First

**Start ML Microservice**:
```bash
cd python_microservice
python run.py
```

**Start Java Backend**:
```bash
mvn spring-boot:run
```

### 2. Run Tests

**Unit Tests Only**:
```bash
cd tests
python -m unittest test_ml_microservice.py -v
```

**Integration Tests Only**:
```bash
cd tests
python test_integration.py
```

**All Tests**:
```bash
cd tests
python -m unittest discover -v
```

## Test Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ML_SERVICE_URL` | `http://localhost:5001` | ML microservice URL |
| `JAVA_SERVICE_URL` | `http://localhost:8080` | Java backend URL |

### Test Data

The integration tests use predefined test URLs:

**Safe URLs**:
- `https://www.google.com`
- `https://www.facebook.com`

**Malicious URLs**:
- `http://malware-test.com`
- `http://phishing-scam.net`

## Test Results

### Unit Test Results
```
test_get_device (__main__.TestConfig) ... ok
test_get_model_name (__main__.TestConfig) ... ok
test_get_server_config (__main__.TestConfig) ... ok
test_health_check (__main__.TestFlaskApp) ... ok
test_is_loaded (__main__.TestModelManager) ... ok
test_load_model_success (__main__.TestModelManager) ... ok
test_model_info (__main__.TestFlaskApp) ... ok
test_predict_invalid_url (__main__.TestFlaskApp) ... ok
test_predict_missing_url (__main__.TestFlaskApp) ... ok
test_predict_valid_url (__main__.TestFlaskApp) ... ok
test_predict_without_model (__main__.TestModelManager) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.123s

OK
```

### Integration Test Results
```
Running Integration Tests...
==================================================

1. Testing ML Microservice...
test_ml_service_health (__main__.TestMLMicroserviceIntegration) ... ok
test_ml_service_info (__main__.TestMLMicroserviceIntegration) ... ok
test_ml_service_predictions (__main__.TestMLMicroserviceIntegration) ... ok

2. Testing Java Backend...
test_java_service_health (__main__.TestJavaBackendIntegration) ... ok
test_java_service_ml_health (__main__.TestJavaBackendIntegration) ... ok
test_java_service_url_scanning (__main__.TestJavaBackendIntegration) ... ok

3. Testing Full System Integration...
test_error_handling (__main__.TestFullSystemIntegration) ... ok
test_full_system_workflow (__main__.TestFullSystemIntegration) ... ok

==================================================
INTEGRATION TEST SUMMARY
==================================================
Total Tests: 8
Errors: 0
Failures: 0
Skipped: 0
Success Rate: 100.0%

✅ All integration tests passed!
```

## Adding New Tests

### Unit Tests
1. Create test class inheriting from `unittest.TestCase`
2. Add test methods starting with `test_`
3. Use mocking for external dependencies

Example:
```python
class TestNewFeature(unittest.TestCase):
    def test_new_functionality(self):
        # Test implementation
        self.assertEqual(expected, actual)
```

### Integration Tests
1. Add test methods to existing classes
2. Use real HTTP requests to test endpoints
3. Handle connection errors gracefully with `skipTest`

Example:
```python
def test_new_endpoint(self):
    try:
        response = requests.get(f"{self.service_url}/new-endpoint")
        self.assertEqual(response.status_code, 200)
    except requests.exceptions.ConnectionError:
        self.skipTest("Service not running")
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure you're in the correct directory
   - Check Python path includes parent directories

2. **Connection Errors**:
   - Verify services are running
   - Check URLs in test configuration

3. **Test Failures**:
   - Check service logs for errors
   - Verify test data is valid
   - Ensure model is loaded correctly

### Debug Mode

Run tests with verbose output:
```bash
python -m unittest test_ml_microservice.py -v
```

Run integration tests with detailed output:
```bash
python test_integration.py
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Unit Tests
  run: |
    cd tests
    python -m unittest test_ml_microservice.py

- name: Run Integration Tests
  run: |
    cd tests
    python test_integration.py
``` 