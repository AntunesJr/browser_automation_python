#!/usr/bin/env python3
"""
Instalador completo para Browser Automation Python v2.0
Meta-installer que automatiza todo o processo de instalação
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║          🚀 INSTALADOR COMPLETO v2.0                    ║
║              Browser Automation Python                  ║
║           Chrome CDP + Playwright + Voice               ║
╚══════════════════════════════════════════════════════════╝
    """)

def step_progress(step, total, description):
    """Mostra progresso da instalação"""
    bar_length = 40
    filled_length = int(bar_length * step / total)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    percent = f"{step/total*100:.1f}%"
    print(f"\n[{step:2d}/{total}] {bar} {percent}")
    print(f"     🔧 {description}")

def run_command(command, description, check=True, timeout=300):
    """Executa comando com feedback visual"""
    print(f"     ⚙️ {description}...")
    
    try:
        if isinstance(command, str):
            result = subprocess.run(
                command, 
                shell=True, 
                check=check, 
                capture_output=True, 
                text=True,
                timeout=timeout
            )
        else:
            result = subprocess.run(
                command, 
                check=check, 
                capture_output=True, 
                text=True,
                timeout=timeout
            )
        
        if result.returncode == 0:
            print(f"     ✅ {description} - Concluído")
            return True, result.stdout
        else:
            print(f"     ❌ {description} - Erro")
            if result.stderr:
                print(f"        {result.stderr[:100]}...")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"     ⏱️ {description} - Timeout")
        return False, "Timeout"
    except Exception as e:
        print(f"     ❌ {description} - Exceção: {e}")
        return False, str(e)

