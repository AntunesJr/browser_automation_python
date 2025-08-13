#!/usr/bin/env python3
#google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
#google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome"

# ==============================================
# I -> Imports.
# ==============================================

from browser.browser_cdp import BrowserCDP
import threading
import random
import time
import subprocess
import os
import sys
import signal
from pynput import mouse
import subprocess

# ==============================================
# Variáveis globais para controle - ATUALIZADAS
# ==============================================
active_browsers = []
running = True
voice_thread = None
voice_active = False
google_text = None
voice_lock = threading.Lock()

# Variável global para o browser PDV
pdv_browser = None
pdv_ready = False

# NOVO: Sistema de comunicação entre threads
command_queue = []
command_lock = threading.Lock()

# Configuração do botão do mouse
# Button.button8 = botão lateral 1 (voltar) - comum em mouses
# Button.button9 = botão lateral 2 (avançar) - comum em mouses
# Button.middle = botão do meio (scroll)
# Button.left = botão esquerdo
# Button.right = botão direito

# Por padrão, usar botão do meio (altere conforme necessário)
# Após identificar seus botões com --identify, você pode usar:
# mouse.Button.button8, mouse.Button.button9, etc.
VOICE_TRIGGER_BUTTON = mouse.Button.button8 #mouse.Button.middle  # Altere após identificar seus botões

# ==============================================
# II -> Classe para identificar botões do mouse
# ==============================================

class MouseButtonIdentifier:
    """Identifica qual botão do mouse está sendo pressionado"""
    
    @staticmethod
    def identify_buttons():
        """Modo de identificação de botões"""
        print("\n" + "="*60)
        print("🖱️  IDENTIFICADOR DE BOTÕES DO MOUSE")
        print("="*60)
        print("Clique em qualquer botão do mouse para identificá-lo")
        print("Pressione ESC no teclado para sair")
        print("-"*60)
        
        def on_click(x, y, button, pressed):
            if pressed:
                button_name = str(button).replace("Button.", "")
                print(f"✓ Botão detectado: {button_name}")
                print(f"  Posição: ({x}, {y})")
                print(f"  Código Python: mouse.Button.{button_name}")
                
                # Sugestões de uso
                if "button" in button_name.lower():
                    print(f"  💡 Use no código: VOICE_TRIGGER_BUTTON = mouse.Button.{button_name}")
                
                print("-"*60)
        
        def on_move(x, y):
            pass  # Ignorar movimento
        
        def on_scroll(x, y, dx, dy):
            print(f"✓ Scroll detectado: {'para cima' if dy > 0 else 'para baixo'}")
            print(f"  Posição: ({x}, {y})")
            print(f"  💡 Para usar scroll: Implemente on_scroll no listener")
            print("-"*60)
        
        # Listener do mouse
        with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
        ) as listener:
            try:
                # Listener do teclado para sair com ESC
                from pynput import keyboard
                
                def on_press(key):
                    if key == keyboard.Key.esc:
                        print("\n✅ Identificação concluída!")
                        print("\n📝 PRÓXIMOS PASSOS:")
                        print("1. Edite o arquivo e altere VOICE_TRIGGER_BUTTON")
                        print("2. Use o código Python mostrado acima")
                        print("3. Execute o programa normalmente")
                        listener.stop()
                        return False
                
                with keyboard.Listener(on_press=on_press) as kb_listener:
                    kb_listener.join()
                    
            except KeyboardInterrupt:
                print("\n✅ Identificação interrompida!")

# ==============================================
# NOVO: Sistema de Comunicação Entre Threads
# ==============================================

def send_command_to_pdv(command, data=None):
    """Envia comando para a thread PDV de forma thread-safe"""
    global command_queue, command_lock
    
    with command_lock:
        command_queue.append({
            'command': command,
            'data': data,
            'timestamp': time.time()
        })
    
    print(f"   📤 Comando '{command}' enviado para PDV")

