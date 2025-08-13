# ==============================================
# authenticator/__init__.py
# version: 0.0.1
# author: silvioantunes1@hotmail.com
# ==============================================

# Authenticator - A secure credential management system with encryption support.
# This package provides secure credential storage and management with encryption capabilities using the cryptography library.

__version__ = '0.0.1'
__author__ = 'Silvio Antunes'
__email__ = 'silvioantunes1@hotmail.com'

from .credentials import Credentials
from .message.msg_code import MsgCode
from .message.msg_handler import MessageHandler
from .crypto.crypto_manager import CryptoManager
from .crypto.decrypto_manager import DecryptoManager
from .core.credentials_checker import CredentialsChecker
from .core.credentials_reader import CredentialsReader

__all__ = [ 'Credentials', 'MsgCode', 'MessageHandler', 'CryptoManager', 'DecryptoManager', 'CredentialsChecker', 'CredentialsReader' ]