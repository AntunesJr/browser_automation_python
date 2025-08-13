#!/usr/bin/env python3
"""
Script personalizado de configuração do ambiente de desenvolvimento
Execute: python custom_setup.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║            🚀 CONFIGURAÇÃO DO AMBIENTE                   ║
    ║                 Browser Automation                      ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    print("🔍 Verificando versão do Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_virtual_env():
    """Verifica se está em um ambiente virtual"""
    print("\n🏠 Verificando ambiente virtual...")
    
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )
    
    if in_venv:
        venv_path = os.environ.get('VIRTUAL_ENV', 'detectado')
        print(f"✅ Ambiente virtual ativo: {venv_path}")
        return True
    else:
        print("⚠️  Ambiente virtual não detectado")
        print("   Recomendado criar um venv: python -m venv .venv")
        return False

def install_package_safely(package_name, display_name=None):
    """Instala um pacote de forma segura"""
    display_name = display_name or package_name
    try:
        print(f"   📦 Instalando {display_name}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name, "--upgrade", "--quiet"
        ])
        print(f"   ✅ {display_name} instalado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao instalar {display_name}: {e}")
        return False

def install_requirements():
    """Instala as dependências necessárias"""
    print("\n📦 Instalando dependências do projeto...")
    
    # Atualizar pip primeiro
    print("   🔧 Atualizando pip...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"
        ])
        print("   ✅ Pip atualizado")
    except:
        print("   ⚠️  Aviso: Não foi possível atualizar o pip")
    
    requirements = [
        ("selenium>=4.15.0", "Selenium (automação web)"),
        ("pynput>=1.7.6", "PyNput (controle de entrada)"),
        ("requests>=2.31.0", "Requests (HTTP)"),
        ("psutil>=5.9.0", "PSUtil (sistema)"),
        ("fake-useragent>=1.4.0", "Fake UserAgent"),
        ("cryptography>=38.0.0", "Cryptography (encriptação)"),
        ("coloredlogs>=15.0.1", "Colored Logs"),
        ("jsonschema>=4.19.0", "JSON Schema")
    ]
    
    success_count = 0
    for requirement, display_name in requirements:
        if install_package_safely(requirement, display_name):
            success_count += 1
    
    print(f"\n   📊 Resultado: {success_count}/{len(requirements)} dependências instaladas")
    return success_count == len(requirements)

def check_firefox():
    """Verifica se o Firefox está instalado"""
    print("\n🦊 Verificando Firefox...")
    
    firefox_paths = {
        "Windows": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ],
        "Linux": [
            "/usr/bin/firefox",
            "/usr/local/bin/firefox",
            "/snap/bin/firefox",
            "/usr/bin/firefox-esr"
        ],
        "Darwin": [
            "/Applications/Firefox.app/Contents/MacOS/firefox"
        ]
    }
    
    system = platform.system()
    paths = firefox_paths.get(system, [])
    
    for path in paths:
        if os.path.exists(path):
            print(f"✅ Firefox encontrado: {path}")
            return True
    
    print("❌ Firefox não encontrado")
    print("   📥 Baixe em: https://www.mozilla.org/firefox/")
    return False

def check_geckodriver():
    """Verifica se o GeckoDriver está disponível"""
    print("\n🔧 Verificando GeckoDriver...")
    
    try:
        result = subprocess.run(
            ["geckodriver", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ {version}")
            return True
    except:
        pass
    
    print("❌ GeckoDriver não encontrado")
    system = platform.system().lower()
    
    if "linux" in system:
        print("   💻 Ubuntu/Debian: sudo apt install firefox-geckodriver")
        print("   🔗 Ou: https://github.com/mozilla/geckodriver/releases")
    elif "darwin" in system:
        print("   🍺 Homebrew: brew install geckodriver")
    else:
        print("   🔗 Download: https://github.com/mozilla/geckodriver/releases")
    
    return False

def create_project_structure():
    """Cria estrutura de diretórios necessária"""
    print("\n📁 Verificando estrutura do projeto...")
    
    directories = [
        "browser",
        "credentials",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"   📂 Criado: {directory}/")
        
        # Criar __init__.py se necessário
        init_file = dir_path / "__init__.py"
        if directory in ["browser", "credentials"] and not init_file.exists():
            init_file.touch()
            print(f"   📝 Criado: {directory}/__init__.py")
    
    print("✅ Estrutura de diretórios OK")
    return True

def test_imports():
    """Testa se as importações funcionam"""
    print("\n🧪 Testando importações...")
    
    test_modules = [
        ("selenium", "Selenium"),
        ("pynput", "PyNput"),
        ("requests", "Requests"),
        ("psutil", "PSUtil"),
        ("cryptography", "Cryptography")
    ]
    
    success_count = 0
    for module, name in test_modules:
        try:
            __import__(module)
            print(f"   ✅ {name}")
            success_count += 1
        except ImportError:
            print(f"   ❌ {name}")
    
    return success_count == len(test_modules)

def test_webdriver():
    """Testa se o WebDriver funciona"""
    print("\n🚗 Testando WebDriver Firefox...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Firefox(options=options)
        driver.get("about:blank")
        driver.quit()
        
        print("   ✅ WebDriver Firefox funcionando")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no WebDriver: {str(e)[:100]}...")
        return False

def install_project():
    """Instala o projeto em modo desenvolvimento"""
    print("\n📦 Instalando projeto...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", ".", "--quiet"
        ])
        print("✅ Projeto instalado em modo desenvolvimento")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def run_credentials_test():
    """Testa o sistema de credenciais"""
    print("\n🔐 Testando sistema de credenciais...")
    
    try:
        from credentials.credentials import Credentials
        creds = Credentials()
        print("   ✅ Sistema de credenciais carregado")
        return True
    except Exception as e:
        print(f"   ❌ Erro no sistema de credenciais: {e}")
        return False

def show_final_instructions(all_success):
    """Mostra instruções finais"""
    print("\n" + "="*60)
    
    if all_success:
        print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n✅ Ambiente pronto para desenvolvimento!")
        print("\n📋 Próximos passos:")
        print("   1. Configure suas credenciais:")
        print("      python -c \"from credentials.credentials import Credentials; print('Sistema OK')\"")
        print("   2. Execute o programa principal:")
        print("      python main.py")
        print("   3. Ou execute testes:")
        print("      python -m pytest tests/ (se tiver pytest instalado)")
        
    else:
        print("⚠️  CONFIGURAÇÃO INCOMPLETA")
        print("="*60)
        print("\n❌ Alguns componentes apresentaram problemas")
        print("   Revise os erros acima e tente resolver os problemas")
        print("   Você pode executar este script novamente após as correções")
    
    print("\n📚 Comandos úteis:")
    print("   check_cred          - Verificar credenciais")
    print("   create_cred         - Criar credenciais")
    print("   python main.py      - Executar automação")
    print("="*60)

def main():
    """Função principal"""
    print_banner()
    
    checks = [
        ("Python", check_python_version),
        ("Ambiente Virtual", check_virtual_env),
        ("Dependências", install_requirements),
        ("Firefox", check_firefox),
        ("GeckoDriver", check_geckodriver),
        ("Estrutura", create_project_structure),
        ("Importações", test_imports),
        ("Projeto", install_project),
        ("WebDriver", test_webdriver),
        ("Credenciais", run_credentials_test)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n🔍 Verificando {name}...")
        try:
            success = check_func()
            results.append((name, success))
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")
            results.append((name, False))
    
    # Resumo
    print("\n📊 RESUMO DOS TESTES:")
    print("-" * 30)
    success_count = 0
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {name}")
        if success:
            success_count += 1
    
    all_success = success_count == len(results)
    show_final_instructions(all_success)
    
    return 0 if all_success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n🛑 Configuração cancelada pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)