def process_pdv_commands():
    """Processa comandos na thread PDV (thread-safe)"""
    global command_queue, command_lock, pdv_browser, pdv_ready, running
    
    with command_lock:
        commands_to_process = command_queue.copy()
        command_queue.clear()
    
    for cmd in commands_to_process:
        command = cmd['command']
        data = cmd['data']
        
        try:
            print(f"   📥 Processando comando PDV: '{command}'")
            
            if command == 'search_product':
                if pdv_browser and pdv_ready:
                    pdv_browser.fill_search_field_pdv(data, "pdv")
                    success = pdv_browser.next_pdv("pdv")
                    print(f"   ✅ Produto '{data}' inserido no campo de busca")
                
            elif command == 'login':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.login("pdv")
                    print(f"   ✅ Login {'realizado' if success else 'falhou'}")
                
            elif command == 'clear_search':
                if pdv_browser and pdv_ready:
                    pdv_browser.fill_search_field_pdv("", "pdv")
                    print("   ✅ Campo de busca limpo")
                
            elif command == 'reload_page':
                if pdv_browser and pdv_ready:
                    pdv_browser.access("https://app.gdoorweb.com.br/movimentos/pdv/nova", "pdv")
                    pdv_browser.bring_to_front("pdv")
                    print("   ✅ Página PDV recarregada")
                
            elif command == 'close_pdv':
                if pdv_browser and pdv_ready:
                    pdv_browser.close_tab("pdv")
                    pdv_ready = False
                    print("   ✅ PDV fechado")
                
            elif command == 'open_pdv':
                if pdv_browser:
                    pdv_browser.access("https://app.gdoorweb.com.br/movimentos/pdv/nova", "pdv")
                    pdv_browser.bring_to_front("pdv")
                    pdv_ready = True
                    print("   ✅ PDV aberto")
                
            elif command == 'close_other_tabs':
                if pdv_browser and pdv_ready:
                    pdv_browser.close_all_tabs_except("pdv")
                    print("   ✅ Outras abas fechadas")
                
            elif command == 'list_tabs':
                if pdv_browser:
                    pdv_browser.list_open_tabs()
                
            elif command == 'exit_program':
                print("   🚪 Encerrando programa via comando de voz...")
                running = False
                pdv_ready = False
            
            elif command == 'set_units':
                if pdv_browser and pdv_ready:
                    units = int(data)
                    success = pdv_browser.unit_pdv(units, "pdv")
                    print(f"   ✅ {units} unidades {'inseridas' if success else 'falha ao inserir'}")
                
            elif command == 'press_enter':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.enter_pdv("pdv")
                    print(f"   ✅ Enter {'pressionado' if success else 'falha ao pressionar'}")
                
            elif command == 'next_item':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.next_pdv("pdv")
                    print(f"   ✅ {'Navegou para próximo item' if success else 'Falha ao navegar'}")
                
            elif command == 'debit':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.debit_pdv("pdv")
                    print(f"   ✅ {'Venda concluída no débito.' if success else 'Falha ao concluir a venda.'}")

            elif command == 'credit':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.credit_pdv("pdv")
                    print(f"   ✅ {'Venda concluída no crédito.' if success else 'Falha ao concluir a venda.'}")

            elif command == 'pix':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.credit_pdv("pdv")
                    print(f"   ✅ {'Venda concluída no pix.' if success else 'Falha ao concluir a venda.'}")

            elif command == 'discount':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.discount_pdv("pdv")
                    print(f"   ✅ {'Aplicando desconto.' if success else 'Falha ao concluir a venda.'}")
            
            elif command == 'change_price_pdv':
                if pdv_browser and pdv_ready:
                    success = pdv_browser.change_price_pdv("pdv")
                    print(f"   ✅ {'Aplicando desconto.' if success else 'Falha ao concluir a venda.'}")

            elif command == 'shutdown':
                if pdv_browser and pdv_ready:
                    print(f"   ✅ {'Desligando o computador.' if success else 'Falha ao desligar o computador.'}")
                try:
                    pdv_browser.close()
                except:
                    pass
                pdv_ready = False
    
                # Chama a função de desligamento
                desligar_computador()
                
                # Encerra o programa
                running = False
                
        except Exception as e:
            print(f"   ❌ Erro ao processar comando '{command}': {e}")

def desligar_computador():
    """Desliga o computador com contagem regressiva"""
    try:
        print("\n" + "="*50)
        print("⚠️  DESLIGANDO O COMPUTADOR EM 10 SEGUNDOS!")
        print("    Pressione Ctrl+C para CANCELAR")
        print("="*50)
        
        # Contagem regressiva
        for i in range(10, 0, -1):
            print(f"    🕐 Desligando em {i} segundos...", end='\r')
            time.sleep(1)
        
        print("\n    🔌 Desligando AGORA...")
        
        # Tenta diferentes comandos de desligamento
        try:
            # Método 1: systemctl (mais moderno)
            subprocess.run(['systemctl', 'poweroff'])
        except:
            try:
                # Método 2: shutdown tradicional
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            except:
                # Método 3: poweroff direto
                subprocess.run(['sudo', 'poweroff'])
        
        return True
        
    except KeyboardInterrupt:
        print("\n    ✅ DESLIGAMENTO CANCELADO!")
        return False
    except Exception as e:
        print(f"\n    ❌ Erro ao desligar: {e}")
        return False

