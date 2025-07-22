# ==============================================
# authenticator/msg/msg_code.py
# version: 0.0.2
# title: Messages Settings
# author: silvioantunes1@hotmail.com
#  ==============================================

from enum import IntEnum

# Internal message codes.
class MsgCode( IntEnum ):  # Fixed: was __MsgCode
    SUCCESS = 0
    # Input/Validation Errors (100-119)
    INVALID_TYPE = 100
    MISSING_KEY_FILE = 101
    MISSING_CREDENTIALS_FILE = 102
    INVALID_CREDENTIALS = 103
    DIRECTORY_ERROR = 104

    # Encryption/Decryption Errors (120-139)
    ENCRYPTION_ERROR = 120
    ENCRYPTION_FERNET_ERROR = 121
    DECRYPTION_ERROR = 122
    DECRYPTION_FERNET_ERROR = 123
    
    # Permission Errors (140-149)
    PERMISSION_ERROR = 140
    PERMISSION_KEY_ERROR = 141
    PERMISSION_CREDENTIALS_ERROR = 142
    
    # I/O Errors (150-159)
    IO_ERROR = 150
    
    # Key Management Errors (160-179)
    PROVIDED_KEY_NULL = 160
    SAVING_KEY_ERROR = 161
    CREATE_KEY_ERROR = 162
    FERNET_NULL = 163
    LOADING_KEY_ERROR = 164
    
    # Unknown Errors (250-255)
    UNKNOWN_FERNET_ERROR = 253
    UNKNOWN_KEY_ERROR = 254
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