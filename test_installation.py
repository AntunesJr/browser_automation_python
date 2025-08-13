#!/usr/bin/env python3
"""
Script de verificação pós-instalação
Testa se todas as dependências estão funcionando corretamente
"""

import sys
import subprocess
import time
import tempfile
import shutil
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print('='*60)

def test_python_imports():
    """Testa todas as importações Python necessárias"""
    print("\n📦 Testando importações Python...")
    
    imports_to_test = [
        ("playwright", "Playwright base"),
        ("playwright.sync_api", "Playwright Sync API"),
        ("pynput", "PyNput base"), 
        ("pynput.mouse", "PyNput Mouse"),
        ("pynput.keyboard", "PyNput Keyboard"),
        ("cryptography", "Cryptography"),
        ("cryptography.fernet", "Cryptography Fernet"),
        ("requests", "Requests"),
        ("psutil", "PSUtil"),
        ("threading", "Threading"),
        ("subprocess", "Subprocess"),
        ("pathlib", "PathLib"),
        ("json", "JSON"),
        ("time", "Time"),
        ("os", "OS"),
        ("sys", "Sys")
    ]
    
    success_count = 0
    failed_imports = []
    
    for module_name, display_name in imports_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name}")
            success_count += 1
        except ImportError as e:
            print(f"   ❌ {display_name}: {e}")
            failed_imports.append((module_name, str(e)))
    
    print(f"\n   📊 Resultado: {success_count}/{len(imports_to_test)} importações bem-sucedidas")
    
    if failed_imports:
        print("\n   ❌ Importações falharam:")
        for module, error in failed_imports:
            print(f"      • {module}: {error}")
    
    return len(failed_imports) == 0

