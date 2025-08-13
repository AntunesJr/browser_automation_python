#!/usr/bin/env python3

# ==============================================
# authenticator/commands/check_cred_json.py
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
import sys
from pathlib import Path
from typing import Dict, Any, List

# Robust import strategy
try:
    from credentials.credentials import Credentials
    from credentials.message.msg_code import MsgCode
    from credentials.message.msg_handler import MessageHandler
    from credentials.config.config import CredentialsConfig
except ImportError:
    try:
        # Try relative import
        from ..credentials import Credentials
        from ..message.msg_code import MsgCode
        from ..message.msg_handler import MessageHandler
        from ..config.config import CredentialsConfig
    except ImportError:
        try:
            # Add root directory to Python path
            current_dir = Path(__file__).resolve().parent
            root_dir = current_dir.parent.parent
            sys.path.insert(0, str(root_dir))
            
            from credentials.credentials import Credentials
            from credentials.message.msg_code import MsgCode
            from credentials.message.msg_handler import MessageHandler
            from credentials.config.config import CredentialsConfig
        except ImportError as e:
            error_output = {
                "exist": False,
                "error": f"Critical import error: {e}",
                "credentials": []
            }
            print(json.dumps(error_output, indent=2))
            sys.exit(255)

def check_default_credentials() -> Dict[str, Any]:
    """
    Check credentials in default directory.
    
    Returns:
        Dict containing default credentials info
    """
    try:
        creds = Credentials()
        dir_status, creds_status, key_status = creds.checker()
        
        default_info = {
            "type": "default",
            "config_name": None,
            "directory": str(creds.credentials_directory),
            "credentials_file": str(creds.credentials_file_path),
            "key_file": str(creds.key_file_path),
            "status": {
                "directory_exists": dir_status == MsgCode.SUCCESS,
                "credentials_exists": creds_status == MsgCode.SUCCESS,
                "key_exists": key_status == MsgCode.SUCCESS,
                "directory_code": dir_status,
                "credentials_code": creds_status,
                "key_code": key_status,
                "directory_message": MessageHandler.get(dir_status),
                "credentials_message": MessageHandler.get(creds_status),
                "key_message": MessageHandler.get(key_status)
            },
            "is_complete": all([
                dir_status == MsgCode.SUCCESS,
                creds_status == MsgCode.SUCCESS,
                key_status == MsgCode.SUCCESS
            ])
        }
        
        return default_info
        
    except Exception as e:
        return {
            "type": "default",
            "config_name": None,
            "directory": "unknown",
            "credentials_file": "unknown",
            "key_file": "unknown",
            "status": {
                "directory_exists": False,
                "credentials_exists": False,
                "key_exists": False,
                "directory_code": MsgCode.UNKNOWN_ERROR,
                "credentials_code": MsgCode.UNKNOWN_ERROR,
                "key_code": MsgCode.UNKNOWN_ERROR,
                "directory_message": str(e),
                "credentials_message": str(e),
                "key_message": str(e)
            },
            "is_complete": False,
            "error": str(e)
        }

def check_registered_credentials() -> List[Dict[str, Any]]:
    """
    Check all registered credential configurations.
    
    Returns:
        List of registered credential configurations info
    """
    registered_configs = []
    
    try:
        creds = Credentials()
        saved_configs = creds.list_saved_configs()
        
        for config_info in saved_configs:
            try:
                # Check status of this specific config using the existing method
                status_code, exists, file_status = creds._config_manager.check_config_exists(config_info.name)
                
                base_path = Path(config_info.base_directory)
                credentials_dir = base_path / config_info.folder_name
                
                config_data = {
                    "type": "registered",
                    "config_name": config_info.name,
                    "description": config_info.description,
                    "directory": str(credentials_dir),
                    "credentials_file": str(credentials_dir / config_info.credentials_filename),
                    "key_file": str(credentials_dir / config_info.key_filename),
                    "created_date": config_info.created_at,
                    "last_used": config_info.last_used,
                    "status": {
                        "directory_exists": file_status.get("directory_exists", False) if file_status else False,
                        "credentials_exists": file_status.get("credentials_exists", False) if file_status else False,
                        "key_exists": file_status.get("key_exists", False) if file_status else False,
                        "status_code": status_code,
                        "status_message": MessageHandler.get(status_code)
                    },
                    "is_complete": (
                        file_status and
                        file_status.get("directory_exists", False) and
                        file_status.get("credentials_exists", False) and
                        file_status.get("key_exists", False)
                    ) if file_status else False
                }
                
                registered_configs.append(config_data)
                
            except Exception as e:
                # Add error info for this specific config
                error_config = {
                    "type": "registered",
                    "config_name": config_info.name,
                    "description": config_info.description,
                    "directory": "unknown",
                    "credentials_file": "unknown",
                    "key_file": "unknown",
                    "created_date": config_info.created_at if hasattr(config_info, 'created_at') else None,
                    "last_used": config_info.last_used if hasattr(config_info, 'last_used') else None,
                    "status": {
                        "directory_exists": False,
                        "credentials_exists": False,
                        "key_exists": False,
                        "status_code": MsgCode.UNKNOWN_ERROR,
                        "status_message": str(e)
                    },
                    "is_complete": False,
                    "error": str(e)
                }
                registered_configs.append(error_config)
                
    except Exception as e:
        # Return empty list with error info
        pass
    
    return registered_configs

def main() -> None:
    """Main entry point for JSON credential existence check."""
    try:
        # Check default credentials
        default_creds = check_default_credentials()
        
        # Check registered credentials
        registered_creds = check_registered_credentials()
        
        # Combine all credentials
        all_credentials = [default_creds] + registered_creds
        
        # Check if any credentials exist and are complete
        any_exist = any(cred.get("is_complete", False) for cred in all_credentials)
        complete_credentials = [cred for cred in all_credentials if cred.get("is_complete", False)]
        incomplete_credentials = [cred for cred in all_credentials if not cred.get("is_complete", False)]
        
        # Build output
        output = {
            "exist": any_exist,
            "total_configs": len(all_credentials),
            "complete_configs": len(complete_credentials),
            "incomplete_configs": len(incomplete_credentials),
            "summary": {
                "has_default": default_creds.get("is_complete", False),
                "registered_count": len(registered_creds),
                "complete_registered": len([c for c in registered_creds if c.get("is_complete", False)])
            },
            "credentials": all_credentials
        }
        
        # Output JSON
        print(json.dumps(output, indent=2, ensure_ascii=False))
        
        # Exit with appropriate code
        sys.exit(0 if any_exist else 1)
        
    except Exception as e:
        error_output = {
            "exist": False,
            "error": f"Unexpected error: {e}",
            "total_configs": 0,
            "complete_configs": 0,
            "incomplete_configs": 0,
            "summary": {
                "has_default": False,
                "registered_count": 0,
                "complete_registered": 0
            },
            "credentials": []
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(255)

if __name__ == "__main__":
    main()