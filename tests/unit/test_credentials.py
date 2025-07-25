import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
from credentials.credentials import Credentials
from credentials.message.msg_code import MsgCode

class TestCredentials(unittest.TestCase):
    
    @patch("os.chmod")
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "exists", return_value=False)
    @patch.object(Path, "mkdir")
    def test_create_credentials_success(self, mock_mkdir, mock_exists, mock_file, mock_chmod):
        # Test successful credential creation.
        creds = Credentials()
        result = creds.create_credentials(
            username = None,
            email = "test@example.com",
            password = "securepassword123",
            additional_data= None
        )
        self.assertEqual(result, MsgCode.SUCCESS)
    
    def test_verify_valid_credentials(self):
        # Test valid credential verification.
        creds = Credentials()
        creds.create_credentials(
            email = "test@example.com",
            password = "securepassword123"
        )
        result = creds.verify_credentials(
            email="test@example.com",
            password="securepassword123"
        )
        self.assertEqual(result, MsgCode.SUCCESS)

if __name__ == "__main__":
    unittest.main()