# ==============================================
# authenticator/Credentials.py
# version: 0.1.0
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
from typing import Any, Dict, Optional, Tuple

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig
from credentials.core.credentials_checker import CredentialsChecker
from credentials.crypto.crypto_manager import CryptoManager
from credentials.core.credentials_reader import CredentialsReader

class Credentials:
    # Main credentials manager with modular architecture.

    def __init__(
        self,
        base_directory: Optional[ Path ] = None,
        folder_name: Optional[ str ] = None,
        credentials_filename: Optional[ str ] = None,
        key_filename: Optional[ str ] = None
    ) -> None:
        # Initialize credentials manager with custom or default paths.
        # Args:
            # base_directory: Base directory for credentials folder (default: home).
            # folder_name: Name of credentials folder (default: .credentials).
            # credentials_filename: Name of credentials file (default: credentials.enc).
            # key_filename: Name of key file (default: key.key).

        # Initialize configuration
        self._config = CredentialsConfig(
            base_directory = base_directory,
            folder_name = folder_name,
            credentials_filename = credentials_filename,
            key_filename = key_filename
        )
        
        # Initialize components
        self._checker = CredentialsChecker( self._config )
        self._crypto_manager = CryptoManager( self._config )
        self._reader = CredentialsReader( self._config )

    def __del__( self ) -> None:
        # Clean up resources on deletion.

        self._config = None
        self._checker = None
        self._crypto_manager = None
        self._reader = None

    def checker( self ) -> Tuple[ MsgCode, MsgCode, MsgCode ]:
        
        msg00 = self._checker.check_directory()
        
        if msg00 != MsgCode.SUCCESS:
            return msg00, None, None
        
        msg01 = self._checker.check_credentials_file()
        msg02 = self._checker.check_key_file()
        
        return msg00, msg01, msg02

    def create_credentials(
        self,
        username: Optional[ str ] = None,
        email: Optional[ str ] = None,
        password: Optional[ str ] = None,
        additional_data: Optional[ Dict[ str, Any ] ] = None,
        key_password: Optional[ str ] = None
    ) -> MsgCode:
        # Create and store encrypted credentials.
        # Args:
            # username: User identifier (optional).
            # email: User email address.
            # password: User password.
            # additional_data: Extra credential data (optional).
            # key_password: Password for key derivation (optional).
        # Returns:
            # MsgCode: Operation status.

        # Generate and save key
        key_status, key = self._crypto_manager.create_key( key_password )
        if key_status != MsgCode.SUCCESS or not key:
            return key_status or MsgCode.CREATE_KEY_ERROR
        
        save_key_status = self._crypto_manager.save_key( key )
        if save_key_status != MsgCode.SUCCESS:
            return save_key_status
        
        # Prepare credentials data
        credentials_data = {
            'username': username,
            'email': email,
            'password': password,
            'additional_data': additional_data or {}
        }
        
        # Encrypt data
        encrypt_status, encrypted_data = self._crypto_manager.encrypt_data( credentials_data )
        if encrypt_status != MsgCode.SUCCESS or not encrypted_data:
            return encrypt_status or MsgCode.ENCRYPTION_ERROR
        
        # Save encrypted data
        return self._crypto_manager.save_encrypted_data( encrypted_data )
    
    def load_credentials( self ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:
        # Load and decrypt stored credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - dict: Decrypted credentials (or None on failure).

        return self._reader.read_credentials()

    def verify_credentials( self, email: str, password: str ) -> MsgCode:
        # Verify provided credentials against stored credentials.
        # Args:
            # email: Email to verify.
            # password: Password to verify.
        # Returns:
            # MsgCode: Verification result.

        return self._reader.verify_login( email, password )

    def get_username( self ) -> Tuple[ MsgCode, Optional[ str ] ]:
        # Get username from stored credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - str: Username (or None on failure).

        return self._reader.get_username()
    
    def get_email( self ) -> Tuple[ MsgCode, Optional[ str ] ]:
        # Get email from stored credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - str: Email (or None on failure).

        return self._reader.get_email()
    
    def get_password( self ) -> Tuple[ MsgCode, Optional[ str ] ]:
        # Get password from stored credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - str: Password (or None on failure).

        return self._reader.get_password()
    
    def get_additional_data( self ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:
        # Get additional data from stored credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - dict: Additional data (or None on failure).

        return self._reader.get_additional_data()
    
    def get_credential_field( self, field_name: str ) -> Tuple[ MsgCode, Optional[ Any ] ]:
        # Get specific field from credentials.
        # Args:
            # field_name: Name of the field to retrieve.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - Any: Field value (or None on failure).

        return self._reader.get_credential_field( field_name )
    
    # Configuration access methods
    @property
    def credentials_file_path( self ) -> Path:
        # Get credentials file path.
        return self._config.credentials_file
    
    @property
    def key_file_path( self ) -> Path:
        # Get key file path.
        return self._config.key_file
    
    @property
    def credentials_directory( self ) -> Path:
        # Get credentials directory path.
        return self._config.credentials_dir