def test_chrome_installation():
    """Testa se o Chrome está instalado e funcionando"""
    print("\n🌐 Testando instalação do Google Chrome...")
    
    chrome_commands = [
        "google-chrome-stable",
        "google-chrome",
        "/usr/bin/google-chrome-stable", 
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    working_commands = []
    
    for cmd in chrome_commands:
        try:
            result = subprocess.run(
                [cmd, "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ {cmd}: {version}")
                working_commands.append(cmd)
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
            continue
    
    if working_commands:
        print(f"\n   📊 {len(working_commands)} comando(s) Chrome funcionando")
        return True, working_commands[0]
    else:
        print("   ❌ Nenhum comando Chrome encontrado")
        return False, None

def test_chrome_debug_mode(chrome_cmd):
    """Testa se o Chrome pode ser iniciado em modo debug"""
    print("\n🔧 Testando Chrome em modo debug...")
    
    if not chrome_cmd:
        print("   ❌ Comando Chrome não disponível")
        return False
    
    # Cria diretório temporário
    temp_dir = tempfile.mkdtemp(prefix="chrome-test-")
    test_port = 9225  # Porta diferente para não conflitar
    
    try:
        print(f"   🚀 Iniciando Chrome na porta {test_port}...")
        
        # Inicia Chrome
        proc = subprocess.Popen([
            chrome_cmd,
            f"--remote-debugging-port={test_port}",
            f"--user-data-dir={temp_dir}",
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Aguarda inicialização
        print("   ⏳ Aguardando inicialização...")
        time.sleep(4)
        
        # Testa conexão CDP
        try:
            import requests
            response = requests.get(f"http://localhost:{test_port}/json", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ CDP funcionando - {len(data)} páginas detectadas")
                success = True
            else:
                print(f"   ❌ CDP retornou status {response.status_code}")
                success = False
                
        except Exception as e:
            print(f"   ❌ Erro ao conectar via CDP: {e}")
            success = False
        
        # Mata processo
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        
        return success
        
    except Exception as e:
        print(f"   ❌ Erro ao iniciar Chrome: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

def test_playwright_installation():
    """Testa se o Playwright está instalado corretamente"""
    print("\n🎭 Testando Playwright...")
    
    try:
        from playwright.sync_api import sync_playwright
        print("   ✅ Playwright sync_api importado")
        
        # Testa se consegue iniciar (sem conectar a nada)
        with sync_playwright() as p:
            print("   ✅ Playwright context criado")
            
            # Verifica browsers disponíveis
            browsers = []
            try:
                chromium = p.chromium
                browsers.append("chromium")
            except:
                pass
            
            try:
                firefox = p.firefox
                browsers.append("firefox")
            except:
                pass
            
            print(f"   ✅ Browsers disponíveis: {', '.join(browsers) if browsers else 'Nenhum'}")
            
            if not browsers:
                print("   ⚠️ Nenhum browser Playwright encontrado")
                print("   💡 Execute: python -m playwright install")
                return False
            
            return True
            
    except ImportError as e:
        print(f"   ❌ Erro ao importar Playwright: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erro no Playwright: {e}")
        return False

def test_playwright_cdp_integration(chrome_cmd):
    """Testa integração Playwright + Chrome CDP"""
    print("\n🔗 Testando integração Playwright + Chrome CDP...")
    
    if not chrome_cmd:
        print("   ❌ Chrome não disponível")
        return False
    
    temp_dir = tempfile.mkdtemp(prefix="playwright-cdp-test-")
    test_port = 9226
    
    chrome_proc = None
    try:
        # Inicia Chrome
        print("   🚀 Iniciando Chrome para CDP...")
        chrome_proc = subprocess.Popen([
            chrome_cmd,
            f"--remote-debugging-port={test_port}",
            f"--user-data-dir={temp_dir}",
            "--headless",
            "--no-sandbox"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(3)
        
        # Testa Playwright
        print("   🎭 Conectando Playwright via CDP...")
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://localhost:{test_port}")
            
            # Cria contexto e página
            if browser.contexts:
                context = browser.contexts[0]
            else:
                context = browser.new_context()
            
            page = context.new_page()
            
            # Navega para página teste
            test_html = "data:text/html,<html><head><title>Teste CDP</title></head><body><h1>Sucesso!</h1></body></html>"
            page.goto(test_html)
            
            # Verifica resultado
            title = page.title()
            content = page.locator("h1").inner_text()
            
            print(f"   ✅ Página carregada - Título: '{title}'")
            print(f"   ✅ Conteúdo: '{content}'")
            
            # Testa JavaScript
            js_result = page.evaluate("() => navigator.userAgent")
            print(f"   ✅ JavaScript executado - UserAgent detectado")
            
            browser.close()
            
            return True
    
    except Exception as e:
        print(f"   ❌ Erro na integração: {e}")
        return False
    
    finally:
        # Cleanup
        if chrome_proc:
            try:
                chrome_proc.terminate()
                chrome_proc.wait(timeout=5)
            except:
                chrome_proc.kill()
        
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

def test_credentials_system():
    """Testa o sistema de credenciais"""
    print("\n🔐 Testando sistema de credenciais...")
    
    try:
        # Adiciona diretório atual ao path
        current_dir = Path.cwd()
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        # Tenta importar módulos
        from credentials.credentials import Credentials
        from credentials.message.msg_code import MsgCode
        from credentials.message.msg_handler import MessageHandler
        print("   ✅ Módulos de credenciais importados")
        
        # Testa criação de instância
        creds = Credentials()
        print("   ✅ Instância Credentials criada")
        
        # Testa verificação básica (sem criar arquivos)
        try:
            status = creds.checker()
            print(f"   ✅ Método checker executado (retornou: {type(status)})")
        except Exception as e:
            print(f"   ⚠️ Erro no checker (esperado se não houver credenciais): {e}")
        
        # Testa MessageHandler
        try:
            msg = MessageHandler.get(0)  # Código de sucesso
            print(f"   ✅ MessageHandler funcionando: '{msg}'")
        except Exception as e:
            print(f"   ❌ Erro no MessageHandler: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro de importação: {e}")
        print("   💡 Verifique se os módulos credentials estão no diretório")
        return False
    except Exception as e:
        print(f"   ❌ Erro geral: {e}")
        return False

def test_mouse_control():
    """Testa controle básico do mouse"""
    print("\n🖱️ Testando controle do mouse...")
    
    try:
        from pynput import mouse
        from pynput.mouse import Button, Listener
        print("   ✅ PyNput mouse importado")
        
        # Testa detecção de posição
        current_pos = mouse.position
        print(f"   ✅ Posição atual do mouse: {current_pos}")
        
        # Testa tipos de botão disponíveis
        buttons = [Button.left, Button.right, Button.middle]
        
        # Verifica botões especiais se disponíveis
        try:
            buttons.extend([Button.button8, Button.button9])
        except AttributeError:
            pass
        
        print(f"   ✅ Botões detectados: {[str(b).replace('Button.', '') for b in buttons]}")
        
        # Testa criação de listener (sem iniciar)
        def dummy_click(x, y, button, pressed):
            pass
        
        listener = Listener(on_click=dummy_click)
        print("   ✅ Mouse listener criado (não iniciado)")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro ao importar pynput: {e}")
        print("   💡 Instale com: pip install pynput")
        return False
    except Exception as e:
        print(f"   ❌ Erro no teste mouse: {e}")
        return False

def test_project_structure():
    """Verifica estrutura do projeto"""
    print("\n📁 Verificando estrutura do projeto...")
    
    required_files = [
        "main.py",
        "browser/browser_cdp.py",
        "browser/__init__.py",
        "credentials/credentials.py",
        "credentials/__init__.py",
        "credentials/message/msg_code.py",
        "credentials/message/msg_handler.py"
    ]
    
    optional_files = [
        "requirements.txt",
        "custom_setup.py",
        "start_chrome_debug.sh"
    ]
    
    missing_required = []
    missing_optional = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_required.append(file_path)
    
    for file_path in optional_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   - {file_path} (opcional)")
            missing_optional.append(file_path)
    
    if missing_required:
        print(f"\n   ❌ Arquivos obrigatórios faltando: {len(missing_required)}")
        for file in missing_required:
            print(f"      • {file}")
        return False
    else:
        print(f"\n   ✅ Todos os arquivos obrigatórios presentes")
        return True

def run_comprehensive_test():
    """Executa todos os testes"""
    print_header("VERIFICAÇÃO COMPLETA DA INSTALAÇÃO")
    
    tests = [
        ("Importações Python", test_python_imports),
        ("Instalação Chrome", test_chrome_installation),
        ("Playwright", test_playwright_installation),
        ("Sistema de Credenciais", test_credentials_system),
        ("Controle Mouse", test_mouse_control),
        ("Estrutura Projeto", test_project_structure)
    ]
    
    results = {}
    chrome_cmd = None
    
    # Executa testes básicos
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            if isinstance(result, tuple):
                success, extra = result
                if test_name == "Instalação Chrome":
                    chrome_cmd = extra
                results[test_name] = success
            else:
                results[test_name] = result
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")
            results[test_name] = False
    
    # Testes que dependem do Chrome
    if chrome_cmd:
        advanced_tests = [
            ("Chrome Debug Mode", lambda: test_chrome_debug_mode(chrome_cmd)),
            ("Playwright + CDP", lambda: test_playwright_cdp_integration(chrome_cmd))
        ]
        
        for test_name, test_func in advanced_tests:
            print(f"\n--- {test_name} ---")
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"   ❌ Erro inesperado: {e}")
                results[test_name] = False
    
    # Relatório final
    print_header("RELATÓRIO FINAL")
    
    passed_tests = []
    failed_tests = []
    
    for test_name, success in results.items():
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"   {status} {test_name}")
        
        if success:
            passed_tests.append(test_name)
        else:
            failed_tests.append(test_name)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   ✅ Passaram: {len(passed_tests)}")
    print(f"   ❌ Falharam: {len(failed_tests)}")
    print(f"   📈 Taxa de sucesso: {len(passed_tests)/len(results)*100:.1f}%")
    
    if len(passed_tests) >= len(results) * 0.8:  # 80% ou mais
        print("\n🎉 INSTALAÇÃO APROVADA!")
        print("✅ Seu ambiente está pronto para usar o sistema")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Execute: ./start_chrome_debug.sh")
        print("   2. Execute: python main.py")
        print("   3. Use os comandos de mouse configurados")
    else:
        print("\n⚠️ INSTALAÇÃO PRECISA DE AJUSTES")
        print("❌ Alguns componentes não estão funcionando")
        print("\n🔧 PROBLEMAS DETECTADOS:")
        for test in failed_tests:
            print(f"   • {test}")
        print("\n💡 SOLUÇÕES:")
        print("   • Execute novamente: python custom_setup.py")
        print("   • Verifique as mensagens de erro acima")
        print("   • Instale dependências manualmente se necessário")

if __name__ == "__main__":
    try:
        run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n\n🛑 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro crítico durante teste: {e}")
        sys.exit(1)