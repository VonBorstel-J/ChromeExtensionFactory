import os
import tempfile
import shutil

def combine_templates(template_names, base_path):
    temp_dir = tempfile.mkdtemp()
    for tmpl in template_names:
        tmpl_dir = os.path.join(base_path, tmpl)
        for filename in os.listdir(tmpl_dir):
            src = os.path.join(tmpl_dir, filename)
            dst = os.path.join(temp_dir, filename)
            if os.path.exists(dst):
                base, ext = os.path.splitext(filename)
                dst = os.path.join(temp_dir, f"{base}_{tmpl}{ext}")
            shutil.copy(src, dst)
    return temp_dir
