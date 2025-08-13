#!/usr/bin/env python3
"""
Script de configuração do ambiente para Browser Automation
Execute: python custom_setup.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Configurações do projeto
PROJECT_DIRS = ["browser", "credentials", "logs", "temp"]
REQUIREMENTS = [
    "selenium>=4.15.0",
    "pynput>=1.7.6",
    "requests>=2.31.0",
    "psutil>=5.9.0",
    "fake-useragent>=1.4.0",
    "cryptography>=38.0.0",
    "coloredlogs>=15.0.1",
    "jsonschema>=4.19.0"
]

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         🚀 CONFIGURAÇÃO DO AMBIENTE DE AUTOMAÇÃO         ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    print("\n🔍 Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ necessário! Versão atual: {sys.version.split()[0]}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatível")
    return True

def setup_virtual_env():
    print("\n🏠 Configurando ambiente virtual...")
    venv_dir = ".venv"
    
    if not os.path.exists(venv_dir):
        print("   Criando novo ambiente virtual...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
            print(f"   ✅ Ambiente virtual criado em: {venv_dir}")
        except subprocess.CalledProcessError:
            print("   ❌ Falha ao criar ambiente virtual")
            return False
    else:
        print(f"   ✅ Ambiente virtual existente encontrado em: {venv_dir}")
    
    # Ativar o ambiente virtual
    activate_script = "Scripts\\activate" if platform.system() == "Windows" else "bin/activate"
    activate_path = os.path.join(venv_dir, activate_script)
    
    if not os.path.exists(activate_path):
        print(f"   ❌ Script de ativação não encontrado: {activate_path}")
        return False
    
    print(f"\n📌 Para ativar o ambiente virtual:")
    print(f"   Windows: .\\{venv_dir}\\Scripts\\activate")
    print(f"   Linux/macOS: source {venv_dir}/bin/activate")
    return True

def install_dependencies():
    print("\n📦 Instalando dependências...")
    try:
        # Atualizar pip
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"
        ])
        
        # Instalar pacotes
        for package in REQUIREMENTS:
            print(f"   📦 Instalando {package.split('>')[0]}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--quiet"
            ])
        
        print("✅ Todas dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def setup_firefox():
    print("\n🦊 Configurando Firefox...")
    system = platform.system()
    
    # Verificar instalação do Firefox
    firefox_paths = {
        "Windows": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ],
        "Linux": ["/usr/bin/firefox", "/usr/bin/firefox-esr"],
        "Darwin": ["/Applications/Firefox.app/Contents/MacOS/firefox"]
    }
    
    for path in firefox_paths.get(system, []):
        if os.path.exists(path):
            print(f"✅ Firefox encontrado: {path}")
            break
    else:
        print("❌ Firefox não encontrado")
        print("   📥 Download: https://www.mozilla.org/firefox/")
        return False
    
    # Verificar GeckoDriver
    print("\n🔧 Verificando GeckoDriver...")
    try:
        result = subprocess.run(
            ["geckodriver", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {version}")
            return True
    except:
        pass
    
    print("❌ GeckoDriver não encontrado")
    
    install_commands = {
        "Linux": "sudo apt install firefox-geckodriver",
        "Darwin": "brew install geckodriver"
    }
    
    if system in install_commands:
        print(f"   💡 Comando de instalação: {install_commands[system]}")
    else:
        print("   🔗 Download: https://github.com/mozilla/geckodriver/releases")
    
    return False

def create_project_structure():
    print("\n📁 Criando estrutura de diretórios...")
    for directory in PROJECT_DIRS:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📂 Criado: {directory}/")
            
            # Adicionar __init__.py para módulos Python
            if directory in ["browser", "credentials"]:
                init_file = dir_path / "__init__.py"
                init_file.touch()
                print(f"   📝 Criado: {directory}/__init__.py")
    
    # Criar arquivo .env.example se não existir
    env_example = Path(".env.example")
    if not env_example.exists():
        with env_example.open("w") as f:
            f.write("# Configurações de ambiente\n")
            f.write("USERNAME=seu_usuario\n")
            f.write("PASSWORD=sua_senha\n")
            f.write("API_KEY=sua_chave_api\n")
        print("   📝 Criado: .env.example")
    
    print("✅ Estrutura do projeto configurada")
    return True

def test_environment():
    print("\n🧪 Testando ambiente...")
    tests = [
        ("Selenium", "from selenium import webdriver"),
        ("PyNput", "from pynput import keyboard, mouse"),
        ("Requests", "import requests"),
        ("PSUtil", "import psutil"),
        ("WebDriver", "driver = webdriver.Firefox(options=webdriver.FirefoxOptions()); driver.quit()")
    ]
    
    success = True
    for name, code in tests:
        try:
            subprocess.check_call([
                sys.executable, "-c", 
                f"try:\n    {code}\nexcept Exception as e:\n    print(f'❌ {name}: {{e}}')\n    exit(1)"
            ])
            print(f"   ✅ {name}")
        except subprocess.CalledProcessError:
            print(f"   ❌ {name} - Erro na importação/execução")
            success = False
    
    return success

def show_next_steps():
    print("\n" + "="*60)
    print("✅ CONFIGURAÇÃO COMPLETA!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("1. Ative o ambiente virtual:")
    print("   Windows: .\\.venv\\Scripts\\activate")
    print("   Linux/macOS: source .venv/bin/activate")
    print("2. Configure suas credenciais:")
    print("   - Copie .env.example para .env")
    print("   - Edite o arquivo .env com suas informações")
    print("3. Execute o script principal:")
    print("   python main.py")
    print("\n🛠️  Comandos úteis:")
    print("   python -m browser.automation  # Executar automação")
    print("   python -m credentials.manager # Gerenciar credenciais")
    print("="*60)

def main():
    print_banner()
    
    # Executar etapas de configuração
    steps = [
        ("Versão do Python", check_python_version),
        ("Ambiente Virtual", setup_virtual_env),
        ("Dependências", install_dependencies),
        ("Firefox e Driver", setup_firefox),
        ("Estrutura do Projeto", create_project_structure),
        ("Testes de Ambiente", test_environment)
    ]
    
    results = []
    for name, step in steps:
        print(f"\n🔧 {name}...")
        try:
            success = step()
            results.append(success)
            print("✅ Concluído" if success else "❌ Falhou")
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")
            results.append(False)
    
    # Mostrar resumo
    print("\n📊 RESUMO DA CONFIGURAÇÃO:")
    for i, (name, _) in enumerate(steps):
        status = "✅" if results[i] else "❌"
        print(f"   {status} {name}")
    
    if all(results):
        show_next_steps()
        return 0
    else:
        print("\n⚠️ ALGUMAS ETAPAS FALHARAM!")
        print("Revise as mensagens de erro acima e tente novamente")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Configuração cancelada pelo usuário")
        sys.exit(130)