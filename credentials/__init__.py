# ==============================================
# authenticator/__init__.py
# version: 0.1.0
# author: silvioantunes1@hotmail.com
# ==============================================

"""
Authenticator - A secure credential management system with encryption support.

This package provides secure credential storage and management with encryption
capabilities using the cryptography library.
"""

__version__ = '0.0.1'
__author__ = 'Silvio Antunes'
__email__ = 'silvioantunes1@hotmail.com'

from .Credentials import Credentials
from .msg.Message import MsgCode, Message

__all__ = ['Credentials', 'MsgCode', 'Message']