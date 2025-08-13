#!/usr/bin/env python3

import sys
import argparse
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

#create_cred "email@email.com" "minhaSenha123" --username silvio --keypass "senhaChaveOpcional"
def main():
    parser = argparse.ArgumentParser(description="Create encrypted credentials via CLI arguments.")
    parser.add_argument("email", type=str, help="Email do usuário")
    parser.add_argument("password", type=str, help="Senha do usuário")
    parser.add_argument("--username", type=str, help="Nome de usuário", default=None)
    parser.add_argument("--keypass", type=str, help="Senha da chave criptográfica", default=None)
    args = parser.parse_args()

    creds = Credentials()
    status = creds.create_credentials(
        username=args.username,
        email=args.email,
        password=args.password,
        key_password=args.keypass
    )

    if status == MsgCode.SUCCESS:
        print(f"\033[1;32m✅ Credenciais salvas com sucesso.\033[0m")
        sys.exit(0)
    else:
        print(f"\033[1;31m❌ Erro: {MessageHandler.get(status)}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()