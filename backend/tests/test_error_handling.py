# /backend/tests/test_error_handling.py
import pytest
from app import app

def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not found"

def test_500(client, mocker):
    mocker.patch('routes.auth_routes.signup', side_effect=Exception('Test Exception'))
    response = client.post('/auth/signup', json={"email":"error@test.com","password":"error"})
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"
