# /backend/tests/test_prometheus.py
import pytest
from prometheus_client import REGISTRY

def test_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert "http_requests_total" in response.get_data(as_text=True)
