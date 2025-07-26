#!/usr/bin/env python3
"""
Output credential verification results in JSON format.
"""

import json
import sys
from credentials.credentials import Credentials
from credentials.message.msg_code import MsgCode
from credentials.message.msg_handler import MessageHandler

def main() -> None:
    """Main entry point for JSON credential check."""
    __creds = Credentials()
    __result00, __result01, __result02 = __creds.checker()
    results = {
        "directory": __result00,
        "credentials": __result01,
        "key": __result02,
    }
    
    output = {
        "checks": [
            {
                "name": key,
                "code": value,
                "message": MessageHandler.get( value )
            }
            for key, value in results.items()
        ],
        "overall_status": "secure" if all( c == MsgCode.SUCCESS for c in results.values() ) else "insecure"
    }
    
    print(json.dumps(output, indent=2))
    sys.exit(0 if output["overall_status"] == "secure" else 1)

if __name__ == "__main__":
    main()