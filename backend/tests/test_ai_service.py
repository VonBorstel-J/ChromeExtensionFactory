# /backend/tests/test_ai_service.py
import pytest
from unittest.mock import patch
from ai_service import generate_code_snippet

@patch('ai_service.openai.Completion.create')
def test_generate_code_snippet(mock_create):
    mock_create.return_value = {
        "choices": [{"text": "console.log('Hello World');"}]
    }
    code = generate_code_snippet("Build a tab manager", "tab_manager")
    assert code == "console.log('Hello World');"
