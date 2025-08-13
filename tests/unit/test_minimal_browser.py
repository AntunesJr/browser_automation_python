#!/usr/bin/env python3

# ==============================================
# TESTE MÍNIMO - Diagnóstico de Problemas
# ==============================================

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TestMinimal')

def test_firefox_basic():
    """Teste básico do Firefox sem configurações especiais"""
    logger.info("🧪 Teste 1: Firefox básico (sem stealth)")
    
    try:
        # Configuração mínima
        options = Options()
        options.add_argument("--no-sandbox")
        
        # Serviço silencioso
        service = Service(log_path=os.devnull)
        
        logger.info("🔧 Inicializando Firefox básico...")
        driver = webdriver.Firefox(options=options, service=service)
        
        logger.info("🌐 Acessando Google...")
        driver.get("https://www.google.com")
        
        # Executar script stealth
        driver.execute_script(stealth_script)
        
        time.sleep(5)
        
        logger.info(f"✅ URL atual: {driver.current_url}")
        logger.info(f"✅ Título: {driver.title}")
        
        # Verificar webdriver property
        result = driver.execute_script("return navigator.webdriver;")
        logger.info(f"🔍 navigator.webdriver após stealth: {result}")
        
        # Verificar se funciona
        current_url = driver.current_url
        if "google.com" in current_url and "automationcontrolled" not in current_url:
            logger.info("✅ Stealth mínimo funcionou!")
        else:
            logger.warning(f"⚠️ Possível problema detectado: {current_url}")
        
        driver.quit()
        logger.info("✅ Teste 2 concluído")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no teste stealth mínimo: {str(e)}")
        return False

def test_geckodriver():
    """Testa se o geckodriver está funcionando"""
    logger.info("🧪 Teste 0: Verificando geckodriver")
    
    try:
        import subprocess
        result = subprocess.run(["geckodriver", "--version"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            logger.info(f"✅ {version}")
            return True
        else:
            logger.error("❌ geckodriver não responde corretamente")
            return False
            
    except FileNotFoundError:
        logger.error("❌ geckodriver não encontrado no PATH")
        return False
    except subprocess.TimeoutExpired:
        logger.error("❌ geckodriver timeout")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao testar geckodriver: {str(e)}")
        return False

def test_firefox_installation():
    """Testa se o Firefox está instalado"""
    logger.info("🧪 Verificando instalação do Firefox")
    
    firefox_paths = [
        "/usr/bin/firefox",
        "/usr/local/bin/firefox", 
        "/snap/bin/firefox",
        "/opt/firefox/firefox"
    ]
    
    for path in firefox_paths:
        if os.path.exists(path):
            logger.info(f"✅ Firefox encontrado: {path}")
            return True
    
    logger.error("❌ Firefox não encontrado nos caminhos padrão")
    return False

def diagnose_timeout_issue():
    """Diagnóstica problemas de timeout"""
    logger.info("🔍 Diagnóstico de timeout...")
    
    # Verificar processos firefox
    try:
        import subprocess
        result = subprocess.run(["pgrep", "-f", "firefox"], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            logger.warning("⚠️ Processos Firefox já em execução:")
            for pid in result.stdout.strip().split('\n'):
                logger.warning(f"   PID: {pid}")
            
            logger.info("💡 Tente matar os processos: pkill -f firefox")
        else:
            logger.info("✅ Nenhum processo Firefox encontrado")
            
    except Exception as e:
        logger.error(f"Erro ao verificar processos: {str(e)}")
    
    # Verificar permissões de /tmp
    try:
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            logger.info(f"✅ /tmp acessível: {tmp.name}")
    except Exception as e:
        logger.error(f"❌ Problema com /tmp: {str(e)}")
    
    # Verificar variáveis de ambiente
    display = os.environ.get('DISPLAY')
    logger.info(f"🖥️ DISPLAY: {display or 'não definido'}")
    
    if not display:
        logger.warning("⚠️ DISPLAY não definido - isso pode causar problemas")
        logger.info("💡 Tente: export DISPLAY=:0")

def run_all_tests():
    """Executa todos os testes de diagnóstico"""
    logger.info("🚀 Iniciando diagnóstico completo...")
    logger.info("=" * 50)
    
    tests = [
        ("Geckodriver", test_geckodriver),
        ("Firefox Installation", test_firefox_installation), 
        ("Firefox Basic", test_firefox_basic),
        ("Firefox Stealth Minimal", test_firefox_stealth_minimal)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"❌ {test_name} falhou: {str(e)}")
            results[test_name] = False
    
    # Diagnóstico adicional se houver falhas
    if not all(results.values()):
        logger.info("\n--- Diagnóstico de Problemas ---")
        diagnose_timeout_issue()
    
    # Relatório final
    logger.info("\n" + "=" * 50)
    logger.info("📊 RELATÓRIO FINAL:")
    logger.info("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        logger.info(f"{test_name}: {status}")
    
    if all(results.values()):
        logger.info("\n🎉 TODOS OS TESTES PASSARAM!")
        logger.info("✅ Seu ambiente está funcionando corretamente")
        logger.info("💡 Você pode usar o browser_stable.py com confiança")
    else:
        failed_tests = [name for name, passed in results.items() if not passed]
        logger.info(f"\n⚠️ {len(failed_tests)} teste(s) falharam:")
        for test in failed_tests:
            logger.info(f"   • {test}")
        
        logger.info("\n💡 SOLUÇÕES SUGERIDAS:")
        if not results.get("Geckodriver", True):
            logger.info("• Instale geckodriver: sudo apt install firefox-geckodriver")
        if not results.get("Firefox Installation", True):
            logger.info("• Instale Firefox: sudo apt install firefox")
        if not results.get("Firefox Basic", True):
            logger.info("• Verifique se há conflitos de versão ou permissões")
            logger.info("• Tente: pkill -f firefox && pkill -f geckodriver")
        if not results.get("Firefox Stealth Minimal", True):
            logger.info("• Use o browser_stable.py que tem melhor tratamento de erros")

if __name__ == "__main__":
    run_all_tests()
        
        time.sleep(6)
        
        logger.info(f"✅ URL atual: {driver.current_url}")
        logger.info(f"✅ Título: {driver.title}")
        
        # Verificar se aparece "automationcontrolled"
        current_url = driver.current_url
        if "google.com" in current_url:
            logger.info("✅ Acesso ao Google funcionou!")
        else:
            logger.warning(f"⚠️ URL inesperada: {current_url}")
        
        # Testar execução de JavaScript
        result = driver.execute_script("return navigator.webdriver;")
        logger.info(f"🔍 navigator.webdriver: {result}")
        
        driver.quit()
        logger.info("✅ Teste 1 concluído")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no teste básico: {str(e)}")
        return False

def test_firefox_stealth_minimal():
    """Teste com stealth mínimo"""
    logger.info("🧪 Teste 2: Firefox com stealth mínimo")
    
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        
        # Apenas as configurações mais essenciais
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        
        service = Service(log_path=os.devnull)
        
        logger.info("🔧 Inicializando Firefox com stealth mínimo...")
        driver = webdriver.Firefox(options=options, service=service)
        
        # Script stealth ultra-simples
        stealth_script = '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        '''
        
        logger.info("🌐 Acessando Google...")
        driver.get("https://www.google.com")