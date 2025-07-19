"""
Unit tests for ML Microservice
"""
import unittest
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path to import the microservice
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_microservice'))

from python_microservice.app import create_app
from python_microservice.model_manager import ModelManager
from python_microservice.config import Config

class TestModelManager(unittest.TestCase):
    """Test cases for ModelManager"""
    
    def setUp(self):
        self.model_manager = ModelManager()
    
    @patch('python_microservice.model_manager.AutoTokenizer.from_pretrained')
    @patch('python_microservice.model_manager.AutoModelForSequenceClassification.from_pretrained')
    def test_load_model_success(self, mock_model, mock_tokenizer):
        """Test successful model loading"""
        # Mock the model and tokenizer
        mock_tokenizer.return_value = Mock()
        mock_model.return_value = Mock()
        
        # Test loading
        result = self.model_manager.load_model('test-model')
        
        self.assertTrue(result)
        self.assertIsNotNone(self.model_manager.model)
        self.assertIsNotNone(self.model_manager.tokenizer)
    
    def test_predict_without_model(self):
        """Test prediction without loaded model"""
        with self.assertRaises(RuntimeError):
            self.model_manager.predict("https://example.com")
    
    def test_get_model_info(self):
        """Test model info retrieval"""
        info = self.model_manager.get_model_info()
        
        self.assertIn('model_name', info)
        self.assertIn('device', info)
        self.assertIn('max_length', info)
        self.assertIn('loaded', info)
    
    def test_is_loaded(self):
        """Test model loaded status"""
        # Initially not loaded
        self.assertFalse(self.model_manager.is_loaded())
        
        # Mock loading
        self.model_manager.model = Mock()
        self.model_manager.tokenizer = Mock()
        
        self.assertTrue(self.model_manager.is_loaded())

class TestConfig(unittest.TestCase):
    """Test cases for Config"""
    
    def test_get_model_name(self):
        """Test model name retrieval"""
        model_name = Config.get_model_name()
        self.assertIsInstance(model_name, str)
    
    def test_get_device(self):
        """Test device retrieval"""
        device = Config.get_device()
        self.assertIn(device, ['cpu', 'cuda'])
    
    def test_get_server_config(self):
        """Test server config retrieval"""
        config = Config.get_server_config()
        
        self.assertIn('host', config)
        self.assertIn('port', config)
        self.assertIn('debug', config)
        self.assertIsInstance(config['port'], int)

class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', data)
        self.assertIn('service', data)
        self.assertIn('model_loaded', data)
    
    def test_model_info(self):
        """Test model info endpoint"""
        response = self.client.get('/info')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('service', data)
        self.assertIn('model_info', data)
        self.assertIn('config', data)
    
    def test_predict_missing_url(self):
        """Test prediction with missing URL"""
        response = self.client.post('/predict', 
                                 data=json.dumps({}),
                                 content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_predict_invalid_url(self):
        """Test prediction with invalid URL"""
        response = self.client.post('/predict',
                                 data=json.dumps({'url': ''}),
                                 content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_predict_valid_url(self):
        """Test prediction with valid URL"""
        # Mock the model manager to avoid actual model loading
        with patch.object(self.app, 'model_manager') as mock_manager:
            mock_manager.predict.return_value = ('safe', 0.8)
            mock_manager.model_name = 'test-model'
            
            response = self.client.post('/predict',
                                     data=json.dumps({'url': 'https://example.com'}),
                                     content_type='application/json')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('url', data)
            self.assertIn('prediction', data)
            self.assertIn('confidence', data)
            self.assertIn('model', data)

if __name__ == '__main__':
    unittest.main() 