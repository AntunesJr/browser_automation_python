#!/usr/bin/env python3

# ==============================================
# authenticator/commands/check_cred.py
# version: 0.0.3
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

# Robust import strategy
try:
    from credentials.credentials import Credentials
    from credentials.message.msg_code import MsgCode
    from credentials.message.msg_handler import MessageHandler
except ImportError:
    try:
        # Try relative import
        from ..credentials import Credentials
        from ..message.msg_code import MsgCode
        from ..message.msg_handler import MessageHandler
    except ImportError:
        try:
            # Add root directory to Python path
            current_dir = Path(__file__).resolve().parent
            root_dir = current_dir.parent.parent
            sys.path.insert(0, str(root_dir))
            
            from credentials.message.msg_code import MsgCode
            from credentials.message.msg_handler import MessageHandler
        except ImportError as e:
            print(f"Critical import error: {e}")
            sys.exit(255)

# Titles for each verification
CHECK_TITLES = {
    "directory": "Directory Verification",
    "credentials": "Credentials Verification",
    "key": "Encryption Key Verification"
}

# Custom success messages
SUCCESS_MESSAGES = {
    "directory": "✅ Directory configured correctly",
    "credentials": "✅ Valid credentials accessible",
    "key": "✅ Valid encryption key"
}

def main():
    __creds = Credentials()
    __result00, __result01, __result02 = __creds.checker()
    # Perform verifications
    results = {
        "directory": __result00,
        "credentials": __result01,
        "key": __result02
    }
    
    # Display formatted results
    print("Security Verification Results:")
    print("=" * 50)
    
    for check_name, code in results.items():
        title = CHECK_TITLES[ check_name ]
        
        if code == 0:
            status = "\033[1;32mSUCCESS\033[0m"
            message = SUCCESS_MESSAGES[ check_name ]
        else:
            status = "\033[1;31mERROR\033[0m"
            message = MessageHandler(code)
        
        print(f"{title}:")
        print(f"  Status: {status}")
        print(f"  Code: {code}")
        print(f"  Message: {message}")
        print("-" * 50)

    # Check if all verifications succeeded
    all_success = all(code == 0 for code in results.values())
    print("\nOverall Status:")
    if all_success:
        print( "\033[1;32mALL VERIFICATIONS SUCCEEDED!\033[0m" )
    else:
        print( "\033[1;31mVERIFICATION ISSUES DETECTED. PLEASE CORRECT THE ERRORS ABOVE.\033[0m" )

    # Exit code: 0 if all OK, 1 if any error
    sys.exit( 0 if all_success else 1 )

if __name__ == "__main__":
    main()