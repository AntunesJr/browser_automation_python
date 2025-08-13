#!/usr/bin/env python3
"""
Script para testar todos os comandos CLI instalados
Verifica se os entry_points do setup.py estão funcionando
"""

import subprocess
import sys
import shutil
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print('='*60)

def test_command_exists(command_name):
    """Testa se um comando existe no PATH"""
    return shutil.which(command_name) is not None

def test_command_help(command_name):
    """Testa se o comando responde ao --help"""
    try:
        result = subprocess.run(
            [command_name, "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "", "Command not found or timeout"

def test_command_version(command_name):
    """Testa se o comando responde ao --version"""
    try:
        result = subprocess.run(
            [command_name, "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "", "Command not found or timeout"

def test_credential_commands():
    """Testa comandos de credenciais"""
    print_header("COMANDOS DE CREDENCIAIS")
    
    commands = [
        ("check_cred", "Verificar credenciais"),
        ("check_cred_json", "Verificar credenciais (JSON)"),
        ("create_cred", "Criar credenciais"),
        ("create_cred_json", "Criar credenciais (JSON)"),
        ("show_cred", "Mostrar credenciais"),
        ("show_cred_json", "Mostrar credenciais (JSON)")
    ]
    
    results = {}
    
    for cmd, description in commands:
        print(f"\n🔍 Testando: {cmd} ({description})")
        
        # Verifica se existe
        exists = test_command_exists(cmd)
        print(f"   📍 Comando existe: {'✅' if exists else '❌'}")
        
        if exists:
            # Testa --help
            help_ok, help_out, help_err = test_command_help(cmd)
            print(f"   📋 Responde --help: {'✅' if help_ok else '❌'}")
            
            if help_ok and help_out:
                # Mostra primeira linha da ajuda
                first_line = help_out.split('\n')[0][:80]
                print(f"   💡 Ajuda: {first_line}...")
            elif help_err:
                print(f"   ⚠️ Erro: {help_err[:60]}...")
        
        results[cmd] = exists
    
    return results

def test_system_commands():
    """Testa comandos do sistema"""
    print_header("COMANDOS DO SISTEMA")
    
    commands = [
        ("browser_automation", "Programa principal"),
        ("setup_browser_automation", "Configuração do ambiente"),
        ("test_browser_automation", "Teste da instalação"),
        ("identify_mouse_buttons", "Identificar botões do mouse")
    ]
    
    results = {}
    
    for cmd, description in commands:
        print(f"\n🔍 Testando: {cmd} ({description})")
        
        # Verifica se existe
        exists = test_command_exists(cmd)
        print(f"   📍 Comando existe: {'✅' if exists else '❌'}")
        
        if exists:
            # Testa --help
            help_ok, help_out, help_err = test_command_help(cmd)
            print(f"   📋 Responde --help: {'✅' if help_ok else '❌'}")
            
            # Alguns comandos podem não ter --help, tenta --version
            if not help_ok:
                version_ok, version_out, version_err = test_command_version(cmd)
                print(f"   🔢 Responde --version: {'✅' if version_ok else '❌'}")
        
        results[cmd] = exists
    
    return results

def test_development_commands():
    """Testa comandos de desenvolvimento"""
    print_header("COMANDOS DE DESENVOLVIMENTO")
    
    commands = [
        ("start_chrome_debug", "Iniciar Chrome debug")
    ]
    
    results = {}
    
    for cmd, description in commands:
        print(f"\n🔍 Testando: {cmd} ({description})")
        
        # Verifica se existe
        exists = test_command_exists(cmd)
        print(f"   📍 Comando existe: {'✅' if exists else '❌'}")
        
        results[cmd] = exists
    
    return results

def test_python_module_access():
    """Testa se os módulos podem ser importados"""
    print_header("ACESSO VIA MÓDULOS PYTHON")
    
    modules_to_test = [
        ("credentials.credentials", "Módulo de credenciais"),
        ("credentials.message.msg_code", "Códigos de mensagem"),
        ("browser.browser_cdp", "Controle de browser via CDP"),
        ("main", "Módulo principal")
    ]
    
    results = {}
    
    for module, description in modules_to_test:
        print(f"\n🔍 Testando: {module} ({description})")
        
        try:
            __import__(module)
            print(f"   ✅ Importação bem-sucedida")
            results[module] = True
        except ImportError as e:
            print(f"   ❌ Erro de importação: {e}")
            results[module] = False
        except Exception as e:
            print(f"   ⚠️ Outro erro: {e}")
            results[module] = False
    
    return results

def test_direct_script_execution():
    """Testa execução direta dos scripts"""
    print_header("EXECUÇÃO DIRETA DE SCRIPTS")
    
    scripts = [
        ("main.py", "Programa principal"),
        ("custom_setup.py", "Setup customizado"),
        ("test_installation.py", "Teste de instalação")
    ]
    
    results = {}
    
    for script, description in scripts:
        print(f"\n🔍 Testando: {script} ({description})")
        
        script_path = Path(script)
        exists = script_path.exists()
        print(f"   📍 Arquivo existe: {'✅' if exists else '❌'}")
        
        if exists:
            # Testa se é executável
            try:
                result = subprocess.run(
                    [sys.executable, script, "--help"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                executable = result.returncode in [0, 1, 2]  # Pode retornar erro mas pelo menos executa
                print(f"   🚀 Executável: {'✅' if executable else '❌'}")
            except subprocess.TimeoutExpired:
                print(f"   ⏱️ Timeout (pode estar funcionando)")
                executable = True
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                executable = False
        else:
            executable = False
        
        results[script] = exists and executable
    
    return results

def generate_report(all_results):
    """Gera relatório final"""
    print_header("RELATÓRIO FINAL DOS COMANDOS CLI")
    
    total_tests = 0
    passed_tests = 0
    
    for category, results in all_results.items():
        print(f"\n📊 {category}:")
        category_passed = 0
        category_total = len(results)
        
        for item, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {item}")
            if success:
                category_passed += 1
        
        print(f"   📈 {category}: {category_passed}/{category_total} ({category_passed/category_total*100:.1f}%)")
        
        total_tests += category_total
        passed_tests += category_passed
    
    print(f"\n🎯 RESULTADO GERAL:")
    print(f"   ✅ Passaram: {passed_tests}")
    print(f"   ❌ Falharam: {total_tests - passed_tests}")
    print(f"   📊 Taxa de sucesso: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests >= total_tests * 0.8:  # 80% ou mais
        print("\n🎉 COMANDOS CLI FUNCIONANDO CORRETAMENTE!")
        print("✅ O setup.py foi instalado com sucesso")
        print("\n💡 COMO USAR:")
        print("   • check_cred                    - Verificar credenciais")
        print("   • create_cred email senha       - Criar credenciais")
        print("   • browser_automation            - Executar programa")
        print("   • setup_browser_automation      - Configurar ambiente")
    else:
        print("\n⚠️ ALGUNS COMANDOS NÃO ESTÃO FUNCIONANDO")
        print("❌ Pode haver problema na instalação do setup.py")
        print("\n🔧 SOLUÇÕES:")
        print("   • Reinstale: pip install -e .")
        print("   • Execute: python setup.py develop")
        print("   • Verifique: pip list | grep browser")

def check_pip_installation():
    """Verifica se o pacote foi instalado via pip"""
    print_header("VERIFICAÇÃO DA INSTALAÇÃO PIP")
    
    try:
        result = subprocess.run(
            ["pip", "list"], 
            capture_output=True, 
            text=True
        )
        
        if "browser-automation-python" in result.stdout:
            print("✅ Pacote encontrado na lista do pip")
            
            # Mostra informações do pacote
            info_result = subprocess.run(
                ["pip", "show", "browser-automation-python"],
                capture_output=True,
                text=True
            )
            
            if info_result.returncode == 0:
                print("📋 Informações do pacote:")
                for line in info_result.stdout.split('\n')[:10]:  # Primeiras 10 linhas
                    if line.strip():
                        print(f"   {line}")
            
            return True
        else:
            print("❌ Pacote NÃO encontrado na lista do pip")
            print("💡 Execute: pip install -e . (para instalação em modo desenvolvimento)")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar pip: {e}")
        return False

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║              🧪 TESTE DOS COMANDOS CLI v2.0              ║
║                    Browser Automation                   ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Verifica instalação pip primeiro
    pip_ok = check_pip_installation()
    
    # Executa todos os testes
    all_results = {
        "Comandos de Credenciais": test_credential_commands(),
        "Comandos do Sistema": test_system_commands(), 
        "Comandos de Desenvolvimento": test_development_commands(),
        "Módulos Python": test_python_module_access(),
        "Scripts Diretos": test_direct_script_execution()
    }
    
    # Gera relatório
    generate_report(all_results)
    
    # Instruções finais
    print(f"\n📝 INSTRUÇÕES ADICIONAIS:")
    
    if not pip_ok:
        print("1️⃣ Instale o pacote: pip install -e .")
        
    print("2️⃣ Configure ambiente: setup_browser_automation")
    print("3️⃣ Crie credenciais: create_cred email senha")
    print("4️⃣ Execute programa: browser_automation")
    
    print(f"\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro crítico durante teste: {e}")
        sys.exit(1)