# ==============================================
# III -> Funções para controle do voice
# ==============================================

def initialize_connection():
    """Inicializa e testa a conexão CDP - apenas para verificação inicial"""
    print("\n🔄 Verificando conexão CDP...")
    
    test_browser = BrowserCDP()
    
    if not test_browser.connect():
        print("❌ O navegador Chrome não foi aberto em modo depuração.")
        print("\n📋 SOLUÇÕES PARA MANTER SEU PERFIL:")
        print("\n🔧 RECOMENDADO - Duas instâncias simultâneas:")
        print("   1. Mantenha seu Chrome normal aberto")
        print("   2. Execute em outro terminal:")
        print("      cp -r \"$HOME/.config/google-chrome\" \"$HOME/.config/google-chrome-debug\"")
        print("      google-chrome --remote-debugging-port=9222 --user-data-dir=\"$HOME/.config/google-chrome-debug\" &")
        return False
    
    print("✅ Conexão CDP disponível!")
    
    # Fechar conexão de teste
    try:
        test_browser.close()
    except:
        pass
    
    return True

def check_chrome_debug_and_start():
    """Verifica se Chrome debug está ativo e oferece opções para iniciar"""
    import requests
    import subprocess
    import os
    
    print("\n🔍 Verificando Chrome em modo debug...")
    
    try:
        response = requests.get("http://localhost:9222/json", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Chrome debug já está ativo com {len(data)} páginas")
            return True
    except:
        pass
    
    print("   ❌ Chrome debug não está ativo na porta 9222")
    print("\n🚀 Iniciando Chrome debug automaticamente...")
    
    # Verifica se perfil debug já existe
    debug_profile = os.path.expanduser("~/.config/google-chrome-debug")
    original_profile = os.path.expanduser("~/.config/google-chrome")
    
    try:
        # Se perfil debug não existe, cria copiando o original
        if not os.path.exists(debug_profile) and os.path.exists(original_profile):
            print(f"   📂 Criando perfil debug com suas configurações...")
            subprocess.run([
                "cp", "-r", original_profile, debug_profile
            ], check=True, capture_output=True)
            print(f"   ✅ Perfil copiado para {debug_profile}")
        
        # Inicia Chrome debug
        print("   🔧 Iniciando Chrome debug...")
        subprocess.Popen([
            "google-chrome",
            "--remote-debugging-port=9222",
            f"--user-data-dir={debug_profile}",
            "--no-first-run",
            "--disable-web-security"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Aguarda inicialização
        print("   ⏳ Aguardando Chrome inicializar...")
        for i in range(10):  # Tenta por 10 segundos
            time.sleep(1)
            try:
                response = requests.get("http://localhost:9222/json", timeout=1)
                if response.status_code == 200:
                    print(f"   ✅ Chrome debug ativo após {i+1} segundos")
                    return True
            except:
                continue
        
        print("   ⚠️ Chrome debug não respondeu dentro do tempo esperado")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao copiar perfil: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erro ao iniciar Chrome: {e}")
        return False

def auto_setup_chrome():
    """Configura Chrome automaticamente mantendo perfil do usuário"""
    print("\n🔧 CONFIGURAÇÃO AUTOMÁTICA DO CHROME")
    print("="*50)
    
    # Verifica se Chrome debug já está rodando
    if check_chrome_debug_and_start():
        return True
    
    print("\n❌ Não foi possível configurar Chrome automaticamente")
    print("\n📋 CONFIGURAÇÃO MANUAL:")
    print("1. Abra um novo terminal")
    print("2. Execute um dos comandos abaixo:")
    print("\n   # OPÇÃO 1 - Perfil separado (RECOMENDADO)")
    print("   cp -r ~/.config/google-chrome ~/.config/google-chrome-debug")
    print("   google-chrome --remote-debugging-port=9222 --user-data-dir=\"$HOME/.config/google-chrome-debug\" &")
    print("\n   # OPÇÃO 2 - Perfil temporário")  
    print("   google-chrome --remote-debugging-port=9222 --user-data-dir=\"/tmp/chrome-debug\" &")
    print("\n3. Execute o programa novamente")
    
    return False

def voice_thread_runner():
    """Thread runner para voice"""
    global voice_active
    voice_active = True
    voice_action()

def on_mouse_click(x, y, button, pressed):
    """Callback para cliques do mouse"""
    global voice_thread, voice_active, voice_lock
    
    # Converte button para string para comparação mais flexível
    button_str = str(button)
    trigger_str = str(VOICE_TRIGGER_BUTTON)
    
    if button_str == trigger_str and pressed:
        with voice_lock:
            if not voice_active:
                print(f"\n🖱️  Botão {button_str.replace('Button.', '')} pressionado - Iniciando voice...")
                
                # Cria e inicia nova thread para voice
                voice_thread = threading.Thread(target=voice_thread_runner, daemon=True)
                voice_thread.start()
            else:
                print(f"⚠️  Voice já está em execução, aguarde conclusão...")

def initialize_pdv_browser():
    """Inicializa e mantém o browser PDV em loop"""
    global pdv_browser, pdv_ready, running
    
    try:
        print("\n🏪 Inicializando browser PDV...")
        
        # Criar instância BrowserCDP para PDV
        pdv_browser = BrowserCDP()
        
        if not pdv_browser.connect():
            print("   ❌ Erro ao conectar com Chrome debug para PDV")
            return False
        
        print("   ✅ Conexão CDP estabelecida para PDV")
        
        # Acessar página PDV
        pdv_page = pdv_browser.access("https://app.gdoorweb.com.br/movimentos/pdv/nova", "pdv")
        pdv_browser.bring_to_front("pdv")
        print("   ✅ Página PDV acessada")
        
        # Verificar se precisa fazer login
        if not pdv_browser.url_search("movimentos/pdv/nova", "pdv"):
            print("   🔐 Fazendo login automático...")
            login_success = pdv_browser.login("pdv")
            if login_success:
                print("   ✅ Login realizado com sucesso!")
                time.sleep(3)
                
                if pdv_browser.url_search("movimentos/pdv/nova", "pdv"):
                    print("   ✅ PDV carregado corretamente após login!")
                else:
                    print("   ⚠️ PDV pode não ter carregado completamente, mas continuando...")
            else:
                print("   ❌ Falha no login, mas continuando...")
        else:
            print("   ✅ PDV já carregado, não precisa de login")
        
        pdv_ready = True
        print("   🎯 PDV pronto para comandos de voz!")
        
        # Loop principal com processamento de comandos
        while running and pdv_ready:
            time.sleep(2)  # Verifica a cada 2 segundos
            
            # NOVO: Processa comandos da fila
            process_pdv_commands()
            
            # Verifica status da página PDV
            try:
                pdv_page = pdv_browser.get_page("pdv")
                
                if pdv_page and not pdv_page.is_closed():
                    current_url = pdv_page.url
                    if "gdoorweb.com.br" in current_url:
                        # PDV está ok
                        pass
                    else:
                        print(f"   ⚠️ PDV mudou de URL: {current_url}")
                        pdv_browser.access("https://app.gdoorweb.com.br/movimentos/pdv/nova", "pdv")
                        pdv_browser.bring_to_front("pdv")
                else:
                    if pdv_ready:  # Só reconecta se ainda deveria estar ativo
                        print("   ⚠️ Página PDV foi fechada, reconectando...")
                        pdv_page = pdv_browser.access("https://app.gdoorweb.com.br/movimentos/pdv/nova", "pdv")
                        pdv_browser.bring_to_front("pdv")
                        print("   ✅ PDV reconectado!")
                    
            except Exception as e:
                if pdv_ready:  # Só tenta reconectar se ainda deveria estar ativo
                    print(f"   🔄 Erro no monitoramento PDV, tentando reconectar: {e}")
                    try:
                        pdv_page = pdv_browser.access("https://app.gdoorweb.com.br/movimentos/pdv/nova", "pdv")
                        pdv_browser.bring_to_front("pdv")
                        print("   ✅ PDV reconectado após erro!")
                    except Exception as e2:
                        print(f"   ❌ Erro crítico ao reconectar PDV: {e2}")
                        pdv_ready = False
                        break
        
        print("   📴 Loop de monitoramento PDV finalizado")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na inicialização do PDV: {e}")
        pdv_ready = False
        return False

def converter_numero_extenso(texto):
    """Converte número por extenso para inteiro"""
    numeros = {
        'zero': 0, 'um': 1, 'uma': 1, 'dois': 2, 'duas': 2,
        'três': 3, 'tres': 3, 'quatro': 4, 'cinco': 5,
        'seis': 6, 'sete': 7, 'oito': 8, 'nove': 9, 'dez': 10,
        'onze': 11, 'doze': 12, 'treze': 13, 'catorze': 14,
        'quinze': 15, 'dezesseis': 16, 'dezessete': 17,
        'dezoito': 18, 'dezenove': 19, 'vinte': 20,
        'trinta': 30, 'quarenta': 40, 'cinquenta': 50
    }
    
    texto_lower = texto.lower()
    
    # Verifica cada número no dicionário
    for palavra, numero in numeros.items():
        # Usa regex para garantir palavra completa
        if re.search(rf'\b{palavra}\b', texto_lower):
            return numero
    
    return None

def process_voice_command(command_text):
    """Processa comandos de voz e envia para thread PDV"""
    global pdv_ready, running
    
    if not pdv_ready:
        print("   ❌ PDV não está pronto para comandos")
        return False
    
    command_text = command_text.lower().strip()
    print(f"\n🎯 Processando comando: '{command_text}'")
    
    try:
        
        # 1. Tenta números em formato numeral (15 unidades)
        units_match = re.search(r'(\d+)\s*(?:unidades?|un\b)', command_text)
        if units_match:
            units = int(units_match.group(1))
            print(f"   🔢 Número detectado: {units}")
            send_command_to_pdv('set_units', units)
            return True
        
        # 2. Tenta números por extenso (duas unidades)
        elif re.search(r'\b(?:unidades?|un\b)', command_text):
            units = converter_numero_extenso(command_text)
            if units is not None:
                print(f"   🔢 Número por extenso convertido: {units}")
                send_command_to_pdv('set_units', units)
                return True
        
        # Comando: pesquisar [produto]
        elif re.search(r'\bpesquisar\b', command_text):
            product = remove_word(command_text, "pesquisar").strip()
            if product:
                print(f"   🔍 Enviando busca de produto: '{product}'")
                send_command_to_pdv('search_product', product)
                return True
            else:
                print("   ❌ Nenhum produto especificado para pesquisar")
                return False
        
        # Comando: login
        elif re.search(r'\blogin\b', command_text):
            print("   🔐 Enviando comando de login...")
            send_command_to_pdv('login')
            return True
        
        # Comando: limpar
        elif re.search(r'\blimpar\b', command_text):
            print("   🧹 Enviando comando para limpar campo...")
            send_command_to_pdv('clear_search')
            return True
        
        # Comando: recarregar
        elif re.search(r'\brecarregar\b', command_text):
            print("   🔄 Enviando comando para recarregar...")
            send_command_to_pdv('reload_page')
            return True
        
        # Comando: fechar pdv
        elif re.search(r'\bfechar pdv\b', command_text):
            print("   🗂️ Enviando comando para fechar PDV...")
            send_command_to_pdv('close_pdv')
            return True
        
        # Comando: abrir pdv
        elif re.search(r'\babrir pdv\b', command_text) or re.search(r'\babrir emissor de nota fiscal\b', command_text) or re.search(r'\bnova nota fiscal\b', command_text) or re.search(r'\bemitir nova nota fiscal\b', command_text):
            print("   🏪 Enviando comando para abrir PDV...")
            send_command_to_pdv('open_pdv')
            return True
        
        # Comando: fechar abas
        elif re.search(r'\bfechar abas\b', command_text):
            print("   🗂️ Enviando comando para fechar outras abas...")
            send_command_to_pdv('close_other_tabs')
            return True
        
        # Comando: listar abas
        elif re.search(r'\blistar abas\b', command_text):
            print("   📋 Enviando comando para listar abas...")
            send_command_to_pdv('list_tabs')
            return True
        
        # Comando: sair programa
        elif re.search(r'\bsair programa\b', command_text) or re.search(r'\bfechar programa\b', command_text):
            print("   🚪 Enviando comando para encerrar programa...")
            send_command_to_pdv('exit_program')
            return True
        
        # Comando: enter
        elif command_text.strip() == "enter" or command_text.strip() == "confirmar" or command_text.strip() == "adcionar":
            print("   ⏎ Enviando comando Enter...")
            send_command_to_pdv('press_enter')
            return True
        
        # Comando: próximo ou próxima
        elif re.search(r'\bpróxim[oa]?\b', command_text) or command_text.strip() == "baixo":
            print("   ⬇️ Enviando comando para próximo item...")
            send_command_to_pdv('next_item')
            return True
        
        # Comando: anterior ou voltar (extra)
        elif re.search(r'\banterior\b', command_text) or command_text.strip() == "cima" or command_text.strip() == "voltar":
            print("   ⬆️ Enviando comando para item anterior...")
            send_command_to_pdv('previous_item')
            return True
        
        elif re.search(r'\bpix\b', command_text):
            print("   ⬆️ Finalizando venda como pix...")
            send_command_to_pdv('credit')
            return True

        elif re.search(r'\bdébito\b', command_text) or command_text.strip() == "cartão de débito":
            print("   ⬆️ Finalizando venda como débito...")
            send_command_to_pdv('debit')
            return True

        elif re.search(r'\bcrédito\b', command_text) or command_text.strip() == "cartão de crédito":
            print("   ⬆️ Finalizando venda como crédito...")
            send_command_to_pdv('pix')
            return True
        
        elif re.search(r'\bdesconto\b', command_text) or command_text.strip() == "dar desconto":
            print("   ⬆️ Aplicando desconto...")
            send_command_to_pdv('discount')
            return True

        elif re.search(r'\bmudar preço\b', command_text) or command_text.strip() == "alterar preço":
            print("   ⬆️ mudando preço...")
            send_command_to_pdv('change_price')
            return True

        elif re.search(r'\bdesligar\b', command_text) or command_text.strip() == "desligar computador":
            print("   ⬆️ mudando preço...")
            send_command_to_pdv('shutdown')
            return True

        # Comando: ajuda
        elif re.search(r'\bpix\b', command_text):
            print("\n📖 COMANDOS DISPONÍVEIS:")
            print("   • 'X unidades' - Define X unidades do produto (ex: '10 unidades')")
            print("   • 'pesquisar [produto]' - Busca produto no PDV")
            print("   • 'enter' ou 'confirmar' - Pressiona Enter")
            print("   • 'próximo' ou 'baixo' - Navega para próximo item")
            print("   • 'anterior' ou 'cima' - Navega para item anterior")
            print("   • 'login' - Faz login no sistema")
            print("   • 'limpar' - Limpa campo de busca")
            print("   • 'recarregar' - Recarrega página PDV")
            print("   • 'fechar pdv' - Fecha aba do PDV")
            print("   • 'abrir pdv' - Abre/recarrega aba do PDV")
            print("   • 'fechar abas' - Fecha outras abas (exceto PDV)")
            print("   • 'listar abas' - Mostra abas abertas")
            print("   • 'sair programa' - Encerra o programa")
            print("   • 'fechar programa' - Encerra o programa")
            print("   • 'ajuda' - Mostra esta lista")
            return True
        
        else:
            print(f"   ❓ Comando não reconhecido: '{command_text}'")
            print("   💡 Diga 'ajuda' para ver comandos disponíveis")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao processar comando: {e}")
        return False

def voice_action():
    """Executa a ação de voice quando ativada - SIMPLIFICADA"""
    global voice_active, google_text
    
    try:
        print("\n" + "="*40)
        print("🎤 VOICE ATIVADO VIA BOTÃO DO MOUSE")
        print("="*40)
        
        # Criar nova instância BrowserCDP apenas para o Google
        voice_browser = BrowserCDP()
        
        if not voice_browser.connect():
            print("   ❌ Erro ao conectar com Chrome debug nesta thread")
            return
        
        print("   ✅ Conexão CDP estabelecida para esta thread")
        
        # Encontrar ou acessar página do Google
        try:
            google_page = voice_browser.access("https://www.google.com/", "google")
            voice_browser.bring_to_front("google")
            print("   ✅ Página do Google acessada")
        except Exception as e:
            print(f"   ⚠️ Erro ao acessar Google: {e}")
            return
        
        # Executar sequência de voice no Google
        try:
            voice_browser.google_microphone()
            print("   → Microfone do Google ativado")
            time.sleep(10)  # Aguarda gravação
            
            google_text = voice_browser.read_google_search_field()
            print(f"   ✓ Texto capturado: '{google_text}'")
            
            # Processar comando de voz no PDV
            if google_text and google_text.strip():
                process_voice_command(google_text)
            else:
                print("   ⚠️ Nenhum comando capturado")
                
        except Exception as e:
            print(f"   ❌ Erro durante operação de voice: {e}")
        
        # CORREÇÃO: Fechar APENAS o browser do Google, NÃO o PDV
        try:
            # Fecha apenas a aba do Google neste browser específico
            voice_browser.close_tab("google")
            # Fecha apenas este browser (não afeta o PDV que está em outro browser)
            voice_browser.close()
            print("   ✅ Browser do Google fechado (PDV mantido)")
        except Exception as e:
            print(f"   ⚠️ Erro ao fechar Google: {e}")
        
        print("="*40)
        print("✅ COMANDO DE VOZ PROCESSADO")
        print("="*40 + "\n")
        
    except Exception as e:
        print(f"❌ Erro na execução do voice: {e}")
    
    finally:
        voice_active = False
# ==============================================
# IV -> Funções originais adaptadas
# ==============================================

def cleanup_browsers():
    """Fecha todos os browsers ativos - ATUALIZADA"""
    global active_browsers, pdv_browser, pdv_ready
    print("\n🔄 Encerrando todos os browsers...")
    
    # Fecha PDV browser se existir
    if pdv_browser:
        try:
            pdv_browser.close()
        except:
            pass
    
    pdv_ready = False
    
    for browser in active_browsers:
        try:
            browser.close()
        except:
            pass
    
    active_browsers.clear()
    print("✅ Todos os browsers foram fechados!")

def signal_handler(signum, frame):
    """Handler para sinais do sistema (Ctrl+C)"""
    global running
    running = False
    cleanup_browsers()
    sys.exit(0)

def input_monitor():
    """Monitora input do usuário para encerramento"""
    global running
    try:
        button_name = str(VOICE_TRIGGER_BUTTON).replace("Button.", "").upper()
        
        print("\n" + "="*60)
        print("🚀 AUTOMAÇÃO DE BROWSERS INICIADA")
        print("="*60)
        print(f"🖱️  Botão configurado para VOICE: {button_name}")
        print("💡 Pressione ENTER para encerrar o programa")
        print("💡 Ou use Ctrl+C para encerramento forçado")
        print("="*60 + "\n")
        
        input()  # Aguarda o usuário pressionar Enter
        
        print("\n🛑 Solicitação de encerramento recebida...")
        running = False
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupção detectada...")
        running = False

import re

def remove_word(texto, palavra):
    padrao = r'\b{}\b'.format(re.escape(palavra))
    resultado = re.sub(padrao, '', texto)
    # Remove espaços extras resultantes
    resultado = re.sub(r'\s+', ' ', resultado).strip()
    # Corrige espaços antes de pontuação
    resultado = re.sub(r'\s+([.,;!?])', r'\1', resultado)
    return resultado

    

# ==============================================
# V -> Main modificado
# ==============================================

def main():
    global running
    
    auto_setup_chrome()

    # Configurar handler para sinais
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🔧 Iniciando sistema de automação...")
    
    # Verificar se deve identificar botões
    if len(sys.argv) > 1 and sys.argv[1] == "--identify":
        MouseButtonIdentifier.identify_buttons()
        return
    
    # Lista para armazenar threads
    threads = []
    
    try:
        # Tenta inicializar conexão CDP
        print("🔍 Verificando conexão Chrome debug...")
        chrome_ready = initialize_connection()
        
        if not chrome_ready:
            print("\n⚠️ Chrome debug não está pronto.")
            print("💡 Configure o Chrome debug primeiro.")
            return
        
        # Inicia thread do PDV
        print("🏪 Iniciando thread PDV...")
        pdv_thread = threading.Thread(target=initialize_pdv_browser, daemon=True)
        pdv_thread.start()
        threads.append(pdv_thread)
        
        # Aguarda PDV ficar pronto
        print("   ⏳ Aguardando PDV ficar pronto...")
        for i in range(30):  # Aguarda até 30 segundos
            if pdv_ready:
                break
            time.sleep(1)
        
        if not pdv_ready:
            print("   ❌ PDV não ficou pronto a tempo")
            return
        
        # Inicia listener do mouse
        mouse_listener = mouse.Listener(on_click=on_mouse_click)
        mouse_listener.start()
        print(f"🖱️  Listener do mouse ativo - Botão {VOICE_TRIGGER_BUTTON} configurado para voice")
        
        # Thread para monitorar input do usuário
        input_thread = threading.Thread(target=input_monitor, daemon=True)
        input_thread.start()
        threads.append(input_thread)
        time.sleep(0.1)
        
        print("\n" + "="*60)
        print("🚀 SISTEMA DE MENU DE VOZ ATIVO")
        print("="*60)
        print("🎤 Pressione o botão do mouse para ativar comandos de voz")
        print("💡 Comandos disponíveis: pesquisar, login, limpar, ajuda")
        print("🏪 PDV rodando em background - sempre pronto!")
        print("="*60 + "\n")
        
        # Loop principal - manter programa rodando
        while running:
            time.sleep(1)
            
            # Verificar se threads ainda estão ativas
            active_threads = [t for t in threads if t.is_alive()]
            
            if len(active_threads) == 0:
                print("⚠️ Todas as threads finalizaram.")
                break
        
        # Para o listener do mouse
        mouse_listener.stop()
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupção detectada no main...")
        running = False
    
    except Exception as e:
        print(f"❌ Erro crítico no main: {str(e)}")
        running = False
    
    finally:
        # Cleanup final
        running = False
        cleanup_browsers()
        
        print("\n" + "="*60)
        print("✨ PROGRAMA FINALIZADO COM SUCESSO")
        print("="*60)

# ==============================================
# VI -> Utilitário para configurar botões no LXQT
# ==============================================

def setup_mouse_buttons_lxqt():
    """Configura botões do mouse no LXQT"""
    print("\n" + "="*60)
    print("🔧 CONFIGURAÇÃO DE BOTÕES DO MOUSE NO LXQT")
    print("="*60)
    
    print("\n📝 Para configurar botões extras do mouse no LXQT:")
    print("\n1. Instale as ferramentas necessárias:")
    print("   sudo apt-get install xinput xbindkeys xbindkeys-config")
    
    print("\n2. Liste seus dispositivos de entrada:")
    print("   xinput list")
    
    print("\n3. Teste os botões do mouse:")
    print("   xev | grep -i button")
    
    print("\n4. Configure o xbindkeys (~/.xbindkeysrc):")
    print("""
# Exemplo de configuração para botão lateral 1 (button 8)
"python3 /caminho/para/seu/script.py --trigger-voice"
    b:8

# Exemplo para botão lateral 2 (button 9)
"python3 /caminho/para/seu/script.py --trigger-voice"
    b:9
""")
    
    print("\n5. Recarregue o xbindkeys:")
    print("   killall xbindkeys && xbindkeys")
    
    print("\n6. Para iniciar xbindkeys automaticamente, adicione ao autostart do LXQT:")
    print("   Menu → Preferências → Sessão do LXQt → Autostart")
    print("   Adicione: xbindkeys")
    
    print("\n" + "="*60)

# ==============================================
# VII -> Handle PyInstaller executable path
# ==============================================

if __name__ == "__main__":
    try:
        # Verifica argumentos de linha de comando
        if "--setup" in sys.argv:
            setup_mouse_buttons_lxqt()
            sys.exit(0)
        
        if "--identify" in sys.argv:
            MouseButtonIdentifier.identify_buttons()
            sys.exit(0)
        
        if "--trigger-voice" in sys.argv:
            # Modo trigger único - executa voice uma vez e sai
            initialize_voice_connection()
            voice_action()
            sys.exit(0)
        
        # No início do main(), adicione:
        if "--auto-setup" in sys.argv:
            auto_setup_chrome()
            sys.exit(0)

        # Instalação do pynput se necessário
        try:
            import pynput
        except ImportError:
            print("❌ Biblioteca pynput não encontrada!")
            print("📦 Instale com: pip install pynput")
            print("\nNo Debian/Ubuntu, você também pode precisar de:")
            print("   sudo apt-get install python3-tk python3-dev")
            sys.exit(1)
        
        if getattr(sys, 'frozen', False):
            os.chdir(sys._MEIPASS)
        
        main()
        
    except Exception as e:
        print(f"❌ Erro fatal: {str(e)}")
        input("Pressione Enter para sair...")

'''
# Crie uma cópia do seu perfil para debug (uma vez só)
cp -r "$HOME/.config/google-chrome" "$HOME/.config/google-chrome-debug"

# Inicie Chrome debug (mantenha seu Chrome normal aberto)
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome-debug" --no-first-run &
'''