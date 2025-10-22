import pytest
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_endpoint(client):
    """Test root endpoint returns correct data"""
    response = client.get('/')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['message'] == "Hello from Simple App!"
    assert data['version'] == "1.0.0"
    assert data['environment'] == 'development'


def test_hello_endpoint_with_environment(monkeypatch):
    """Test root endpoint with different environment"""
    monkeypatch.setenv('ENVIRONMENT', 'production')
    
    # Re-import to pick up new environment variable
    import importlib
    import app as app_module
    importlib.reload(app_module)
    
    with app_module.app.test_client() as client:
        response = client.get('/')
        data = response.get_json()
        assert data['environment'] == 'production'


def test_health_endpoint(client):
    """Test health endpoint"""
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"


def test_info_endpoint(client):
    """Test info endpoint"""
    response = client.get('/info')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['app'] == "Simple Python App"
    assert data['maintainer'] == "DevOps Team"
    assert data['language'] == "Python"


def test_nonexistent_endpoint(client):
    """Test 404 for non-existent endpoints"""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_method_not_allowed(client):
    """Test 405 for unsupported methods"""
    response = client.post('/')
    assert response.status_code == 405


def test_response_content_type(client):
    """Test responses are JSON"""
    endpoints = ['/', '/health', '/info']
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.content_type == 'application/json'
