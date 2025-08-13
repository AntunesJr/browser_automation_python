# ==============================================
# authenticator/config/config.py
# version: 0.2.1
# author: silvioantunes1@hotmail.com
# ==============================================

# Copyright (C) 2025 Silvio Antunes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from pathlib import Path
from typing import Optional, Tuple
from credentials.message.msg_code import MsgCode

# Default configuration
DEFAULT_FOLDER_NAME = '.credentials'
DEFAULT_CREDENTIALS_NAME = 'credentials.enc'
DEFAULT_KEY_NAME = 'key.key'
HOME_DIR = Path.home()

# Secure file permissions (read/write for owner only)
SECURE_FILE_MODE = 0o600
SECURE_DIR_MODE = 0o700

class CredentialsConfig:
    # Configuration manager for credentials storage paths.

    def __init__(
        self,
        base_directory: Optional[ Path ] = None,
        folder_name: Optional[ str ] = None,
        credentials_filename: Optional[ str ] = None,
        key_filename: Optional[ str ] = None
    ) -> None:
        # Initialize configuration with custom or default paths.
        # Args:
            # base_directory: Base directory for credentials folder (default: home)
            # folder_name: Name of credentials folder (default: .credentials)
            # credentials_filename: Name of credentials file (default: credentials.enc)
            # key_filename: Name of key file (default: key.key)

        self._base_dir = base_directory or HOME_DIR
        self._folder_name = folder_name or DEFAULT_FOLDER_NAME
        self._credentials_name = credentials_filename or DEFAULT_CREDENTIALS_NAME
        self._key_name = key_filename or DEFAULT_KEY_NAME
        
        # Build full paths
        self._credentials_dir = self._base_dir / self._folder_name
        self._credentials_file = self._credentials_dir / self._credentials_name
        self._key_file = self._credentials_dir / self._key_name
    
    @property
    def credentials_dir( self ) -> Path:
        # Get credentials directory path.
        return self._credentials_dir

    @property
    def credentials_file( self ) -> Path:
        # Get credentials file path.
        return self._credentials_file
    
    @property
    def key_file( self ) -> Path:
        # Get key file path.
        return self._key_file

    def ensure_secure_directory( self ) -> MsgCode:
        # Ensure the credentials directory exists with secure permissions.
        # Returns:
            # MsgCode: Success or error code. 

        try:
            self._credentials_dir.mkdir( mode = SECURE_DIR_MODE, exist_ok = True )
            return MsgCode.SUCCESS
        except PermissionError:
            return MsgCode.PERMISSION_DIR_ERROR
        except OSError:
            return MsgCode.IO__DIR_ERROR
        except Exception:
            return MsgCode.UNKNOWN_DIR_ERROR

# Global default configuration instance
default_config = CredentialsConfig()