# ==============================================
# authenticator/crypto/decrypto_maneger.py
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

import json
from typing import Any, Dict, Optional, Tuple

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig
from credentials.crypto.crypto_manager import CryptoManager

class DecryptoManager:
    # Decryption manager for credentials.

    def __init__( self, config: CredentialsConfig ) -> None:
        # Initialize decryption manager with configuration.
        # Args:
            # config: Configuration instance with file paths.

        self._config = config
        self._crypto_manager = CryptoManager( config )

    def load_encrypted_data( self ) -> Tuple[ MsgCode, Optional[ bytes ] ]:
        # Load encrypted data from credentials file.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - bytes: Encrypted data (or None on failure).

        try:
            with open( self._config.credentials_file, 'rb' ) as cred_file:
                encrypted_data = cred_file.read()
                return MsgCode.SUCCESS, encrypted_data
        except FileNotFoundError:
            return MsgCode.MISSING_CREDENTIALS_FILE, None
        except PermissionError:
            return MsgCode.PERMISSION_CREDENTIALS_ERROR, None
        except OSError:
            return MsgCode.IO_CREDENTIAIS_ERROR, None
        except Exception:
            return MsgCode.UNKNOWN_CREDENTIALS_FILE_ERROR, None

    def decrypt_data( self, encrypted_data: bytes ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:
        # Decrypt credentials data.
        # Args:
            # encrypted_data: Encrypted credentials data.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - dict: Decrypted credentials data (or None on failure).

        fernet_status, fernet = self._crypto_manager._get_fernet()
        if fernet_status != MsgCode.SUCCESS or not fernet:
            return fernet_status or MsgCode.FERNET_NULL, None

        try:
            decrypted_data = fernet.decrypt( encrypted_data )
            credentials_dict = json.loads( decrypted_data.decode() )
            return MsgCode.SUCCESS, credentials_dict
        except Exception:
            return MsgCode.DECRYPTION_ERROR, None

    def load_and_decrypt_credentials( self ) -> Tuple[ MsgCode, Optional[ Dict[ str, Any ] ] ]:
        # Load and decrypt stored credentials in one operation.
        # Returns:
            # Tuple containing:
                # - MsgCode: Operation status.
                # - dict: Decrypted credentials (or None on failure).
        # Load encrypted data

        load_status, encrypted_data = self.load_encrypted_data()
        if load_status != MsgCode.SUCCESS or not encrypted_data:
            return load_status, None

        # Decrypt data
        decrypt_status, credentials = self.decrypt_data( encrypted_data )
        return decrypt_status, credentials