#!/usr/bin/env python3

from setuptools import setup, find_packages
import sys
import os

# Se executado com argumentos especiais (nosso script personalizado)
if len(sys.argv) > 1 and sys.argv[1] in ['--install', '--quick', '--validate', '--no-optional', '--quiet']:
    # Nosso script personalizado de setup
    import subprocess
    import platform
    from pathlib import Path

    def print_banner():
        print("""
        ╔══════════════════════════════════════════════════════════╗
        ║            🚀 SETUP DE AUTOMAÇÃO DE BROWSERS             ║
        ║                      Versão Stealth                     ║
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

    def install_requirements():
        """Instala as dependências necessárias"""
        print("\n📦 Instalando dependências...")
        
        requirements = [
            "selenium>=4.15.0",
            "pynput>=1.7.6", 
            "requests>=2.31.0",
            "psutil>=5.9.0",
            "fake-useragent>=1.4.0",
            "cryptography>=38.0.0"
        ]
        
        for requirement in requirements:
            try:
                print(f"   Instalando {requirement.split('>=')[0]}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", requirement, "--quiet"
                ])
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar {requirement}: {e}")
                return False
        
        print("✅ Todas as dependências foram instaladas!")
        return True

    def check_firefox():
        """Verifica se o Firefox está instalado"""
        print("\n🦊 Verificando Firefox...")
        
        # Caminhos comuns do Firefox
        firefox_paths = {
            "Windows": [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            ],
            "Linux": [
                "/usr/bin/firefox",
                "/usr/local/bin/firefox",
                "/snap/bin/firefox"
            ],
            "Darwin": [  # macOS
                "/Applications/Firefox.app/Contents/MacOS/firefox"
            ]
        }
        
        system = platform.system()
        paths = firefox_paths.get(system, [])
        
        firefox_found = False
        for path in paths:
            if os.path.exists(path):
                print(f"✅ Firefox encontrado: {path}")
                firefox_found = True
                break
        
        if not firefox_found:
            print("⚠️  Firefox não encontrado nos caminhos padrão")
            print("   Por favor, instale o Firefox antes de continuar")
            print("   Download: https://www.mozilla.org/firefox/")
            return False
        
        return True

    def check_geckodriver():
        """Verifica se o GeckoDriver está disponível"""
        print("\n🔧 Verificando GeckoDriver...")
        
        try:
            result = subprocess.run(
                ["geckodriver", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"✅ {version}")
                return True
            else:
                raise subprocess.CalledProcessError(result.returncode, "geckodriver")
                
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print("❌ GeckoDriver não encontrado!")
            print_geckodriver_install_instructions()
            return False

    def print_geckodriver_install_instructions():
        """Imprime instruções para instalar o GeckoDriver"""
        system = platform.system().lower()
        
        print("\n📋 INSTRUÇÕES PARA INSTALAR GECKODRIVER:")
        print("="*50)
        
        if "windows" in system:
            print("Windows:")
            print("1. Baixe: https://github.com/mozilla/geckodriver/releases")
            print("2. Extraia geckodriver.exe")
            print("3. Adicione ao PATH ou coloque na pasta do projeto")
            print("4. Ou use chocolatey: choco install geckodriver")
            
        elif "linux" in system:
            print("Linux:")
            print("1. Ubuntu/Debian: sudo apt install firefox-geckodriver")
            print("2. Ou baixe: https://github.com/mozilla/geckodriver/releases")
            print("3. Mova para /usr/local/bin/: sudo mv geckodriver /usr/local/bin/")
            
        elif "darwin" in system:
            print("macOS:")
            print("1. Com Homebrew: brew install geckodriver")
            print("2. Ou baixe: https://github.com/mozilla/geckodriver/releases")

    def create_browser_directory():
        """Cria diretório browser se não existir"""
        print("\n📁 Criando estrutura de diretórios...")
        
        browser_dir = Path("browser")
        browser_dir.mkdir(exist_ok=True)
        
        # Criar __init__.py se não existir
        init_file = browser_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print("✅ Diretório browser configurado")

    def run_test():
        """Executa um teste básico do sistema"""
        print("\n🧪 Executando teste básico...")
        
        try:
            # Test import selenium
            import selenium
            print("✅ Selenium importado com sucesso")
            
            # Test import pynput
            import pynput
            print("✅ Pynput importado com sucesso")
            
            # Test Firefox WebDriver creation (sem abrir browser)
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options
            
            options = Options()
            options.add_argument("--headless")  # Não abrir janela
            
            try:
                driver = webdriver.Firefox(options=options)
                driver.quit()
                print("✅ WebDriver Firefox funcional")
            except Exception as e:
                print(f"❌ Erro no WebDriver: {e}")
                return False
            
            return True
            
        except ImportError as e:
            print(f"❌ Erro de importação: {e}")
            return False

    def custom_setup_main():
        """Função principal do setup customizado"""
        print_banner()
        
        success = True
        
        # Verificações sequenciais
        if not check_python_version():
            success = False
        
        if not install_requirements():
            success = False
        
        if not check_firefox():
            success = False
        
        if not check_geckodriver():
            success = False
        
        # Criar estrutura de arquivos
        create_browser_directory()
        
        # Teste final
        if success and run_test():
            print("\n" + "="*60)
            print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
            print("="*60)
            print("✅ Sistema pronto para uso")
            print("🔧 Lembre-se de configurar suas credenciais")
            print("🚀 Execute: python main.py")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ SETUP INCOMPLETO")
            print("="*60)
            print("Por favor, resolva os problemas indicados acima")
            print("="*60)

    # Executar setup customizado
    custom_setup_main()
    
else:
    # Setup padrão do setuptools
    setup(
        name="browser_automation-python",
        version="0.1.0",
        author="Silvio Antunes",
        author_email="silvioantunes1@hotmail.com",
        description="Browser automation in python",
        long_description=open("README.md").read() if os.path.exists("README.md") else "",
        long_description_content_type="text/markdown",
        license="GPL-3.0",
        packages=find_packages(),
        python_requires=">=3.8",
        install_requires=[
            "selenium>=4.15.0",
            "pynput>=1.7.6",
            "requests>=2.31.0",
            "psutil>=5.9.0",
            "fake-useragent>=1.4.0",
            "cryptography>=38.0.0",
        ],
        entry_points={
            "console_scripts": [
                "check_cred=credentials.commands.check_cred:main",
                "check_cred_json=credentials.commands.check_cred_json:main",
                "create_cred=credentials.commands.create_cred:main",
                "show_cred=credentials.commands.show_cred:main",
                "show_cred_json=credentials.commands.show_cred_json:main"
            ],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Security :: Cryptography",
        ],
    )