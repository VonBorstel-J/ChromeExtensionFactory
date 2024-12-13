# /backend/tests/test_rate_limiting.py
import pytest

def test_rate_limiting(client):
    for _ in range(201):
        response = client.get('/test/health')
        if _ < 200:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
            assert "Too Many Requests" in response.get_data(as_text=True)
