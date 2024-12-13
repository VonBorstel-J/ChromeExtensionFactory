# /backend/tests/test_tasks.py
import pytest
from tasks.celery_worker import async_generate_code

def test_async_generate_code():
    result = async_generate_code.delay("test_idea", "web_scraper", "openai")
    assert result is not None
    assert isinstance(result.id, str)
