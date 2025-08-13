#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

try:
    from credentials.credentials import Credentials
    from credentials.message.msg_code import MsgCode
    from credentials.message.msg_handler import MessageHandler
except ImportError:
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    sys.path.insert(0, str(root_dir))
    from credentials.credentials import Credentials
    from credentials.message.msg_code import MsgCode
    from credentials.message.msg_handler import MessageHandler

#echo '{"email": "email@email.com", "password": "minhaSenha123", "username": "silvio"}' | create_cred_json
def main():
    parser = argparse.ArgumentParser(description="Exibe credenciais descriptografadas no formato JSON.")
    parser.add_argument("--config_name", type=str, help="Nome da configuração salva", default=None)
    args = parser.parse_args()

    try:
        creds = Credentials(config_name=args.config_name) if args.config_name else Credentials()
        status, data = creds.load_credentials()

        if status != MsgCode.SUCCESS:
            output = {
                "success": False,
                "error": MessageHandler.get(status),
                "config": args.config_name or "default"
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
            sys.exit(1)

        print(json.dumps({
            "success": True,
            "config": args.config_name or "default",
            "credentials": data
        }, indent=2, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        output = {
            "success": False,
            "error": str(e),
            "config": args.config_name or "default"
        }
        print(json.dumps(output, indent=2))
        sys.exit(255)

if __name__ == "__main__":
    main()
