#!/usr/bin/env python3
"""
Script de configuração atualizado para o sistema de automação via CDP
Dependências: Playwright + Google Chrome + Sistema de Credenciais
Autor: Browser Automation
Versão: 2.0.0
"""

import os
import sys
import subprocess
import platform
import requests
import time
from pathlib import Path

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║            🚀 CONFIGURAÇÃO DO AMBIENTE v2.0              ║
    ║           Chrome DevTools Protocol + Playwright         ║
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

def get_system_info():
    """Obtém informações do sistema"""
    system = platform.system()
    arch = platform.machine()
    distro = "Unknown"
    
    try:
        # Tenta identificar a distribuição Linux
        if system == "Linux":
            with open("/etc/os-release", "r") as f:
                content = f.read()
                if "debian" in content.lower() or "ubuntu" in content.lower():
                    distro = "Debian/Ubuntu"
                elif "fedora" in content.lower():
                    distro = "Fedora"
                elif "arch" in content.lower():
                    distro = "Arch"
                else:
                    distro = "Linux"
    except:
        pass
    
    print(f"\n💻 Sistema detectado: {system} {arch} ({distro})")
    return system, arch, distro

def install_system_dependencies(system, distro):
    """Instala dependências do sistema"""
    print("\n📦 Instalando dependências do sistema...")
    
    if system == "Linux":
        if "Debian" in distro:
            # Atualizar repositórios
            print("   🔄 Atualizando repositórios...")
            try:
                subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
                print("   ✅ Repositórios atualizados")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️ Aviso: Erro ao atualizar repositórios: {e}")
            
            # Dependências essenciais
            essential_packages = [
                "curl",
                "wget", 
                "software-properties-common",
                "apt-transport-https",
                "ca-certificates",
                "gnupg",
                "lsb-release",
                "python3-pip",
                "python3-dev",
                "python3-tk",  # Para pynput
                "xvfb",  # Para headless se necessário
                "dbus-x11"  # Para evitar problemas de sessão
            ]
            
            print("   📋 Instalando pacotes essenciais...")
            for package in essential_packages:
                try:
                    result = subprocess.run(
                        ["dpkg", "-l", package], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode != 0:
                        print(f"   📦 Instalando {package}...")
                        subprocess.run(
                            ["sudo", "apt", "install", "-y", package], 
                            check=True, 
                            capture_output=True
                        )
                        print(f"   ✅ {package} instalado")
                    else:
                        print(f"   ✓ {package} já instalado")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️ Erro ao instalar {package}: {e}")
                    continue
            
            return True
            
        elif "Fedora" in distro:
            packages = [
                "curl", "wget", "python3-pip", "python3-devel", 
                "python3-tkinter", "xorg-x11-server-Xvfb"
            ]
            try:
                subprocess.run(["sudo", "dnf", "install", "-y"] + packages, check=True)
                print("   ✅ Dependências Fedora instaladas")
                return True
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Erro ao instalar dependências Fedora: {e}")
                return False
                
        else:
            print("   ⚠️ Distribuição Linux não reconhecida - pule se já tiver as dependências")
            return True
            
    elif system == "Darwin":  # macOS
        try:
            # Verifica se Homebrew está instalado
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            print("   ✅ Homebrew detectado")
            
            # Instala dependências via Homebrew
            packages = ["python3", "curl"]
            subprocess.run(["brew", "install"] + packages, check=True)
            print("   ✅ Dependências macOS instaladas via Homebrew")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️ Homebrew não encontrado - instale manualmente se necessário")
            return True
            
    else:  # Windows
        print("   ℹ️ Windows detectado - dependências do sistema gerenciadas pelo pip")
        return True

def install_google_chrome(system, arch):
    """Instala o Google Chrome"""
    print("\n🌐 Verificando Google Chrome...")
    
    # Verifica se Chrome já está instalado
    chrome_commands = [
        "google-chrome-stable",
        "google-chrome", 
        "chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome"
    ]
    
    for cmd in chrome_commands:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ Chrome já instalado: {version}")
                return True, cmd
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    print("   📥 Chrome não encontrado, instalando...")
    
    if system == "Linux":
        # Método 1: Repositório oficial do Google
        try:
            print("   🔧 Adicionando repositório oficial do Google Chrome...")
            
            # Baixa e adiciona a chave GPG
            subprocess.run([
                "curl", "-fSsL", 
                "https://dl.google.com/linux/linux_signing_key.pub"
            ], check=True, stdout=subprocess.PIPE)
            
            gpg_result = subprocess.run([
                "curl", "-fSsL", 
                "https://dl.google.com/linux/linux_signing_key.pub"
            ], capture_output=True, check=True)
            
            subprocess.run([
                "sudo", "gpg", "--dearmor", "-o", 
                "/usr/share/keyrings/google-chrome.gpg"
            ], input=gpg_result.stdout, check=True)
            
            # Adiciona repositório
            repo_content = "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main"
            subprocess.run([
                "sudo", "tee", "/etc/apt/sources.list.d/google-chrome.list"
            ], input=repo_content, text=True, check=True, capture_output=True)
            
            # Atualiza e instala
            subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
            subprocess.run(["sudo", "apt", "install", "-y", "google-chrome-stable"], check=True)
            
            print("   ✅ Google Chrome instalado via repositório oficial")
            return True, "google-chrome-stable"
            
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Falha no método 1: {e}")
            
            # Método 2: Download direto do .deb
            try:
                print("   🔄 Tentando instalação via download direto...")
                
                if arch == "x86_64":
                    chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
                    chrome_file = "/tmp/google-chrome-stable_current_amd64.deb"
                    
                    # Download
                    subprocess.run(["wget", "-O", chrome_file, chrome_url], check=True)
                    
                    # Instala
                    subprocess.run(["sudo", "dpkg", "-i", chrome_file], check=True)
                    subprocess.run(["sudo", "apt", "install", "-f", "-y"], check=True)  # Corrige dependências
                    
                    # Limpa arquivo temporário
                    os.remove(chrome_file)
                    
                    print("   ✅ Google Chrome instalado via download direto")
                    return True, "google-chrome-stable"
                else:
                    print(f"   ❌ Arquitetura {arch} não suportada pelo Chrome")
                    print("   💡 Tente usar Chromium: sudo apt install chromium")
                    return False, None
                    
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Falha no método 2: {e}")
                print("   💡 Instale manualmente ou use Chromium")
                return False, None
                
    elif system == "Darwin":  # macOS
        try:
            # Instala via Homebrew Cask
            subprocess.run(["brew", "install", "--cask", "google-chrome"], check=True)
            print("   ✅ Google Chrome instalado via Homebrew")
            return True, "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar Chrome no macOS: {e}")
            print("   💡 Baixe manualmente de: https://www.google.com/chrome/")
            return False, None
            
    elif system == "Windows":
        print("   ℹ️ Windows detectado")
        print("   💡 Baixe o Chrome manualmente de: https://www.google.com/chrome/")
        print("   💡 Ou use o Edge (compatível com CDP)")
        return False, None
    
    return False, None

