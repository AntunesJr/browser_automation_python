#!/usr/bin/env python3

from setuptools import setup, find_packages
import sys
import os

# Se executado com argumentos especiais (nosso script personalizado simplificado)
if len(sys.argv) > 1 and sys.argv[1] in ['--quick-setup', '--check-deps', '--validate']:
    import subprocess
    from pathlib import Path

    def quick_setup():
        """Setup rápido - redireciona para custom_setup.py"""
        print("""
        ╔══════════════════════════════════════════════════════════╗
        ║                    🚀 SETUP RÁPIDO v2.0                 ║
        ║            Chrome DevTools Protocol + Playwright        ║
        ╚══════════════════════════════════════════════════════════╝
        """)
        
        print("📋 Este é o setup.py v2.0 simplificado.")
        print("💡 Para configuração completa, use: python custom_setup.py")
        print("")
        
        custom_setup_path = Path("custom_setup.py")
        if custom_setup_path.exists():
            print("🔄 Executando custom_setup.py...")
            subprocess.run([sys.executable, "custom_setup.py"])
        else:
            print("❌ custom_setup.py não encontrado!")
            print("💡 Baixe de: https://github.com/seu-usuario/browser_automation_python")

    def check_dependencies():
        """Verifica dependências rapidamente"""
        print("🔍 Verificando dependências v2.0...")
        
        deps_v2 = {
            "playwright": "Playwright (CDP)",
            "pynput": "PyNput (Mouse/Keyboard)",
            "cryptography": "Cryptography (Credenciais)",
            "requests": "Requests (HTTP)",
            "psutil": "PSUtil (Sistema)"
        }
        
        for dep, desc in deps_v2.items():
            try:
                __import__(dep)
                print(f"   ✅ {desc}")
            except ImportError:
                print(f"   ❌ {desc} - Execute: pip install {dep}")

    def validate_project():
        """Valida estrutura do projeto"""
        print("📁 Validando estrutura do projeto v2.0...")
        
        required_files = [
            "main.py",
            "custom_setup.py", 
            "browser/browser_cdp.py",
            "credentials/credentials.py"
        ]
        
        missing = []
        for file in required_files:
            if Path(file).exists():
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file}")
                missing.append(file)
        
        if missing:
            print(f"\n⚠️ Arquivos faltando: {len(missing)}")
            print("💡 Baixe o projeto completo do GitHub")
        else:
            print("\n✅ Estrutura do projeto OK!")

    # Executar ação baseada no argumento
    if "--quick-setup" in sys.argv:
        quick_setup()
    elif "--check-deps" in sys.argv:
        check_dependencies()
    elif "--validate" in sys.argv:
        validate_project()
    
    sys.exit(0)

