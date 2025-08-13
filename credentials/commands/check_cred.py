#!/usr/bin/env python3

# ==============================================
# authenticator/commands/check_exists_cred.py
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

import sys
from pathlib import Path
from typing import List, Dict, Any

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
            print(f"\033[1;31m❌ Critical import error: {e}\033[0m")
            sys.exit(255)

# Colors and symbols for better visualization
class Colors:
    SUCCESS = "\033[1;32m"
    ERROR = "\033[1;31m"
    WARNING = "\033[1;33m"
    INFO = "\033[1;34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

class Symbols:
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    FOLDER = "📁"
    FILE = "📄"
    KEY = "🔑"

def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{title.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")

def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{Colors.BOLD}{Colors.INFO}{title}{Colors.RESET}")
    print(f"{Colors.INFO}{'-' * len(title)}{Colors.RESET}")

def print_credential_info(cred_info: Dict[str, Any], index: int = None) -> None:
    """Print detailed information about a credential configuration."""
    
    # Header for this credential
    if index is not None:
        print(f"\n{Colors.BOLD}[{index + 1}] ", end="")
    else:
        print(f"\n{Colors.BOLD}", end="")
    
    if cred_info["type"] == "default":
        print(f"Default Configuration{Colors.RESET}")
    else:
        print(f"Registered Configuration: {cred_info['config_name']}{Colors.RESET}")
    
    # Basic info
    print(f"   Type: {cred_info['type'].title()}")
    if cred_info.get("description"):
        print(f"   Description: {cred_info['description']}")
    if cred_info.get("created_date"):
        print(f"   Created: {cred_info['created_date']}")
    
    # Directory and files
    print(f"   {Symbols.FOLDER} Directory: {cred_info['directory']}")
    print(f"   {Symbols.FILE} Credentials: {cred_info['credentials_file']}")
    print(f"   {Symbols.KEY} Key File: {cred_info['key_file']}")
    
    # Status information
    status = cred_info["status"]
    print(f"\n   Status:")
    
    # Directory status
    if status.get("directory_exists", False):
        print(f"   {Symbols.SUCCESS} {Colors.SUCCESS}Directory exists{Colors.RESET}")
    else:
        print(f"   {Symbols.ERROR} {Colors.ERROR}Directory missing{Colors.RESET}")
        if status.get("directory_message"):
            print(f"      → {status['directory_message']}")
    
    # Credentials file status
    if status.get("credentials_exists", False):
        print(f"   {Symbols.SUCCESS} {Colors.SUCCESS}Credentials file exists{Colors.RESET}")
    else:
        print(f"   {Symbols.ERROR} {Colors.ERROR}Credentials file missing{Colors.RESET}")
        if status.get("credentials_message"):
            print(f"      → {status['credentials_message']}")
    
    # Key file status
    if status.get("key_exists", False):
        print(f"   {Symbols.SUCCESS} {Colors.SUCCESS}Key file exists{Colors.RESET}")
    else:
        print(f"   {Symbols.ERROR} {Colors.ERROR}Key file missing{Colors.RESET}")
        if status.get("key_message"):
            print(f"      → {status['key_message']}")
    
    # Overall status
    if cred_info.get("is_complete", False):
        print(f"\n   {Symbols.SUCCESS} {Colors.SUCCESS}{Colors.BOLD}COMPLETE - Ready to use{Colors.RESET}")
    else:
        print(f"\n   {Symbols.WARNING} {Colors.WARNING}{Colors.BOLD}INCOMPLETE - Missing components{Colors.RESET}")
    
    # Error information if present
    if cred_info.get("error"):
        print(f"\n   {Symbols.ERROR} {Colors.ERROR}Error: {cred_info['error']}{Colors.RESET}")

def check_default_credentials() -> Dict[str, Any]:
    """Check credentials in default directory."""
    try:
        creds = Credentials()
        dir_status, creds_status, key_status = creds.checker()
        
        return {
            "type": "default",
            "config_name": None,
            "directory": str(creds.credentials_directory),
            "credentials_file": str(creds.credentials_file_path),
            "key_file": str(creds.key_file_path),
            "status": {
                "directory_exists": dir_status == MsgCode.SUCCESS,
                "credentials_exists": creds_status == MsgCode.SUCCESS,
                "key_exists": key_status == MsgCode.SUCCESS,
                "directory_message": MessageHandler.get(dir_status) if dir_status != MsgCode.SUCCESS else None,
                "credentials_message": MessageHandler.get(creds_status) if creds_status != MsgCode.SUCCESS else None,
                "key_message": MessageHandler.get(key_status) if key_status != MsgCode.SUCCESS else None
            },
            "is_complete": all([
                dir_status == MsgCode.SUCCESS,
                creds_status == MsgCode.SUCCESS,
                key_status == MsgCode.SUCCESS
            ])
        }
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
                "directory_message": str(e),
                "credentials_message": str(e),
                "key_message": str(e)
            },
            "is_complete": False,
            "error": str(e)
        }

