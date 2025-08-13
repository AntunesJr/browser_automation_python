#!/usr/bin/env python3
"""
Módulo de Automação CDP - Google e ChatGPT Voice Control
Autor: Browser Automation
Descrição: Controla microfone do Google e ChatGPT via CDP
"""

from playwright.sync_api import sync_playwright
import time
import sys

class CDPBrowserController:
    """Controlador de navegador via Chrome DevTools Protocol"""
    
    def __init__(self, debug_port=9222):
        self.debug_port = debug_port
        self.playwright = None
        self.browser = None
        self.context = None
        self.google_page = None
        self.chatgpt_page = None
    
    def connect(self):
        """Conecta ao Chrome já aberto com debugging habilitado"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.connect_over_cdp(f"http://localhost:{self.debug_port}")
            self.context = self.browser.contexts[0]
            
            # Aplica anti-detecção em todas as páginas
            for page in self.context.pages:
                self._apply_stealth(page)
            
            print(f"✅ Conectado ao Chrome via CDP na porta {self.debug_port}")
            print(f"   Contextos: {len(self.browser.contexts)}")
            print(f"   Páginas abertas: {len(self.context.pages)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def _apply_stealth(self, page):
        """Aplica scripts anti-detecção na página"""
        page.add_init_script("""
            // Remove webdriver flag
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Chrome runtime
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            
            // Permissions API fix
            const originalQuery = window.navigator.permissions.query;
            if (originalQuery) {
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            }
        """)
    
    def find_or_open_google(self):
        """Encontra ou abre a aba do Google"""
        print("\n🔍 Procurando aba do Google...")
        
        # Procura por aba existente do Google
        for page in self.context.pages:
            if "google.com" in page.url:
                self.google_page = page
                print(f"   ✓ Aba do Google encontrada: {page.title}")
                page.bring_to_front()
                return page
        
        # Se não encontrou, abre nova aba
        print("   → Abrindo nova aba do Google...")
        self.google_page = self.context.new_page()
        self._apply_stealth(self.google_page)
        self.google_page.goto("https://www.google.com", wait_until="networkidle")
        print(f"   ✓ Google aberto: {self.google_page.title}")
        return self.google_page
    
    def click_google_microphone(self):
        """Clica no botão de microfone do Google"""
        print("\n🎤 Ativando microfone do Google...")
        
        if not self.google_page:
            print("   ❌ Página do Google não encontrada")
            return False
        
        try:
            # Garante que estamos na página do Google
            self.google_page.bring_to_front()
            
            # Procura o botão do microfone por diferentes seletores
            selectors = [
                'svg.goxjub',  # Classe do SVG
                'svg[viewBox="0 -960 960 960"]',  # ViewBox específico
                'div[aria-label*="voice" i]',  # Aria label com "voice"
                'div[aria-label*="voz" i]',  # Aria label em português
                'div[aria-label*="microfone" i]',  # Aria label microfone
                'button[aria-label*="voice" i]',  # Botão com aria-label
                'div.XDyW0e',  # Classe do container do microfone
            ]
            
            clicked = False
            for selector in selectors:
                if self.google_page.locator(selector).count() > 0:
                    self.google_page.locator(selector).first.click()
                    print(f"   ✓ Microfone ativado usando seletor: {selector}")
                    clicked = True
                    break
            
            if not clicked:
                print("   ⚠ Botão do microfone não encontrado, tentando método alternativo...")
                # Tenta clicar por coordenadas aproximadas (geralmente à direita da barra de pesquisa)
                search_box = self.google_page.locator('textarea[name="q"], input[name="q"]').first
                if search_box:
                    box = search_box.bounding_box()
                    if box:
                        # Clica à direita da caixa de pesquisa onde geralmente fica o microfone
                        self.google_page.mouse.click(box['x'] + box['width'] + 30, box['y'] + box['height']/2)
                        print("   ✓ Tentativa de clique por posição relativa")
                        clicked = True
            
            time.sleep(2)  # Aguarda ativação do microfone
            return clicked
            
        except Exception as e:
            print(f"   ❌ Erro ao clicar no microfone: {e}")
            return False
    
    def read_google_search_field(self):
        """Lê o texto do campo de pesquisa do Google"""
        print("\n📖 Lendo campo de pesquisa do Google...")
        
        if not self.google_page:
            print("   ❌ Página do Google não encontrada")
            return None
        
        try:
            # Procura o campo de pesquisa
            selectors = [
                'textarea[name="q"]',  # Textarea moderna
                'input[name="q"]',     # Input clássico
                'textarea.gLFyf',      # Classe específica
                '#APjFqb'              # ID específico
            ]
            
            for selector in selectors:
                element = self.google_page.locator(selector).first
                if element:
                    text = element.input_value()
                    print(f"   ✓ Texto encontrado: '{text}'")
                    return text
            
            print("   ⚠ Campo de pesquisa vazio ou não encontrado")
            return ""
            
        except Exception as e:
            print(f"   ❌ Erro ao ler campo: {e}")
            return None
    
    def find_or_open_chatgpt(self):
        """Encontra ou abre a aba do ChatGPT"""
        print("\n🤖 Procurando aba do ChatGPT...")
        
        # Procura por aba existente do ChatGPT
        for page in self.context.pages:
            if "chatgpt.com" in page.url or "chat.openai.com" in page.url:
                self.chatgpt_page = page
                print(f"   ✓ Aba do ChatGPT encontrada: {page.title}")
                page.bring_to_front()
                return page
        
        # Se não encontrou, abre nova aba
        print("   → Abrindo nova aba do ChatGPT...")
        self.chatgpt_page = self.context.new_page()
        self._apply_stealth(self.chatgpt_page)
        self.chatgpt_page.goto("https://chatgpt.com/", wait_until="networkidle")
        print(f"   ✓ ChatGPT aberto: {self.chatgpt_page.title}")
        time.sleep(5)  # Aguarda carregamento completo
        return self.chatgpt_page
    
    def click_chatgpt_dictation(self):
        """Clica no botão de ditado do ChatGPT"""
        print("\n🎙️ Ativando ditado do ChatGPT...")
        
        if not self.chatgpt_page:
            print("   ❌ Página do ChatGPT não encontrada")
            return False
        
        try:
            self.chatgpt_page.bring_to_front()
            
            # Seletores para o botão de ditado
            selectors = [
                'button[aria-label*="ditado" i]',
                'button[aria-label*="dictation" i]',
                'button[aria-label*="voice" i]',
                'button.composer-btn svg[viewBox="0 0 20 20"]',
                'button:has(svg path[d*="M15.7806"])',  # Path específico do SVG
            ]
            
            for selector in selectors:
                if self.chatgpt_page.locator(selector).count() > 0:
                    self.chatgpt_page.locator(selector).first.click()
                    print(f"   ✓ Ditado ativado usando: {selector}")
                    return True
            
            print("   ⚠ Botão de ditado não encontrado")
            return False
            
        except Exception as e:
            print(f"   ❌ Erro ao ativar ditado: {e}")
            return False
    
    def stop_chatgpt_dictation(self):
        """Para o ditado e envia no ChatGPT"""
        print("\n⏹️ Parando ditado do ChatGPT...")
        
        if not self.chatgpt_page:
            return False
        
        try:
            # Primeiro tenta clicar no botão de parar
            stop_selectors = [
                'button[aria-label*="Interromper" i]',
                'button[aria-label*="Stop" i]',
                'button:has(svg path[d*="M14.2548"])',  # Path do X
            ]
            
            for selector in stop_selectors:
                if self.chatgpt_page.locator(selector).count() > 0:
                    self.chatgpt_page.locator(selector).first.click()
                    print("   ✓ Ditado interrompido")
                    time.sleep(1)
                    break
            
            # Depois clica em enviar
            send_selectors = [
                'button[aria-label*="Enviar" i]',
                'button[aria-label*="Send" i]',
                'button:has(svg path[d*="M15.4835"])',  # Path do checkmark
            ]
            
            for selector in send_selectors:
                if self.chatgpt_page.locator(selector).count() > 0:
                    self.chatgpt_page.locator(selector).first.click()
                    print("   ✓ Mensagem enviada")
                    return True
            
            return False
            
        except Exception as e:
            print(f"   ❌ Erro ao parar ditado: {e}")
            return False
    
    def read_chatgpt_field(self):
        """Lê o texto do campo do ChatGPT"""
        print("\n📝 Lendo campo do ChatGPT...")
        
        if not self.chatgpt_page:
            print("   ❌ Página do ChatGPT não encontrada")
            return None
        
        try:
            # Seletores para o campo de texto
            selectors = [
                'div#prompt-textarea',
                'div.ProseMirror',
                'div[contenteditable="true"]',
                'div[data-placeholder*="Pergunte" i]',
            ]
            
            for selector in selectors:
                element = self.chatgpt_page.locator(selector).first
                if element:
                    text = element.inner_text()
                    if text and text.strip():
                        print(f"   ✓ Texto encontrado: '{text}'")
                        return text
            
            print("   ⚠ Campo vazio ou não encontrado")
            return ""
            
        except Exception as e:
            print(f"   ❌ Erro ao ler campo: {e}")
            return None
    
    def clear_chatgpt_field(self):
        """Limpa o campo de texto do ChatGPT"""
        print("\n🧹 Limpando campo do ChatGPT...")
        
        if not self.chatgpt_page:
            return False
        
        try:
            # Foca no campo
            field = self.chatgpt_page.locator('div#prompt-textarea, div.ProseMirror').first
            if field:
                field.click()
                # Seleciona tudo e deleta
                self.chatgpt_page.keyboard.press("Control+A")
                self.chatgpt_page.keyboard.press("Delete")
                print("   ✓ Campo limpo")
                return True
            
            print("   ⚠ Campo não encontrado")
            return False
            
        except Exception as e:
            print(f"   ❌ Erro ao limpar campo: {e}")
            return False
    
    def switch_to_google(self):
        """Volta para a aba do Google"""
        print("\n↩️ Voltando para o Google...")
        
        if self.google_page:
            self.google_page.bring_to_front()
            print("   ✓ Aba do Google ativada")
            return True
        
        print("   ❌ Aba do Google não encontrada")
        return False
    
    def disconnect(self):
        """Desconecta do navegador"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("\n👋 Desconectado do navegador")
    
    def run_full_automation(self):
        """Executa a automação completa conforme solicitado"""
        print("\n" + "="*60)
        print("🚀 INICIANDO AUTOMAÇÃO COMPLETA")
        print("="*60)
        
        try:
            # 1. Conecta ao navegador
            if not self.connect():
                return False
            
            # 2. Abre/encontra Google
            self.find_or_open_google()
            
            # 3. Clica no microfone do Google
            self.click_google_microphone()
            
            # 4. Lê o campo de pesquisa do Google
            google_text = self.read_google_search_field()
            print(f"\n📌 TEXTO DO GOOGLE: '{google_text}'")
            '''
            # 5. Abre/encontra ChatGPT
            self.find_or_open_chatgpt()
            
            # 6. Clica no botão de ditado
            if self.click_chatgpt_dictation():
                # 7. Espera 10 segundos
                print("\n⏳ Aguardando 10 segundos...")
                for i in range(10, 0, -1):
                    print(f"   {i}...", end="", flush=True)
                    time.sleep(1)
                print()
                
                # 8. Para o ditado e envia
                self.stop_chatgpt_dictation()
            
            # 9. Lê o campo do ChatGPT
            chatgpt_text = self.read_chatgpt_field()
            print(f"\n📌 TEXTO DO CHATGPT: '{chatgpt_text}'")
            
            # 10. Limpa o campo do ChatGPT
            self.clear_chatgpt_field()
            
            # 11. Volta para o Google
            self.switch_to_google()
            '''
            print("\n" + "="*60)
            print("✅ AUTOMAÇÃO COMPLETA FINALIZADA COM SUCESSO!")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erro durante automação: {e}")
            return False
        
        finally:
            # Mantém conexão aberta para uso posterior se necessário
            # self.disconnect()
            pass

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     CDP Browser Controller - Google & ChatGPT Voice      ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("⚠️  PREPARAÇÃO NECESSÁRIA:")
    print("1. Abra o Chrome com: google-chrome --remote-debugging-port=9222 --user-data-dir='$HOME/chrome-debug-profile'")
    print("2. Faça login no Google e ChatGPT se necessário")
    print("3. Execute este script\n")
    
    controller = CDPBrowserController()
    
    # Menu de opções
    print("Escolha uma opção:")
    print("1. Executar automação completa")
    print("2. Testar conexão apenas")
    print("3. Controle manual passo a passo")
    
    choice = input("\nOpção: ").strip()
    
    if choice == "1":
        controller.run_full_automation()
    
    elif choice == "2":
        if controller.connect():
            print("✅ Conexão bem sucedida!")
            controller.disconnect()
    
    elif choice == "3":
        if controller.connect():
            print("\nComandos disponíveis:")
            print("  g  - Abrir/ir para Google")
            print("  m  - Clicar microfone Google")
            print("  r  - Ler campo Google")
            print("  c  - Abrir/ir para ChatGPT")
            print("  d  - Ativar ditado ChatGPT")
            print("  s  - Parar ditado ChatGPT")
            print("  t  - Ler texto ChatGPT")
            print("  l  - Limpar campo ChatGPT")
            print("  b  - Voltar para Google")
            print("  q  - Sair\n")
            
            while True:
                cmd = input("Comando: ").strip().lower()
                
                if cmd == 'g':
                    controller.find_or_open_google()
                elif cmd == 'm':
                    controller.click_google_microphone()
                elif cmd == 'r':
                    controller.read_google_search_field()
                elif cmd == 'c':
                    controller.find_or_open_chatgpt()
                elif cmd == 'd':
                    controller.click_chatgpt_dictation()
                elif cmd == 's':
                    controller.stop_chatgpt_dictation()
                elif cmd == 't':
                    controller.read_chatgpt_field()
                elif cmd == 'l':
                    controller.clear_chatgpt_field()
                elif cmd == 'b':
                    controller.switch_to_google()
                elif cmd == 'q':
                    break
                else:
                    print("Comando inválido!")
            
            controller.disconnect()
    
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()