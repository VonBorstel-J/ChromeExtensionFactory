# /backend/tests/test_security.py
import pytest
from app import app

def test_csp_headers(client):
    response = client.get('/auth/login')
    assert 'Content-Security-Policy' in response.headers
    assert "default-src 'self'" in response.headers['Content-Security-Policy']

def test_rate_limiting(client):
    for _ in range(201):
        response = client.get('/test/health')
        if _ < 200:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
            assert "Too Many Requests" in response.get_data(as_text=True)