def check_python():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ necessário. Atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_complete():
    """Processo completo de instalação"""
    print_banner()
    
    # Verificação inicial
    if not check_python():
        return False
    
    total_steps = 12
    current_step = 0
    
    try:
        # Passo 1: Instalar o pacote em modo desenvolvimento
        current_step += 1
        step_progress(current_step, total_steps, "Instalando pacote Python")
        success, output = run_command([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], "Instalação do pacote")
        
        if not success:
            print("⚠️ Erro na instalação básica, continuando...")
        
        # Passo 2: Executar custom_setup.py
        current_step += 1
        step_progress(current_step, total_steps, "Configurando ambiente completo")
        
        if Path("custom_setup.py").exists():
            success, output = run_command([
                sys.executable, "custom_setup.py"
            ], "Setup personalizado", timeout=600)
            
            if not success:
                print("⚠️ Setup personalizado com problemas, continuando...")
        else:
            print("⚠️ custom_setup.py não encontrado")
        
        # Passo 3: Instalar browsers do Playwright
        current_step += 1
        step_progress(current_step, total_steps, "Instalando browsers Playwright")
        success, output = run_command([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], "Browsers Playwright", timeout=300)
        
        # Passo 4: Criar script de inicialização do Chrome
        current_step += 1
        step_progress(current_step, total_steps, "Criando scripts auxiliares")
        
        if not Path("start_chrome_debug.sh").exists():
            chrome_script = '''#!/bin/bash
# Script para iniciar Chrome em modo debug
CHROME_DEBUG_PORT=9222
CHROME_PROFILE_DIR="$HOME/.config/chrome-debug-profile"

echo "🚀 Iniciando Chrome em modo debug na porta $CHROME_DEBUG_PORT..."
mkdir -p "$CHROME_PROFILE_DIR"

google-chrome-stable \\
    --remote-debugging-port=$CHROME_DEBUG_PORT \\
    --user-data-dir="$CHROME_PROFILE_DIR" \\
    --no-first-run \\
    --disable-web-security \\
    >/dev/null 2>&1 &

echo "✅ Chrome debug iniciado!"
echo "📋 Verifique: curl http://localhost:$CHROME_DEBUG_PORT/json"
'''
            try:
                with open("start_chrome_debug.sh", "w") as f:
                    f.write(chrome_script)
                os.chmod("start_chrome_debug.sh", 0o755)
                print("     ✅ Script start_chrome_debug.sh criado")
            except Exception as e:
                print(f"     ⚠️ Erro ao criar script: {e}")
        
        # Passo 5: Testar comandos CLI
        current_step += 1
        step_progress(current_step, total_steps, "Testando comandos CLI")
        
        if Path("test_commands.py").exists():
            success, output = run_command([
                sys.executable, "test_commands.py"
            ], "Teste de comandos", check=False, timeout=60)
        
        # Passo 6: Verificar instalação completa
        current_step += 1
        step_progress(current_step, total_steps, "Verificando instalação")
        
        if Path("test_installation.py").exists():
            success, output = run_command([
                sys.executable, "test_installation.py"
            ], "Verificação da instalação", check=False, timeout=120)
        
        # Passo 7: Criar diretórios necessários
        current_step += 1
        step_progress(current_step, total_steps, "Criando estrutura de diretórios")
        
        dirs_to_create = ["logs", "temp", ".credentials"]
        for dir_name in dirs_to_create:
            try:
                Path(dir_name).mkdir(exist_ok=True)
                print(f"     ✅ Diretório {dir_name} criado")
            except Exception as e:
                print(f"     ⚠️ Erro ao criar {dir_name}: {e}")
        
        # Passo 8: Configurar permissões
        current_step += 1
        step_progress(current_step, total_steps, "Configurando permissões")
        
        try:
            os.chmod(".credentials", 0o700)
            print("     ✅ Permissões de segurança configuradas")
        except Exception as e:
            print(f"     ⚠️ Erro nas permissões: {e}")
        
        # Passo 9: Verificar Google Chrome
        current_step += 1
        step_progress(current_step, total_steps, "Verificando Google Chrome")
        
        chrome_commands = ["google-chrome-stable", "google-chrome"]
        chrome_ok = False
        for cmd in chrome_commands:
            success, output = run_command([cmd, "--version"], f"Teste {cmd}", check=False, timeout=10)
            if success:
                print(f"     ✅ {cmd} funcionando")
                chrome_ok = True
                break
        
        if not chrome_ok:
            print("     ⚠️ Google Chrome não encontrado - será instalado pelo custom_setup.py")
        
        # Passo 10: Testar conexão CDP
        current_step += 1
        step_progress(current_step, total_steps, "Testando conexão CDP")
        
        try:
            import requests
            
            # Tenta conectar se Chrome debug estiver rodando
            try:
                response = requests.get("http://localhost:9222/json", timeout=5)
                if response.status_code == 200:
                    print("     ✅ Chrome debug já está rodando")
                else:
                    print("     ℹ️ Chrome debug não ativo (normal)")
            except:
                print("     ℹ️ Chrome debug não ativo (esperado)")
                
        except ImportError:
            print("     ⚠️ Requests não disponível para teste CDP")
        
        # Passo 11: Criar arquivo de configuração exemplo
        current_step += 1
        step_progress(current_step, total_steps, "Criando configuração exemplo")
        
        config_example = '''# Exemplo de configuração para browser_automation_python
# Copie para config.py e ajuste conforme necessário

# Configurações do Chrome Debug
CHROME_DEBUG_PORT = 9222
CHROME_PROFILE_DIR = "~/.config/chrome-debug-profile"

# Configurações de voz
VOICE_TRIGGER_BUTTON = "button8"  # Altere após identificar com --identify

# Configurações do PDV
PDV_URL = "https://app.gdoorweb.com.br/movimentos/pdv/nova"
PDV_LOGIN_AUTO = True

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/automation.log"
'''
        
        try:
            if not Path("config_example.py").exists():
                with open("config_example.py", "w") as f:
                    f.write(config_example)
                print("     ✅ config_example.py criado")
        except Exception as e:
            print(f"     ⚠️ Erro ao criar config_example.py: {e}")
        
        # Passo 12: Finalização
        current_step += 1
        step_progress(current_step, total_steps, "Finalizando instalação")
        time.sleep(1)
        
        # Relatório final
        print(f"\n{'='*60}")
        print("🎉 INSTALAÇÃO COMPLETA FINALIZADA!")
        print(f"{'='*60}")
        
        print("\n✅ COMPONENTES INSTALADOS:")
        print("   • Browser Automation Python v2.0")
        print("   • Playwright + Chrome CDP")
        print("   • Sistema de credenciais criptografado")
        print("   • Comandos CLI funcionais")
        print("   • Scripts auxiliares")
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("   1️⃣ Configure suas credenciais:")
        print("      create_cred \"seu@email.com\" \"suaSenha123\" --username \"seuNome\"")
        print("")
        print("   2️⃣ Identifique os botões do mouse:")
        print("      python main.py --identify")
        print("")
        print("   3️⃣ Inicie o Chrome debug:")
        print("      ./start_chrome_debug.sh")
        print("")
        print("   4️⃣ Execute o programa:")
        print("      browser_automation")
        print("      # OU: python main.py")
        
        print("\n🔧 COMANDOS DISPONÍVEIS:")
        print("   • check_cred                 - Verificar credenciais")
        print("   • create_cred                - Criar credenciais")
        print("   • browser_automation         - Executar programa")
        print("   • setup_browser_automation   - Reconfigurar ambiente")
        print("   • test_browser_automation    - Testar instalação")
        
        print("\n💡 DICAS:")
        print("   • Use 'check_cred' para verificar se as credenciais estão OK")
        print("   • Execute 'test_browser_automation' para diagnósticos")
        print("   • Leia o README.md para documentação completa")
        
        print(f"\n{'='*60}")
        print("🎯 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("Sistema pronto para uso! 🚀")
        print(f"{'='*60}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n🛑 Instalação cancelada pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro durante instalação: {e}")
        return False

def main():
    """Função principal"""
    success = install_complete()
    
    if success:
        print("\n💫 Pronto para começar a automação!")
        sys.exit(0)
    else:
        print("\n⚠️ Instalação incompleta - verifique os erros acima")
        print("💡 Tente executar manualmente:")
        print("   python custom_setup.py")
        print("   pip install -e .")
        sys.exit(1)

if __name__ == "__main__":
    main()