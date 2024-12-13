# /backend/templates_service.py 
import os
import tempfile
import shutil
import uuid

def combine_templates(template_names, base_path):
    temp_dir = tempfile.mkdtemp()
    for tmpl in template_names:
        tmpl_dir = os.path.join(base_path, tmpl)
        for filename in os.listdir(tmpl_dir):
            src = os.path.join(tmpl_dir, filename)
            if os.path.isfile(src):
                base, ext = os.path.splitext(filename)
                unique_suffix = uuid.uuid4().hex[:6]
                dst = os.path.join(temp_dir, f"{base}_{tmpl}_{unique_suffix}{ext}")
                shutil.copy(src, dst)
    return temp_dir
