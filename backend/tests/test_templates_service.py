# /backend/tests/test_templates_service.py
import pytest
from templates_service import combine_templates
import os

def test_combine_templates(tmp_path):
    # Setup mock templates
    template1 = tmp_path / "template1"
    template1.mkdir()
    (template1 / "file1.js").write_text("console.log('Template1 File1');")
    
    template2 = tmp_path / "template2"
    template2.mkdir()
    (template2 / "file1.js").write_text("console.log('Template2 File1');")
    
    combined_dir = combine_templates(["template1", "template2"], tmp_path)
    
    files = os.listdir(combined_dir)
    assert len(files) == 2
    for file in files:
        assert "file1_template" in file