def check_registered_credentials() -> List[Dict[str, Any]]:
    """Check all registered credential configurations."""
    registered_configs = []
    
    try:
        creds = Credentials()
        saved_configs = creds.list_saved_configs()
        
        for config_info in saved_configs:
            try:
                # Check status using the existing method from your ConfigManager
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
                        "status_message": MessageHandler.get(status_code) if status_code != MsgCode.SUCCESS else None
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
                base_path = Path(config_info.base_directory) if hasattr(config_info, 'base_directory') else Path("unknown")
                credentials_dir = base_path / (config_info.folder_name if hasattr(config_info, 'folder_name') else "unknown")
                
                error_config = {
                    "type": "registered",
                    "config_name": config_info.name,
                    "description": config_info.description if hasattr(config_info, 'description') else None,
                    "directory": str(credentials_dir),
                    "credentials_file": str(credentials_dir / (config_info.credentials_filename if hasattr(config_info, 'credentials_filename') else "unknown")),
                    "key_file": str(credentials_dir / (config_info.key_filename if hasattr(config_info, 'key_filename') else "unknown")),
                    "created_date": config_info.created_at if hasattr(config_info, 'created_at') else None,
                    "last_used": config_info.last_used if hasattr(config_info, 'last_used') else None,
                    "status": {
                        "directory_exists": False,
                        "credentials_exists": False,
                        "key_exists": False,
                        "status_message": str(e)
                    },
                    "is_complete": False,
                    "error": str(e)
                }
                registered_configs.append(error_config)
                
    except Exception as e:
        pass
    
    return registered_configs

def main() -> None:
    """Main entry point for visual credential existence check."""
    try:
        print_header("CREDENTIALS EXISTENCE VERIFICATION")
        
        # Check default credentials
        print_section(f"{Symbols.INFO} Checking Default Configuration")
        default_creds = check_default_credentials()
        print_credential_info(default_creds)
        
        # Check registered credentials
        print_section(f"{Symbols.INFO} Checking Registered Configurations")
        registered_creds = check_registered_credentials()
        
        if not registered_creds:
            print(f"\n   {Symbols.INFO} {Colors.INFO}No registered configurations found{Colors.RESET}")
        else:
            for i, cred_info in enumerate(registered_creds):
                print_credential_info(cred_info, i)
        
        # Summary
        print_section(f"{Symbols.INFO} Summary")
        
        all_credentials = [default_creds] + registered_creds
        complete_credentials = [c for c in all_credentials if c.get("is_complete", False)]
        
        print(f"   Total configurations: {len(all_credentials)}")
        print(f"   Complete configurations: {len(complete_credentials)}")
        print(f"   Incomplete configurations: {len(all_credentials) - len(complete_credentials)}")
        
        if complete_credentials:
            print(f"\n   {Symbols.SUCCESS} {Colors.SUCCESS}{Colors.BOLD}CREDENTIALS AVAILABLE!{Colors.RESET}")
            print(f"   {Colors.SUCCESS}You have {len(complete_credentials)} working credential configuration(s){Colors.RESET}")
            
            if len(complete_credentials) > 1:
                print(f"\n   {Colors.INFO}Available configurations:{Colors.RESET}")
                for cred in complete_credentials:
                    if cred["type"] == "default":
                        print(f"   • Default configuration")
                    else:
                        print(f"   • {cred['config_name']}")
        else:
            print(f"\n   {Symbols.WARNING} {Colors.WARNING}{Colors.BOLD}NO COMPLETE CREDENTIALS FOUND{Colors.RESET}")
            print(f"   {Colors.WARNING}Please create or fix credential configurations{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        
        # Exit with appropriate code
        sys.exit(0 if complete_credentials else 1)
        
    except Exception as e:
        print(f"\n{Symbols.ERROR} {Colors.ERROR}{Colors.BOLD}UNEXPECTED ERROR{Colors.RESET}")
        print(f"{Colors.ERROR}Error: {e}{Colors.RESET}")
        sys.exit(255)

if __name__ == "__main__":
    main()