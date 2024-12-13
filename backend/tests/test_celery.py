# /backend/tests/test_celery.py
import pytest
from tasks.celery_worker import async_generate_code
from unittest.mock import patch

@patch('tasks.celery_worker.generate_code_snippet')
def test_async_generate_code(mock_generate):
    mock_generate.return_value = "console.log('Generated Code');"
    result = async_generate_code.delay("Test Idea", "web_scraper", "openai")
    result_value = result.get(timeout=10)
    assert result_value["status"] == "success"
    assert result_value["code"] == "console.log('Generated Code');"