def install_python_dependencies():
    """Instala dependências Python específicas do projeto"""
    print("\n📦 Instalando dependências Python...")
    
    # Atualizar pip primeiro
    print("   🔧 Atualizando pip...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        print("   ✅ Pip atualizado")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Aviso: Não foi possível atualizar o pip: {e}")
    
    # Dependências atualizadas para o novo sistema
    new_requirements = [
        ("playwright>=1.40.0", "Playwright (controle de browser via CDP)"),
        ("pynput>=1.7.6", "PyNput (controle de mouse/teclado)"),
        ("cryptography>=38.0.0", "Cryptography (sistema de credenciais)"),
        ("requests>=2.31.0", "Requests (HTTP)"),
        ("psutil>=5.9.0", "PSUtil (monitoramento de processos)"),
        ("coloredlogs>=15.0.1", "Colored Logs (logs formatados)"),
        ("pathlib", "PathLib (manipulação de caminhos)"),
    ]
    
    # Remove dependências antigas desnecessárias
    old_packages = ["selenium", "fake-useragent", "jsonschema"]
    print("   🧹 Removendo dependências antigas...")
    for package in old_packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], capture_output=True)
            print(f"   🗑️ {package} removido")
        except:
            pass
    
    # Instala novas dependências
    success_count = 0
    for requirement, display_name in new_requirements:
        try:
            print(f"   📦 Instalando {display_name}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", requirement, "--upgrade"
            ], check=True, capture_output=True)
            print(f"   ✅ {display_name} instalado")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar {display_name}: {e}")
    
    print(f"\n   📊 Resultado: {success_count}/{len(new_requirements)} dependências instaladas")
    
    # Instala dependências do Playwright
    print("   🎭 Instalando browsers do Playwright...")
    try:
        subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], check=True)
        print("   ✅ Chromium do Playwright instalado")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Erro ao instalar browsers Playwright: {e}")
        print("   💡 Execute manualmente: python -m playwright install")
    
    return success_count == len(new_requirements)

