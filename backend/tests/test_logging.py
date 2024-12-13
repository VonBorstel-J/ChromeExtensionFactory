# /backend/tests/test_logging.py
import pytest
from app import app
from unittest.mock import patch

def test_logging_on_error(client, caplog):
    with caplog.at_level(logging.ERROR):
        response = client.post('/auth/login', json={"email":"invalid","password":"invalid"})
        assert response.status_code == 401
        assert "Invalid credentials" in response.get_data(as_text=True)
        assert "ERROR" in caplog.text
