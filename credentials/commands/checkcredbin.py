#!/usr/bin/env python3

# ==============================================
# authenticator/commands/checkcred.py
# version: 0.0.4
# author: silvioantunes1@hotmail.com
#  ==============================================

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
import struct
from pathlib import Path

# Tripe import strategy.
try:
    # Try to import as part of the installed package.
    from authenticator.Credentials import Credentials
    from authenticator.msg.Message import MsgCode
except ImportError:
    try:
        # Attempt relative import.
        from ..Credentials import Credentials
        from ..msg.Message import MsgCode
    except ImportError:
        try:
            # Adds the root directory to the path.
            current_dir = Path(__file__).resolve().parent
            root_dir = current_dir.parent.parent
            sys.path.insert(0, str(root_dir))
            
            from authenticator.Credentials import Credentials
            from authenticator.msg.Message import MsgCode
        except ImportError as e:
            print(f"Critical import error: {e}")
            sys.exit(255)

def main():
    __creds = Credentials()
    __result00 = __creds._checkDirectory()
    __result01 = __creds._checkCredentials()
    __result02 = __creds._checkKey()
    
    # Packs the 3 integers (4 bytes each).
    buffer = struct.pack('iii', __result00, __result01, __result02)
    sys.stdout.buffer.write(buffer)

if __name__ == "__main__":
    main()