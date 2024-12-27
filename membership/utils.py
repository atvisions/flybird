import base64
from django.conf import settings
from pathlib import Path

def get_logo_base64():
    """获取 logo 的 base64 编码"""
    logo_path = settings.BASE_DIR / 'static/images/logo.png'
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    return base64.b64encode(logo_data).decode() 