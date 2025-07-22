# ==============================================
# authenticator/config/config.py
# version: 0.1.0
# author: silvioantunes1@hotmail.com
# ==============================================

import os
from pathlib import Path

# Default file paths
HOME_DIR = Path.home()
CREDENTIALS_NAME = 'credentials.enc'
KEY_NAME = 'key.key'
CREDENTIALS_DIR = HOME_DIR / '.credentials'
CREDENTIALS_FILE = CREDENTIALS_DIR / CREDENTIALS_NAME
KEY_FILE = CREDENTIALS_DIR / KEY_NAME

# Secure file permissions (read/write for owner only)
SECURE_FILE_MODE = 0o600

def ensure_secure_directory() -> int:
    """Ensure the authenticator directory exists with secure permissions."""
    try:
        CREDENTIALS_DIR.mkdir(mode=0o700, exist_ok=True)
        return 0
    except Exception:
        return 104