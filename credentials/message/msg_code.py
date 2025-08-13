# ==============================================
# authenticator/msg/msg_code.py
# version: 0.0.2
# title: Messages Settings
# author: silvioantunes1@hotmail.com
#  ==============================================

from enum import IntEnum

# Internal message codes.
class _MsgCode( IntEnum ):
    SUCCESS = 0
    
    # Input/Validation Errors (100-119)
    INVALID_TYPE = 100
    MISSING_KEY_FILE = 101
    MISSING_CREDENTIALS_FILE = 102
    MISSING_DIR = 103

    # Encryption/Decryption Errors (120-139)
    ENCRYPTION_ERROR = 120
    ENCRYPTION_FERNET_ERROR = 121
    DECRYPTION_ERROR = 122
    DECRYPTION_FERNET_ERROR = 123

    # Permission Errors (140-149)
    PERMISSION_ERROR = 140
    PERMISSION_KEY_FILE_ERROR = 141
    PERMISSION_CREDENTIALS_FILE_ERROR = 142

    # I/O Errors (150-159)
    IO_ERROR = 150
    IO_KEY_ERROR = 151
    IO_CREDENTIALS_ERROR = 152
    IO_DIR_ERROR = 153

    # Key Management Errors (160-169)
    PROVIDED_KEY_NULL = 160
    SAVING_KEY_ERROR = 161
    CREATE_KEY_ERROR = 162
    FERNET_NULL = 163
    LOADING_KEY_ERROR = 164
    
    # Credentials Management Erros (170 - 179)
    CREDENTIALS_INVALID = 170
    CREDENTIALS_NULL = 171
    FIELD_NOT_FOUND = 172

    # Config Management Errors (180-189)
    CONFIG_ALREADY_EXISTS = 180
    CONFIG_NOT_FOUND = 181
    CONFIG_INVALID = 182

    # Unknown Errors (250-255)
    UNKNOWN_DIR_ERROR = 251
    UNKNOWN_FERNET_ERROR = 252
    UNKNOWN_CREATE_CREDENTIALS_FILE_ERROR = 253
    UNKNOWN_CREATE_KEY_FILE_ERROR = 254
    UNKNOWN_CREDENTIALS_FILE_ERROR = 253
    UNKNOWN_KEY_FILE_ERROR = 254
    UNKNOWN_ERROR = 255

# Public interface for message codes.
# Singleton class for accessing message codes.
class MsgCodeSingleton:
    
    def __getattr__( self, name ) -> int:
        try:
            return getattr( _MsgCode, name ).value
        except AttributeError:
            raise AttributeError( f"'{self.__class__.__name__}' object has no attribute '{name}'" )

# Create singleton instance.
MsgCode = MsgCodeSingleton()