# Setup padrão do setuptools (atualizado para v2.0)
setup(
    name="browser-automation-python",
    version="2.0.0",
    author="Silvio Antunes", 
    author_email="silvioantunes1@hotmail.com",
    description="Advanced browser automation via Chrome DevTools Protocol with voice commands",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/browser_automation_python",
    license="GPL-3.0",
    packages=find_packages(),
    python_requires=">=3.8",
    
    # ========================================
    # DEPENDÊNCIAS ATUALIZADAS PARA v2.0
    # ========================================
    install_requires=[
        # Core: Playwright para controle via CDP
        "playwright>=1.40.0",
        
        # Controle de entrada
        "pynput>=1.7.6",
        
        # Sistema de credenciais 
        "cryptography>=38.0.0",
        
        # Comunicação e utilitários
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "coloredlogs>=15.0.1",
        
        # Build tools
        "setuptools>=65.5.0",
        
        # Compatibilidade Python < 3.4
        "pathlib2>=2.3.7; python_version < '3.4'"
    ],
    
    # ========================================
    # COMANDOS CLI ATUALIZADOS
    # ========================================
    entry_points={
        "console_scripts": [
            # === COMANDOS DE CREDENCIAIS ===
            "check_cred=credentials.commands.check_cred:main",
            "check_cred_json=credentials.commands.check_cred_json:main", 
            "create_cred=credentials.commands.create_cred:main",
            "create_cred_json=credentials.commands.creat_cred_json:main",
            "show_cred=credentials.commands.show_cred:main",
            "show_cred_json=credentials.commands.show_cred_json:main",
            
            # === COMANDOS DO SISTEMA ===
            "browser_automation=main:main",
            "setup_browser_automation=custom_setup:main",
            "test_browser_automation=test_installation:main",
            
            # === COMANDOS DE DESENVOLVIMENTO ===
            "identify_mouse_buttons=main:main --identify",
            "start_chrome_debug=scripts.start_chrome:main",
        ],
    },
    
    # ========================================
    # METADADOS ATUALIZADOS
    # ========================================
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: System Shells",
        "Environment :: Console",
        "Environment :: X11 Applications"
    ],
    
    # ========================================
    # CONFIGURAÇÕES ADICIONAIS
    # ========================================
    keywords=[
        "browser automation", "CDP", "chrome devtools", "playwright", 
        "voice commands", "PDV", "point of sale", "credentials", 
        "encryption", "mouse control", "automation", "bot"
    ],
    
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/browser_automation_python/issues",
        "Source": "https://github.com/seu-usuario/browser_automation_python", 
        "Documentation": "https://github.com/seu-usuario/browser_automation_python#readme",
        "Changelog": "https://github.com/seu-usuario/browser_automation_python/releases"
    },
    
    # Inclui arquivos não-Python
    include_package_data=True,
    
    # Especifica arquivos extras a incluir
    package_data={
        "": ["*.md", "*.txt", "*.sh", "*.json"],
        "credentials": ["commands/*.py", "config/*.py", "core/*.py", "crypto/*.py", "message/*.py"],
        "browser": ["*.py"],
        "scripts": ["*.py", "*.sh"]
    },
    
    # Dependências extras opcionais
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0", 
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0"
        ],
        "voice": [
            "SpeechRecognition>=3.10.0",
            "pyttsx3>=2.90",
            "pyaudio>=0.2.11"
        ],
        "ocr": [
            "pytesseract>=0.3.10",
            "opencv-python>=4.8.0",
            "pillow>=10.0.0"
        ]
    },
    
    # Configurações de instalação
    zip_safe=False,
    
    # Scripts shell a instalar
    scripts=[
        "start_chrome_debug.sh" if os.path.exists("start_chrome_debug.sh") else None
    ] if any(os.path.exists(f) for f in ["start_chrome_debug.sh"]) else [],
    
    # Metadados adicionais do projeto
    platforms=["Linux", "macOS", "Windows"],
    
    # Configuração de CI/CD (para futuro)
    cmdclass={},
    
    # Requer instalação em ordem específica (Playwright precisa de pós-instalação)
    install_requires_order=[
        "setuptools", "cryptography", "requests", "psutil", 
        "coloredlogs", "pynput", "playwright"
    ] if hasattr(setup, 'install_requires_order') else None
)

# ========================================
# PÓS-INSTALAÇÃO (INSTRUÇÕES)
# ========================================

# Mostra instruções após instalação bem-sucedida
def post_install_message():
    """Mensagem exibida após instalação"""
    message = """
    
╔══════════════════════════════════════════════════════════╗
║           🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!           ║
╚══════════════════════════════════════════════════════════╝

📋 PRÓXIMOS PASSOS:

1️⃣  Instale browsers do Playwright:
    python -m playwright install

2️⃣  Configure o ambiente completo:
    setup_browser_automation
    # OU: python custom_setup.py

3️⃣  Crie suas credenciais:
    create_cred "seu@email.com" "suaSenha123" --username "seuNome"

4️⃣  Inicie o Chrome debug:
    start_chrome_debug
    # OU: ./start_chrome_debug.sh

5️⃣  Execute o programa:
    browser_automation
    # OU: python main.py

🔧 COMANDOS DISPONÍVEIS:

   📋 Credenciais:
   • check_cred           - Verificar credenciais  
   • create_cred          - Criar credenciais
   • show_cred            - Mostrar credenciais

   🚀 Sistema:
   • browser_automation   - Executar programa principal
   • test_browser_automation - Testar instalação
   • identify_mouse_buttons - Configurar botões do mouse

📚 DOCUMENTAÇÃO:
   • README: https://github.com/seu-usuario/browser_automation_python#readme
   • Wiki: https://github.com/seu-usuario/browser_automation_python/wiki

💡 SUPORTE:
   • Issues: https://github.com/seu-usuario/browser_automation_python/issues
   • Email: silvioantunes1@hotmail.com

═══════════════════════════════════════════════════════════
"""
    print(message)

# Exibe a mensagem se foi instalado via pip install
if __name__ == "__main__":
    # Executa apenas se for chamado diretamente como script
    if len(sys.argv) > 1 and any(arg in sys.argv for arg in ['install', 'develop', '-e']):
        post_install_message()