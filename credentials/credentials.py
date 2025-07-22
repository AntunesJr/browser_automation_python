# ==============================================
# authenticator/Credentials.py
# version: 0.0.3
# author: silvioantunes1@hotmail.com
#  ==============================================

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
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from credentials.config.config import (
    CREDENTIALS_FILE,
    KEY_FILE,
    SECURE_FILE_MODE,
    ensure_secure_directory,
)
from credentials.msg.message import MsgCode


class Credentials:
    # Secure credential management with encryption.

    def __init__(
        self,
        key_file: Optional[Path] = None,
        credentials_file: Optional[ Path ] = None,
    ) -> None:
    
        # Initialize credentials manager.
        # Args:
            # key_file: Path to encryption key file.
            # credentials_file: Path to credentials file.

        self._credentials_file = credentials_file or CREDENTIALS_FILE
        self._key_file = key_file or KEY_FILE
        self._fernet: Optional[ Fernet ] = None

    def __del__( self ) -> None:
    
        # Clean up resources on deletion.
        
        self._credentials_file = None
        self._key_file = None
        self._fernet = None

    def _check_directory( self ) -> MsgCode:
    
        # Check if the credentials directory exists and is secure.
        # Returns:
            # MsgCode: Success or error code.

        return ensure_secure_directory()

    def _check_credentials( self ) -> MsgCode:
    
        # Check if credentials file exists and has secure permissions.
        # Returns:
            # MsgCode: Success or specific error code.

        try:
            if not self._credentials_file.exists():
                return MsgCode.MISSING_CREDENTIALS_FILE
            
            if not self._check_permissions( self._credentials_file ):
                return MsgCode.PERMISSION_CREDENTIALS_ERROR
            
            return MsgCode.SUCCESS
        
        except PermissionError:
            return MsgCode.PERMISSION_CREDENTIALS_ERROR
        except OSError:
            return MsgCode.IO_ERROR
        except Exception:
            return MsgCode.UNKNOWN_ERROR

    def _check_key( self ) -> MsgCode:

        #Check if key file exists and has secure permissions.
        # Returns:
            # MsgCode: Success or specific error code.

        try:
            if not self._key_file.exists():
                return MsgCode.MISSING_KEY_FILE
            
            if not self._check_permissions( self._key_file ):
                return MsgCode.PERMISSION_KEY_ERROR
            
            return MsgCode.SUCCESS
        
        except PermissionError:
            return MsgCode.PERMISSION_KEY_ERROR
        except OSError:
            return MsgCode.IO_ERROR
        except Exception:
            return MsgCode.UNKNOWN_ERROR

    def _check_permissions( self, file_path: Path ) -> bool:

        # Verify file has secure permissions (no group/other access).
        # Args:
            # file_path: Path to file being checked.
        # Returns:
            # bool: True if permissions are secure, False otherwise.

        try:
            if file_path.exists():
                stat = file_path.stat()
                if stat.st_mode & 0o077:  # Check for group/other permissions
                    return False
            return True
        except Exception:
            return False

    def verify_credentials( self, email: str, password: str ) -> MsgCode:

        # Verify provided credentials against stored credentials.
        # Args:
            # email: Email to verify.
            # password: Password to verify.
        # Returns:
            # MsgCode: Verification result.

        status, credentials = self.load_credentials()
        if status != MsgCode.SUCCESS:
            return status

        if not credentials:
            return MsgCode.INVALID_CREDENTIALS

        if (credentials.get( 'email' ) == email and 
            credentials.get( 'password' ) == password ):
            return MsgCode.SUCCESS

        return MsgCode.INVALID_CREDENTIALS

    def _create_key(
        self,
        password: Optional[ str ] = None
    ) -> Tuple[MsgCode, Optional[bytes]]:

        # Generate encryption key from password or create random key.
        # Args:
            # password: Optional password for key derivation.
        # Returns:
            #Tuple containing:
                # - MsgCode: Operation status.
                # - bytes: Generated encryption key (or None on failure).

        try:
            if password:
                salt = b'stable_salt_for_consistency'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000
                )
                key = base64.urlsafe_b64encode( kdf.derive(password.encode() ) )
            else:
                key = Fernet.generate_key()
            return MsgCode.SUCCESS, key
        except Exception:
            return MsgCode.UNKNOWN_KEY_ERROR, None

    def _load_key( self ) -> Optional[ bytes ]:
        
        # Load encryption key from file.

        try:
            with open( self._key_file, 'rb' ) as key_file:
                return key_file.read()
        except Exception:
            return None

    def _save_key( self, key: bytes ) -> MsgCode:

        # Save encryption key to file with secure permissions.
        # Args:
            # key: Encryption key to save.
        # Returns:
            # MsgCode: Operation status.

        try:
            with open( self._key_file, 'wb' ) as key_file:
                key_file.write( key )
            os.chmod( self._key_file, SECURE_FILE_MODE )
            return MsgCode.SUCCESS
        except Exception:
            return MsgCode.SAVING_KEY_ERROR

    def _get_fernet( self ) -> Tuple[ MsgCode, Optional[ Fernet ]]:
        
        # Get Fernet instance for encryption/decryption.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - Fernet: Initialized Fernet instance (or None).

        if self._fernet is not None:
            return MsgCode.SUCCESS, self._fernet

        key = self._load_key()
        if not key:
            return MsgCode.MISSING_KEY_FILE, None

        try:
            self._fernet = Fernet( key )
            return MsgCode.SUCCESS, self._fernet
        except Exception:
            return MsgCode.ENCRYPTION_FERNET_ERROR, None

    def create_credentials(
        self,
        username: Optional[ str ],
        email: str,
        password: str,
        additional_data: Optional[ Dict[ str, Any ] ] = None
    ) -> MsgCode:
        
        # Create and store encrypted credentials.
        # Args:
            # username: User identifier (optional).
            # email: User email address.
            # password: User password.
            # additional_data: Extra credential data (optional).
        # Returns:
            # MsgCode: Operation status.

        # Validate directory first.
        dir_status = self._check_directory()

        if dir_status != MsgCode.SUCCESS:
            return dir_status

        # Generate and save key.
        key_status, key = self._create_key()
        if key_status != MsgCode.SUCCESS or not key:
            return key_status or MsgCode.CREATE_KEY_ERROR

        save_status = self._save_key( key )
        if save_status != MsgCode.SUCCESS:
            return save_status

        # Prepare credentials data.
        credentials_data = {
            'username': username or "",
            'email': email,
            'password': password,
            'additional_data': additional_data or {}
        }

        # Encrypt and save credentials.
        fernet_status, fernet = self._get_fernet()

        if fernet_status != MsgCode.SUCCESS or not fernet:
            return fernet_status or MsgCode.FERNET_NULL

        try:
            encrypted_data = fernet.encrypt(
                json.dumps( credentials_data ).encode()
            )
            with open( self._credentials_file, 'wb' ) as cred_file:
                cred_file.write( encrypted_data )
            os.chmod( self._credentials_file, SECURE_FILE_MODE )
            return MsgCode.SUCCESS
        except Exception:
            return MsgCode.ENCRYPTION_ERROR

    def load_credentials( self ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:

        # Load and decrypt stored credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status
                # - dict: Decrypted credentials (or None)

        # Check files first
        cred_status = self._check_credentials()
        
        if cred_status != MsgCode.SUCCESS:
            return cred_status, None

        key_status = self._check_key()
        
        if key_status != MsgCode.SUCCESS:
            return key_status, None

        # Get Fernet instance
        fernet_status, fernet = self._get_fernet()
        
        if fernet_status != MsgCode.SUCCESS or not fernet:
            return fernet_status or MsgCode.FERNET_NULL, None

        # Decrypt credentials
        try:
            with open( self._credentials_file, 'rb' ) as cred_file:
                encrypted_data = cred_file.read()
                decrypted_data = fernet.decrypt( encrypted_data )
                return MsgCode.SUCCESS, json.loads( decrypted_data.decode() )
        except Exception:
            return MsgCode.DECRYPTION_ERROR, None
