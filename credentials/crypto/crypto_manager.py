# ==============================================
# authenticator/crypto/crypto_manager.py
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

import os
import json
import base64
from typing import Any, Dict, Optional, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig, SECURE_FILE_MODE

class CryptoManager:
    # Encryption and key management for credentials.
    
    def __init__(self, config: CredentialsConfig) -> None:
        # Initialize crypto manager with configuration.
        # Args:
            # config: Configuration instance with file paths.

        self._config = config
        self._fernet: Optional[ Fernet ] = None
    
    def __del__(self) -> None:
        # Clean up resources on deletion.
        self._fernet = None
    
    def create_key( self, password: Optional[ str ] = None ) -> Tuple[ MsgCode, Optional[ bytes ] ]:
        # Generate encryption key from password or create random key.
        # Args:
            # password: Optional password for key derivation.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - bytes: Generated encryption key (or None on failure).

        try:
            if password:
                # Use stable salt for consistency
                salt = b'stable_salt_for_consistency'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000
                )
                key = base64.urlsafe_b64encode( kdf.derive( password.encode() ) )
            else:
                key = Fernet.generate_key()
            
            return MsgCode.SUCCESS, key
        except Exception:
            return MsgCode.UNKNOWN_CREATE_KEY_FILE_ERROR, None
    
    def save_key( self, key: bytes ) -> MsgCode:
        # Save encryption key to file with secure permissions.
        # Args:
            # key: Encryption key to save.
        # Returns:
            # MsgCode: Operation status.

        try:
            with open( self._config.key_file, 'wb' ) as key_file:
                key_file.write( key )
            os.chmod( self._config.key_file, SECURE_FILE_MODE )
            return MsgCode.SUCCESS
        except PermissionError:
            return MsgCode.PERMISSION_KEY_FILE_ERROR
        except OSError:
            return MsgCode.IO_KEY_ERROR
        except Exception:
            return MsgCode.SAVING_KEY_ERROR
    
    def load_key( self ) -> Tuple[ MsgCode, Optional[ bytes ] ]:
        # Load encryption key from file.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - bytes: Loaded key (or None on failure).

        try:
            with open( self._config.key_file, 'rb' ) as key_file:
                key = key_file.read()
                return MsgCode.SUCCESS, key
        except FileNotFoundError:
            return MsgCode.MISSING_KEY_FILE, None
        except PermissionError:
            return MsgCode.PERMISSION_KEY_FILE_ERROR, None
        except OSError:
            return MsgCode.IO_KEY_ERROR, None
        except Exception:
            return MsgCode.LOADING_KEY_ERROR, None
    
    def _get_fernet( self ) -> Tuple[ MsgCode, Optional[ Fernet ] ]:
        # Get Fernet instance for encryption/decryption.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - Fernet: Initialized Fernet instance (or None).

        if self._fernet is not None:
            return MsgCode.SUCCESS, self._fernet
        
        key_status, key = self.load_key()
        if key_status != MsgCode.SUCCESS or not key:
            return key_status, None
        
        try:
            self._fernet = Fernet( key )
            return MsgCode.SUCCESS, self._fernet
        except Exception:
            return MsgCode.ENCRYPTION_FERNET_ERROR, None
    
    def encrypt_data( self, data: Dict[ str, Any ] ) -> Tuple[ MsgCode, Optional[ bytes ] ]:
        # Encrypt credentials data.
        # Args:
            # data: Dictionary containing credentials to encrypt.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - bytes: Encrypted data (or None on failure).

        fernet_status, fernet = self._get_fernet()
        if fernet_status != MsgCode.SUCCESS or not fernet:
            return fernet_status or MsgCode.FERNET_NULL, None
        
        try:
            json_data = json.dumps( data ).encode()
            encrypted_data = fernet.encrypt( json_data )
            return MsgCode.SUCCESS, encrypted_data
        except Exception:
            return MsgCode.ENCRYPTION_ERROR, None
    
    def save_encrypted_data( self, encrypted_data: bytes ) -> MsgCode:
        # Save encrypted data to credentials file.
        # Args:
            # encrypted_data: Encrypted credentials data.
        # Returns:
            # MsgCode: Operation status.

        try:
            with open( self._config.credentials_file, 'wb' ) as cred_file:
                cred_file.write( encrypted_data )
            os.chmod( self._config.credentials_file, SECURE_FILE_MODE )
            return MsgCode.SUCCESS
        except PermissionError:
            return MsgCode.PERMISSION_CREDENTIALS_ERROR
        except OSError:
            return MsgCode.IO_CREDENTIALS_ERROR
        except Exception:
            return MsgCode.UNKNOWN_CREATE_CREDENTIALS_FILE_ERROR