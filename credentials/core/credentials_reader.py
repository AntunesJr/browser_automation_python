# ==============================================
# authenticator/core/credentials_reader.py
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

from typing import Any, Dict, Optional, Tuple

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig
from credentials.core.credentials_checker import CredentialsChecker
from credentials.crypto.decrypto_manager import DecryptoManager

class CredentialsReader:
    # Reader for encrypted credentials with security checks.
    
    def __init__( self, config: CredentialsConfig ) -> None:
        # Initialize credentials reader with configuration.
        # Args:
            # config: Configuration instance with file paths.

        self._config = config
        self._decrypto_manager = DecryptoManager( config )
    
    def _get_credential_field( self, field_name: str ) -> Tuple[ MsgCode, Optional[ Any ] ]:
        # Get specific field from credentials.
        # Args:
            # field_name: Name of the field to retrieve.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - Any: Field value (or None on failure).

        read_status, credentials = self._read_credentials()
        if read_status != MsgCode.SUCCESS or not credentials:
            return read_status, None
        
        if field_name not in credentials:
            return MsgCode.FIELD_NOT_FOUND, None
        
        return MsgCode.SUCCESS, credentials[ field_name ]
    
    def get_username( self ) -> Tuple[ MsgCode, Optional[ str ] ]:
        # Get username from credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - str: Username (or None on failure).

        return self._get_credential_field( 'username' )
    
    def get_email( self ) -> Tuple[ MsgCode, Optional[ str ] ]:
        # Get email from credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - str: Email (or None on failure).

        return self._get_credential_field( 'email' )
    
    def get_password( self ) -> Tuple[ MsgCode, Optional [ str ] ]:
        # Get password from credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - str: Password (or None on failure).

        return self._get_credential_field( 'password' )
    
    def get_additional_data( self ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:
        # Get additional data from credentials.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - dict: Additional data (or None on failure).

        return self._get_credential_field( 'additional_data' )

    def _read_credentials( self ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:
        # Read and decrypt stored credentials with security checks.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - dict: Decrypted credentials (or None on failure).

        # Load and decrypt credentials
        return self._decrypto_manager.load_and_decrypt_credentials()

    def verify_login( self, email: str, password: str ) -> MsgCode:
        # Verify login credentials against stored credentials.
        # Args:
            # email: Email to verify.
            # password: Password to verify.
        # Returns:
            # MsgCode: Verification result.

        read_status, credentials = self._read_credentials()
        if read_status != MsgCode.SUCCESS:
            return read_status
        
        return self._checker.verify_credentials( credentials, email, password )