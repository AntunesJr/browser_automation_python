#!/usr/bin/env python3

import sys
import json
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

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"\033[1;31m❌ Erro ao ler JSON: {e}\033[0m")
        sys.exit(1)

    email = input_data.get("email")
    password = input_data.get("password")
    username = input_data.get("username")
    keypass = input_data.get("keypass")

    if not email or not password:
        print("\033[1;31m❌ Campos obrigatórios: 'email' e 'password'\033[0m")
        sys.exit(1)

    creds = Credentials()
    status = creds.create_credentials(
        username=username,
        email=email,
        password=password,
        key_password=keypass
    )

    if status == MsgCode.SUCCESS:
        print(f"\033[1;32m✅ Credenciais criadas com sucesso.\033[0m")
        sys.exit(0)
    else:
        print(f"\033[1;31m❌ Erro: {MessageHandler.get(status)}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()