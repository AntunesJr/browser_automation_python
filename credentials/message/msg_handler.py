# ==============================================
# authenticator/msg/msg_handler.py
# version: 0.0.3
# title: Messages Settings
# author: silvioantunes1@hotmail.com
#  ==============================================

from typing import Dict, Union
from .msg_code import MsgCode

class MessageHandler:
    # Message handler for converting codes to human-readable messages
    # Message handler for converting error codes to human-readable messages.

    _STR_MESSAGES: Dict[ int, str ] = {
        # Success
        0: "Operation completed successfully.",
        
        # Input/Validation Errors (100-119)
        100: "Invalid input type provided.",
        101: "Key file is missing.",
        102: "Credentials file is missing.",
        103: "Invalid credentials provided.",
        
        # Encryption/Decryption Errors (120-139)
        120: "Error occurred during encryption.",
        121: "Error occurred during Fernet encryption.",
        122: "Error occurred during decryption.",
        123: "Error occurred during Fernet decryption.",
        
        # Permission Errors (140-149)
        140: "Permission denied accessing files.",
        141: "Permission denied accessing key file.",
        142: "Permission denied accessing credentials file.",
        
        # I/O Errors (150-159)
        150: "I/O error occurred while accessing files.",
        
        # Key Management Errors (160-179)
        160: "The provided key is null or invalid.",
        161: "Error occurred while saving the encryption key.",
        162: "Error occurred while creating the encryption key.",
        163: "Fernet encryption object is null or invalid.",
        164: "Error occurred while loading the encryption key.",
        
        # Unknown Errors (250-255)
        253: "Unknown error occurred during Fernet operations.",
        254: "Unknown error occurred during key management.",
        255: "Unknown error occurred in the system."
    }

    def __init__(self, code: Union[int, 'MsgCode']) -> None:
        # Initialize message with code.
        # code: Message code (int or MsgCode enum).
    
        if isinstance(code, MsgCode):
            self.code = code.value
        else:
            self.code = int( code )
    
    def __str__( self ) -> str:
        # Return human-readable message.

        return self._STR_MESSAGES.get(
            self.code, 
            f"Unrecognized error code: {self.code}"
        )
    
    def __repr__( self ) -> str:
        # Return string representation for debugging.

        return f"Message(code={self.code}, message='{str(self)}')"

    @classmethod
    def get( cls, code: Union[ int, 'MsgCode' ] ) -> str:
        # Get message string for code.
        # code: Message code (int or MsgCode enum).
        # Returns: Human-readable message string.

        if isinstance( code, MsgCode ):
            code = code.value
        return cls._STR_MESSAGES.get(
            code, 
            f"Unrecognized error code: {code}"
        )
    
    @classmethod
    def add_message( cls, code: int, message: str ) -> None:
        # Add or update a message for a specific code.
        # code: Message code
        # message: Human-readable message

        cls._STR_MESSAGES[ code ] = message
    
    @classmethod
    def get_all_messages( cls ) -> Dict[ int, str ]:
        # Get all available messages.
        # Returns: Dictionary of all message codes and their messages.

        return cls._STR_MESSAGES.copy()
    
    @property
    def is_success( self ) -> bool:
       # Check if the message represents success.

        return self.code == 0
    
    @property
    def is_error( self ) -> bool:
        # Check if the message represents an error. 
        
        return self.code != 0