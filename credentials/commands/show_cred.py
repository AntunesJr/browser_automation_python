#!/usr/bin/env python3

import argparse
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

def main():
    parser = argparse.ArgumentParser(description="Exibe credenciais descriptografadas em formato legível.")
    parser.add_argument("--config_name", type=str, help="Nome da configuração salva", default=None)
    args = parser.parse_args()

    try:
        creds = Credentials(config_name=args.config_name) if args.config_name else Credentials()
        status, data = creds.load_credentials()
        
        if status != MsgCode.SUCCESS:
            print(f"\033[1;31m❌ Erro: {MessageHandler.get(status)}\033[0m")
            sys.exit(1)

        print("\033[1;34m🔓 Credenciais descriptografadas:\033[0m")
        print(f"  📛 Usuário: {data.get('username')}")
        print(f"  📧 Email:   {data.get('email')}")
        print(f"  🔑 Senha:   {data.get('password')}")

        additional = data.get("additional_data", {})
        if additional:
            print(f"\n  🧩 Dados adicionais:")
            for key, value in additional.items():
                print(f"    - {key}: {value}")
        
        sys.exit(0)

    except Exception as e:
        print(f"\033[1;31m❌ Erro inesperado: {e}\033[0m")
        sys.exit(255)

if __name__ == "__main__":
    main()
