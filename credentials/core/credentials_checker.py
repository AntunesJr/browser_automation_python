# ==============================================
# authenticator/core/credentials_checker.py
# version: 0.0.1
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

from pathlib import Path
from typing import Dict, Any, Optional

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig

class CredentialsChecker:
    # Security checker for credentials files and permissions.
    
    def __init__(self, config: CredentialsConfig) -> None:
        # Initialize checker with configuration.
        # Args:
            # config: Configuration instance with file paths.

        self._config = config
    
    def check_directory( self ) -> MsgCode:
        # Ceck if the credentials directory exists and is secure.
        #  Returns:
           # MsgCode: Success or error code.
        try:
            if Path( self._config.credentials_dir ).is_dir():
                return MsgCode.SUCCESS
            return MISSING_DIR
        except PermissionError:
            return MsgCode.PERMISSION_DIR_ERROR
        except OSError:
            return MsgCode.IO_DIR_ERROR
        except Exception:
            return MsgCode.UNKNOWN_DIR_ERROR
    
    
    def check_credentials_file( self ) -> MsgCode:
        # Check if credentials file exists and has secure permissions.
        # Returns:
           # MsgCode: Success or specific error code.

        try:
            if not self._config.credentials_file.exists():
                return MsgCode.MISSING_CREDENTIALS_FILE
            
            if not self._check_file_permissions(self._config.credentials_file):
                return MsgCode.PERMISSION_CREDENTIALS_ERROR
            
            return MsgCode.SUCCESS
        
        except PermissionError:
            return MsgCode.PERMISSION_CREDENTIALS_FILE_ERROR
        except OSError:
            return MsgCode.IO_CREDENTIALS_FILE_ERROR
        except Exception:
            return MsgCode.UNKNOWN_CREDENTIALS_FILE_ERROR
    
    def check_key_file( self ) -> MsgCode:
        # Check if key file exists and has secure permissions.
        # Returns:
            # MsgCode: Success or specific error code.

        try:
            if not self._config.key_file.exists():
                return MsgCode.MISSING_KEY_FILE
            
            if not self._check_file_permissions(self._config.key_file):
                return MsgCode.PERMISSION_KEY_FILE_ERROR
            
            return MsgCode.SUCCESS
        
        except PermissionError:
            return MsgCode.PERMISSION_KEY_FILE_ERROR
        except OSError:
            return MsgCode.IO_KEY_ERROR
        except Exception:
            return MsgCode.UNKNOWN_KEY_FILE_ERROR

    def verify_credentials(
        self,
        stored_credentials: Optional[ Dict [ str, Any ] ],
        email: str,
        password: str
    ) -> MsgCode:
        # Verify provided credentials against stored credentials.
        # Args:
            # stored_credentials: Loaded credentials from storage.
            # email: Email to verify.
            # password: Password to verify.
        # Returns:
            # MsgCode: Verification result.

        if not stored_credentials:
            return MsgCode.CREDENTIALS_NULL
        
        if( stored_credentials.get( 'email' ) == email and
            stored_credentials.get( 'password' ) == password ):
            return MsgCode.SUCCESS
        
        return MsgCode.CREDENTIALS_INVALID
    
    def _check_file_permissions( self, file_path: Path ) -> bool:
        # Verify file has secure permissions (no group/other access).
        # Args:
            # file_path: Path to file being checked.
        # Returns:
            # bool: True if permissions are secure, False otherwise.

        try:
            if file_path.exists():
                stat = file_path.stat()
                # Check for group/other permissions
                if stat.st_mode & 0o077:
                    return False
            return True
        except Exception:
            return False