def create_project_structure():
    """Cria estrutura de diretórios necessária"""
    print("\n📁 Verificando estrutura do projeto...")
    
    directories = [
        "browser",
        "credentials", 
        "credentials/commands",
        "credentials/config",
        "credentials/core",
        "credentials/crypto",
        "credentials/message",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📂 Criado: {directory}/")
        
        # Criar __init__.py nos módulos Python
        if directory.startswith(("browser", "credentials")):
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"   📝 Criado: {directory}/__init__.py")
    
    print("✅ Estrutura de diretórios OK")
    return True

def test_imports():
    """Testa se as importações funcionam"""
    print("\n🧪 Testando importações...")
    
    test_modules = [
        ("playwright", "Playwright"),
        ("playwright.sync_api", "Playwright Sync API"),
        ("pynput", "PyNput"),
        ("pynput.mouse", "PyNput Mouse"),
        ("cryptography", "Cryptography"),
        ("requests", "Requests"),
        ("psutil", "PSUtil")
    ]
    
    success_count = 0
    for module, name in test_modules:
        try:
            __import__(module)
            print(f"   ✅ {name}")
            success_count += 1
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
    
    return success_count == len(test_modules)

def test_chrome_debug():
    """Testa se o Chrome pode ser iniciado em modo debug"""
    print("\n🚗 Testando Chrome em modo debug...")
    
    chrome_commands = ["google-chrome-stable", "google-chrome"]
    
    for cmd in chrome_commands:
        try:
            # Tenta iniciar Chrome em modo debug
            print(f"   🔧 Testando comando: {cmd}")
            
            # Cria diretório temporário para perfil
            import tempfile
            temp_dir = tempfile.mkdtemp(prefix="chrome-debug-test-")
            
            # Inicia Chrome em background
            proc = subprocess.Popen([
                cmd,
                "--remote-debugging-port=9223",  # Porta diferente para teste
                f"--user-data-dir={temp_dir}",
                "--headless",
                "--no-sandbox",
                "--disable-gpu"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Aguarda inicialização
            time.sleep(3)
            
            # Testa conexão CDP
            try:
                response = requests.get("http://localhost:9223/json", timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ Chrome debug funcionando com {cmd}")
                    
                    # Mata processo
                    proc.terminate()
                    proc.wait(timeout=5)
                    
                    # Limpa diretório temporário
                    import shutil
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    
                    return True, cmd
            except requests.RequestException:
                pass
            
            # Mata processo se ainda estiver rodando
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                proc.kill()
            
            # Limpa diretório temporário
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"   ⚠️ Erro ao testar {cmd}: {e}")
            continue
    
    print("   ❌ Nenhum comando Chrome funcionou em modo debug")
    return False, None

def test_playwright_cdp():
    """Testa se o Playwright consegue conectar via CDP"""
    print("\n🎭 Testando conexão Playwright + CDP...")
    
    try:
        # Inicia Chrome debug
        import tempfile
        temp_dir = tempfile.mkdtemp(prefix="playwright-test-")
        
        chrome_proc = subprocess.Popen([
            "google-chrome-stable",
            "--remote-debugging-port=9224",
            f"--user-data-dir={temp_dir}",
            "--headless",
            "--no-sandbox"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(3)
        
        # Testa Playwright
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9224")
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()
            page.goto("data:text/html,<h1>Teste Playwright</h1>")
            
            title = page.title()
            browser.close()
            
            print(f"   ✅ Playwright + CDP funcionando - Título: '{title}'")
            
            # Cleanup
            chrome_proc.terminate()
            chrome_proc.wait(timeout=5)
            
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return True
    
    except Exception as e:
        print(f"   ❌ Erro no teste Playwright: {e}")
        
        # Cleanup em caso de erro
        try:
            chrome_proc.terminate()
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
        
        return False

def test_credentials_system():
    """Testa o sistema de credenciais"""
    print("\n🔐 Testando sistema de credenciais...")
    
    try:
        # Tenta importar o sistema de credenciais
        sys.path.append(os.getcwd())
        from credentials.credentials import Credentials
        from credentials.message.msg_code import MsgCode
        
        print("   ✅ Módulos de credenciais importados")
        
        # Testa criação básica (sem salvar arquivos)
        creds = Credentials()
        print("   ✅ Instância de credenciais criada")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erro no sistema: {e}")
        return False

def create_chrome_launcher_script():
    """Cria script para iniciar Chrome debug facilmente"""
    print("\n📝 Criando script de inicialização do Chrome...")
    
    script_content = '''#!/bin/bash
# Script para iniciar Chrome em modo debug
# Gerado automaticamente pelo custom_setup.py

CHROME_DEBUG_PORT=9222
CHROME_PROFILE_DIR="$HOME/.config/chrome-debug-profile"

echo "🚀 Iniciando Chrome em modo debug..."
echo "   Porta: $CHROME_DEBUG_PORT"
echo "   Perfil: $CHROME_PROFILE_DIR"

# Cria diretório do perfil se não existir
mkdir -p "$CHROME_PROFILE_DIR"

# Mata processos Chrome existentes na porta debug
if lsof -Pi :$CHROME_DEBUG_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Processo usando porta $CHROME_DEBUG_PORT encontrado"
    echo "   Deseja matar? (s/N)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        pkill -f "chrome.*remote-debugging-port=$CHROME_DEBUG_PORT"
        sleep 2
    fi
fi

# Inicia Chrome
google-chrome-stable \\
    --remote-debugging-port=$CHROME_DEBUG_PORT \\
    --user-data-dir="$CHROME_PROFILE_DIR" \\
    --no-first-run \\
    --disable-web-security \\
    --disable-features=VizDisplayCompositor \\
    >/dev/null 2>&1 &

CHROME_PID=$!

echo "   PID do Chrome: $CHROME_PID"
echo "   ✅ Chrome iniciado!"
echo ""
echo "📋 Para verificar:"
echo "   curl http://localhost:$CHROME_DEBUG_PORT/json"
echo ""
echo "🛑 Para parar:"
echo "   kill $CHROME_PID"
echo "   ou: pkill -f 'chrome.*remote-debugging-port'"
'''
    
    script_path = Path("start_chrome_debug.sh")
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Torna executável
        os.chmod(script_path, 0o755)
        
        print(f"   ✅ Script criado: {script_path}")
        print("   💡 Execute: ./start_chrome_debug.sh")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar script: {e}")
        return False

def install_project():
    """Instala o projeto em modo desenvolvimento"""
    print("\n📦 Instalando projeto...")
    
    try:
        if Path("setup.py").exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", "."
            ], check=True, capture_output=True)
            print("✅ Projeto instalado em modo desenvolvimento")
            return True
        else:
            print("   ℹ️ setup.py não encontrado - pulando instalação")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def show_final_instructions(all_success, chrome_cmd=None):
    """Mostra instruções finais"""
    print("\n" + "="*60)
    
    if all_success:
        print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n✅ Ambiente pronto para o novo sistema!")
        print("\n📋 COMO USAR:")
        print("   1. Inicie o Chrome debug:")
        if chrome_cmd:
            print(f"      {chrome_cmd} --remote-debugging-port=9222 --user-data-dir='$HOME/.config/chrome-debug' &")
        print("      OU execute: ./start_chrome_debug.sh")
        print("")
        print("   2. Execute o programa principal:")
        print("      python main.py")
        print("")
        print("   3. Use os comandos de mouse configurados")
        print("")
        print("📊 DEPENDÊNCIAS INSTALADAS:")
        print("   ✅ Playwright (controle via CDP)")
        print("   ✅ PyNput (controle de mouse/teclado)")
        print("   ✅ Sistema de credenciais criptografado")
        print("   ✅ Google Chrome com modo debug")
        print("")
        print("🔧 DEPENDÊNCIAS REMOVIDAS:")
        print("   🗑️ Selenium (não é mais usado)")
        print("   🗑️ Fake-UserAgent (não é mais necessário)")
        
    else:
        print("⚠️  CONFIGURAÇÃO INCOMPLETA")
        print("="*60)
        print("\n❌ Alguns componentes apresentaram problemas")
        print("   Revise os erros acima e tente resolver os problemas")
        print("   Você pode executar este script novamente após as correções")
    
    print("\n📚 COMANDOS ÚTEIS:")
    print("   python main.py --identify    - Identificar botões do mouse")
    print("   ./start_chrome_debug.sh      - Iniciar Chrome debug")
    print("   check_cred                   - Verificar credenciais")
    print("   create_cred                  - Criar credenciais")
    print("="*60)

def main():
    """Função principal"""
    print_banner()
    
    try:
        # Informações do sistema
        system, arch, distro = get_system_info()
        
        # Lista de verificações
        checks = [
            ("Python", check_python_version),
            ("Ambiente Virtual", check_virtual_env),
            ("Dependências Sistema", lambda: install_system_dependencies(system, distro)),
            ("Google Chrome", lambda: install_google_chrome(system, arch)),
            ("Dependências Python", install_python_dependencies),
            ("Estrutura Projeto", create_project_structure),
            ("Importações", test_imports),
            ("Projeto", install_project),
            ("Chrome Debug", test_chrome_debug),
            ("Playwright CDP", test_playwright_cdp),
            ("Sistema Credenciais", test_credentials_system),
            ("Script Chrome", create_chrome_launcher_script)
        ]
        
        results = {}
        chrome_cmd = None
        
        for name, check_func in checks:
            print(f"\n🔍 {name}...")
            try:
                result = check_func()
                if isinstance(result, tuple):
                    success, extra = result
                    if name == "Google Chrome" and success:
                        chrome_cmd = extra
                    elif name == "Chrome Debug" and success:
                        chrome_cmd = extra
                    results[name] = success
                else:
                    results[name] = result
            except Exception as e:
                print(f"   ❌ Erro inesperado em {name}: {e}")
                results[name] = False
        
        # Resumo
        print("\n📊 RESUMO DOS TESTES:")
        print("-" * 30)
        success_count = 0
        for name, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {name}")
            if success:
                success_count += 1
        
        all_success = success_count >= len(results) - 2  # Tolera 2 falhas
        show_final_instructions(all_success, chrome_cmd)
        
        return 0 if all_success else 1
        
    except KeyboardInterrupt:
        print("\n\n🛑 Configuração cancelada pelo usuário")
        return 130
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        sys.exit(1)