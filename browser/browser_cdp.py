from playwright.sync_api import sync_playwright
import time
import sys

from credentials.credentials import Credentials


class BrowserCDP:
    """Controlador de navegador via Chrome DevTools Protocol"""
    
    def __init__(self, debug_port=9222):
        self.debug_port = debug_port
        self.playwright = None
        self.browser = None
        self.context = None
        self.tab_page = None
        self.pages = {}  # Dicionário para armazenar páginas por nome
        self.creds = Credentials()
        self.status, self.data = self.creds.load_credentials()

    def _apply_stealth(self, page):
        """Aplica técnicas de evasão para evitar detecção (exemplo básico)"""
        # Exemplo de injeção de JS para remover propriedades do navegador
        js_script = """
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
        """
        page.add_init_script(js_script)
        
    def connect(self):
        """Conecta ao Chrome já aberto com debugging habilitado"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.connect_over_cdp(f"http://localhost:{self.debug_port}")
            
            # Obtém o contexto principal
            if len(self.browser.contexts) == 0:
                self.context = self.browser.new_context()
            else:
                self.context = self.browser.contexts[0]
            
            # Aplica anti-detecção em todas as páginas existentes
            for page in self.context.pages:
                self._apply_stealth(page)
            
            print(f"✅ Conectado ao Chrome via CDP na porta {self.debug_port}")
            print(f"   Contextos: {len(self.browser.contexts)}")
            print(f"   Páginas abertas: {len(self.context.pages)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {str(e)}", file=sys.stderr)
            return False

    def access(self, url: str, page_name: str = None):
        """Encontra ou abre a aba com a URL especificada"""
        print(f"\n🔍 Procurando aba com URL: {url}...")
        
        # 1. Procura em páginas existentes
        for page in self.context.pages:
            current_url = page.url
            print(f"   Verificando página: {current_url}")
            
            if url in current_url:
                self.tab_page = page
                page.bring_to_front()
                print(f"   ✓ Aba encontrada: [{page.title()}]")
                
                # Armazena a página se nome for fornecido
                if page_name:
                    self.pages[page_name] = page
                return page
        
        # 2. Se não encontrou, abre nova aba
        print(f"   → Nova aba necessária para: {url}")
        self.tab_page = self.context.new_page()
        self._apply_stealth(self.tab_page)
        
        # 3. Navega para a URL com tratamento de erros
        try:
            self.tab_page.goto(url, wait_until="domcontentloaded", timeout=30000)
            print(f"   ✓ Nova aba carregada: [{self.tab_page.title()}]")
        except Exception as e:
            print(f"⚠️ Erro ao carregar URL: {str(e)}", file=sys.stderr)
        
        # 4. Armazena a página se nome for fornecido
        if page_name:
            self.pages[page_name] = self.tab_page
        
        return self.tab_page

    def google_microphone(self):
        """Clica no botão de microfone do Google"""
        print("\n🎤 Ativando microfone do Google...")
        
        google_page = self.get_page("google")

        if not google_page:
            print("   ❌ Página do Google não encontrada")
            return False
        
        try:
            # Garante que estamos na página do Google
            google_page.bring_to_front()
            
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
                if google_page.locator(selector).count() > 0:
                    google_page.locator(selector).first.click()
                    print(f"   ✓ Microfone ativado usando seletor: {selector}")
                    clicked = True
                    break
            
            if not clicked:
                print("   ⚠ Botão do microfone não encontrado, tentando método alternativo...")
                # Tenta clicar por coordenadas aproximadas (geralmente à direita da barra de pesquisa)
                search_box = google_page.locator('textarea[name="q"], input[name="q"]').first
                if search_box:
                    box = search_box.bounding_box()
                    if box:
                        # Clica à direita da caixa de pesquisa onde geralmente fica o microfone
                        google_page.mouse.click(box['x'] + box['width'] + 30, box['y'] + box['height']/2)
                        print("   ✓ Tentativa de clique por posição relativa")
                        clicked = True
            
            time.sleep(2)  # Aguarda ativação do microfone
            return clicked
            
        except Exception as e:
            print(f"   ❌ Erro ao clicar no microfone: {e}")
            return False

    def read_google_search_field(self) -> str:
        """Lê o texto do campo de pesquisa do Google com múltiplas estratégias"""
        print("\n📖 Lendo campo de pesquisa do Google...")
        
        google_page = self.get_page("google")
        if not google_page:
            print("   ❌ Página do Google não encontrada")
            return None
        
        try:
            # Estratégias de seleção hierárquicas
            selectors = [
                'textarea[jsname="yZiJbe"]',  # Seletor mais específico (novo layout)
                'textarea[aria-label="Pesquisar"]',  # Por atributo ARIA
                'textarea[name="q"]',  # Seletor por nome
                'input[name="q"]',  # Versão alternativa do campo
                '.gLFyf',  # Seletor por classe principal
                '[role="combobox"]'  # Seletor por papel
            ]
            
            # Tentar cada seletor até encontrar o elemento
            for selector in selectors:
                element = google_page.locator(selector)
                if element.count() > 0:
                    text = element.first.input_value()
                    if text:
                        print(f"   ✓ Texto encontrado via '{selector}': '{text}'")
                        return text
            
            # Fallback 1: Tentar JS direto
            js_fallback = """
            return document.querySelector('textarea[jsname="yZiJbe"]')?.value || 
                   document.querySelector('textarea[name="q"]')?.value || 
                   document.querySelector('input[name="q"]')?.value || '';
            """
            js_result = google_page.evaluate(js_fallback)
            if js_result:
                print(f"   ✓ Texto encontrado via JS fallback: '{js_result}'")
                return js_result
            
            # Fallback 2: Tentar conteúdo visível
            visible_element = google_page.locator("textarea, input").filter(has_text=re.compile(r".+"))
            if visible_element.count() > 0:
                text = visible_element.first.input_value()
                if text:
                    print(f"   ✓ Texto encontrado via elemento visível: '{text}'")
                    return text
        
            print("   ⚠ Campo de pesquisa vazio ou não encontrado")
            return ""

        except Exception as e:
            print(f"   ❌ Erro crítico ao ler campo: {e}")
            # Última tentativa com timeout generoso
            try:
                text = google_page.locator('[name="q"]').first.input_value(timeout=10000)
                if text:
                    return text
            except:
                return None

    def get_page(self, page_name: str):
        """Retorna página armazenada pelo nome"""
        return self.pages.get(page_name)

    def bring_to_front(self, page_name: str):
        page = self.pages.get(page_name)
        page.bring_to_front()
        print(f"Você está na aba {page_name}.")

    def close(self):
        """Fecha a conexão com o navegador"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ Conexão finalizada")

    def url_search(self, url_suffix: str, page_name: str = None) -> bool:
        """
        Verifica se a URL da página atual ou de uma página específica termina com a string fornecida
        
        Args:
            url_suffix (str): String que deve estar no final da URL
            page_name (str, optional): Nome da página específica. Se None, usa a página atual (tab_page)
        
        Returns:
            bool: True se a URL termina com a string, False caso contrário
        """
        try:
            # Decide qual página verificar
            if page_name:
                page = self.get_page(page_name)
                if not page:
                    print(f"   ❌ Página '{page_name}' não encontrada")
                    return False
            else:
                page = self.tab_page
                if not page:
                    print("   ❌ Nenhuma página ativa encontrada")
                    return False
            
            # Obtém a URL atual da página
            current_url = page.url
            
            # Verifica se termina com o sufixo
            result = current_url.endswith(url_suffix)
            
            print(f"   🔍 URL atual: {current_url}")
            print(f"   📝 Verificando se termina com: '{url_suffix}'")
            print(f"   ✓ Resultado: {result}")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Erro ao verificar URL: {e}")
            return False

    def login(self, page_name=None) -> bool:
        """
        Método combinado para fazer login completo usando credentials
        
        Args:
            page_name (str, optional): Nome da página específica
        
        Returns:
            bool: True se login foi realizado com sucesso
        """
        print("\n🚀 Iniciando login automático...")
        
        # Verifica se credenciais estão carregadas CORRETAMENTE
        print(f"   🔍 Status inicial das credenciais: {self.status}")
        print(f"   📋 Dados das credenciais: {self.data is not None}")
        
        # Se status inicial for falsy ou dados não existirem, tenta recarregar
        if not self.data or self.status != 0:  # MUDANÇA AQUI: 0 é sucesso no seu sistema!
            print("   🔄 Tentando recarregar credenciais...")
            self.status, self.data = self.creds.load_credentials()
            print(f"   📊 Novo status: {self.status}, Dados: {self.data is not None}")
        
        # Verifica se temos dados válidos (0 = sucesso no seu sistema)
        if self.status != 0 or not self.data:  # MUDANÇA AQUI: 0 é sucesso!
            print("   ❌ Credenciais não foram carregadas corretamente")
            print(f"      Status: {self.status} (0 = sucesso)")
            print(f"      Data: {self.data}")
            return False
        
        # Verifica se os campos necessários existem
        if 'email' not in self.data or 'password' not in self.data:
            print("   ❌ Campos email ou password não encontrados nas credenciais")
            print(f"      Campos disponíveis: {list(self.data.keys()) if self.data else 'None'}")
            return False
        
        # Verifica se email e password não são None
        if not self.data['email'] or not self.data['password']:
            print("   ❌ Email ou password estão vazios/None")
            print(f"      Email: {self.data.get('email')}")
            print(f"      Password: {self.data.get('password')}")
            return False
        
        print(f"   ✅ Credenciais carregadas com sucesso")
        print(f"      Email: {self.data.get('email', 'N/A')}")
        print(f"      Password: {'***' if self.data.get('password') else 'N/A'}")
        
        # Preenche email
        if not self.fill_email_field(page_name):
            return False
        
        # Aguarda um pouco para a página carregar
        time.sleep(2)
        
        # Preenche senha
        if not self.fill_password_field(page_name):
            return False
        
        print("   ✅ Login automático concluído!")
        return True
    
    def fill_email_field(self, page_name=None) -> bool:
        """
        Identifica e preenche o campo de email usando credentials carregadas
        """
        try:
            # Debug das credenciais
            print(f"   🔍 Debug credenciais - Status: {self.status}, Data: {self.data is not None}")
            
            # Verifica se as credenciais foram carregadas (0 = sucesso)
            if self.status != 0:  # MUDANÇA AQUI
                print(f"   ❌ Status das credenciais indica erro: {self.status} (0 = sucesso)")
                return False
                
            if not self.data:
                print(f"   ❌ Data das credenciais é None ou vazio: {self.data}")
                return False
                
            if 'email' not in self.data:
                print(f"   ❌ Campo 'email' não encontrado. Campos disponíveis: {list(self.data.keys())}")
                return False
            
            if not self.data['email']:  # NOVA VERIFICAÇÃO
                print(f"   ❌ Email está vazio/None: {self.data['email']}")
                return False
            
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página encontrada")
                return False
            
            email = self.data['email']
            print(f"\n📧 Preenchendo campo de email com: {email}")
            
            # Aguarda o elemento estar disponível (igual ao Selenium WebDriverWait)
            try:
                # Baseado no seu HTML, o seletor mais preciso é por name="email"
                email_element = page.locator('input[name="email"]')
                email_element.wait_for(state="visible", timeout=10000)  # 10 segundos como no Selenium
                
                # Limpa o campo primeiro (igual ao .clear() do Selenium)
                email_element.fill("")
                
                # Preenche com o email das credenciais
                email_element.fill(email)
                
                # Pressiona Enter (igual ao Keys.RETURN do Selenium)
                email_element.press("Enter")
                
                print(f"   ✓ Email preenchido com sucesso: {email}")
                return True
                
            except Exception as e:
                print(f"   ⚠️ Seletor principal falhou, tentando alternativas: {e}")
                
                # Fallback: tenta outros seletores baseados no seu HTML
                fallback_selectors = [
                    'input[type="email"][name="email"]',  # Mais específico
                    'input[id="mat-input-0"]',  # Por ID específico
                    'input[data-placeholder="E-mail"]',  # Por data-placeholder
                    'input[autocomplete="username"]',  # Por autocomplete
                    'input.mat-input-element[type="email"]'  # Por classe + tipo
                ]
                
                for selector in fallback_selectors:
                    try:
                        element = page.locator(selector)
                        if element.count() > 0:
                            element.wait_for(state="visible", timeout=5000)
                            element.fill("")  # Limpa
                            element.fill(email)  # Preenche
                            element.press("Enter")  # Enter
                            print(f"   ✓ Email preenchido usando fallback: {selector}")
                            return True
                    except:
                        continue
            
            print("   ❌ Campo de email não encontrado com nenhum seletor")
            return False
            
        except Exception as e:
            print(f"   ❌ Erro ao preencher email: {e}")
            return False
    
    def fill_password_field(self, page_name=None) -> bool:
        """
        Identifica e preenche o campo de senha usando credentials carregadas
        """
        try:
            # Debug das credenciais
            print(f"   🔍 Debug credenciais - Status: {self.status}, Data: {self.data is not None}")
            
            # Verifica se as credenciais foram carregadas (0 = sucesso)
            if self.status != 0:  # MUDANÇA AQUI
                print(f"   ❌ Status das credenciais indica erro: {self.status} (0 = sucesso)")
                return False
                
            if not self.data:
                print(f"   ❌ Data das credenciais é None ou vazio: {self.data}")
                return False
                
            if 'password' not in self.data:
                print(f"   ❌ Campo 'password' não encontrado. Campos disponíveis: {list(self.data.keys())}")
                return False
            
            if not self.data['password']:  # NOVA VERIFICAÇÃO
                print(f"   ❌ Password está vazio/None: {self.data['password']}")
                return False
            
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página encontrada")
                return False
            
            password = self.data['password']
            print(f"\n🔒 Preenchendo campo de senha...")
            
            # Aguarda um pouco para o campo aparecer (após preencher email)
            time.sleep(1)
            
            try:
                # Seletor principal para senha
                password_element = page.locator('input[type="password"][name="password"]')
                password_element.wait_for(state="visible", timeout=10000)
                
                password_element.fill("")  # Limpa
                password_element.fill(password)  # Preenche
                password_element.press("Enter")  # Enter
                
                print(f"   ✓ Senha preenchida com sucesso")
                return True
                
            except Exception as e:
                print(f"   ⚠️ Seletor principal falhou, tentando alternativas: {e}")
                
                # Fallback para senha
                password_selectors = [
                    'input[type="password"]',
                    'input[name="password"]',
                    'input[data-placeholder*="senha" i]',
                    'input[autocomplete="current-password"]'
                ]
                
                for selector in password_selectors:
                    try:
                        element = page.locator(selector)
                        if element.count() > 0:
                            element.wait_for(state="visible", timeout=5000)
                            element.fill("")
                            element.fill(password)
                            element.press("Enter")
                            print(f"   ✓ Senha preenchida usando fallback: {selector}")
                            return True
                    except:
                        continue
            
            print("   ❌ Campo de senha não encontrado")
            return False
            
        except Exception as e:
            print(f"   ❌ Erro ao preencher senha: {e}")
            return False

    def close_tab(self, page_name: str = None) -> bool:
        """
        Fecha uma aba específica ou a aba atual
        
        Args:
            page_name (str, optional): Nome da página específica. Se None, fecha a aba atual
        
        Returns:
            bool: True se fechou com sucesso, False caso contrário
        """
        try:
            # Decide qual página fechar
            if page_name:
                page = self.get_page(page_name)
                if not page:
                    print(f"   ❌ Página '{page_name}' não encontrada")
                    return False
                print(f"   🗂️ Fechando aba: {page_name}")
            else:
                page = self.tab_page
                if not page:
                    print("   ❌ Nenhuma página ativa encontrada")
                    return False
                print(f"   🗂️ Fechando aba atual")
            
            # Fecha a página
            page.close()
            
            # Remove do dicionário de páginas se existir
            if page_name and page_name in self.pages:
                del self.pages[page_name]
            
            # Se era a página atual, limpa a referência
            if page == self.tab_page:
                self.tab_page = None
            
            print(f"   ✅ Aba fechada com sucesso")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao fechar aba: {e}")
            return False
    
    def close_all_tabs_except(self, keep_page_name: str) -> bool:
        """
        Fecha todas as abas exceto uma específica
        
        Args:
            keep_page_name (str): Nome da página para manter aberta
        
        Returns:
            bool: True se fechou com sucesso, False caso contrário
        """
        try:
            keep_page = self.get_page(keep_page_name)
            if not keep_page:
                print(f"   ❌ Página '{keep_page_name}' não encontrada")
                return False
            
            print(f"   🗂️ Fechando todas as abas exceto: {keep_page_name}")
            
            # Lista todas as páginas para fechar
            pages_to_close = []
            for page in self.context.pages:
                if page != keep_page:
                    pages_to_close.append(page)
            
            # Fecha as páginas
            closed_count = 0
            for page in pages_to_close:
                try:
                    page.close()
                    closed_count += 1
                except:
                    continue
            
            # Limpa dicionário de páginas (mantém apenas a que ficou)
            self.pages = {keep_page_name: keep_page}
            self.tab_page = keep_page
            
            print(f"   ✅ {closed_count} abas fechadas. Mantida: {keep_page_name}")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao fechar abas: {e}")
            return False
    
    def close_all_tabs(self) -> bool:
        """
        Fecha todas as abas abertas
        
        Returns:
            bool: True se fechou com sucesso, False caso contrário
        """
        try:
            print(f"   🗂️ Fechando todas as {len(self.context.pages)} abas")
            
            # Lista todas as páginas para fechar
            pages_to_close = list(self.context.pages)
            
            # Fecha as páginas
            closed_count = 0
            for page in pages_to_close:
                try:
                    page.close()
                    closed_count += 1
                except:
                    continue
            
            # Limpa referências
            self.pages.clear()
            self.tab_page = None
            
            print(f"   ✅ {closed_count} abas fechadas")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao fechar todas as abas: {e}")
            return False
    
    def list_open_tabs(self) -> list:
        """
        Lista todas as abas abertas
        
        Returns:
            list: Lista com informações das abas abertas
        """
        try:
            tabs_info = []
            
            print(f"\n📋 Abas abertas ({len(self.context.pages)}):")
            
            for i, page in enumerate(self.context.pages):
                try:
                    title = page.title()[:50]  # Limita título a 50 chars
                    url = page.url[:60]        # Limita URL a 60 chars
                    
                    # Verifica se é uma página nomeada
                    page_name = None
                    for name, stored_page in self.pages.items():
                        if stored_page == page:
                            page_name = name
                            break
                    
                    tab_info = {
                        'index': i,
                        'title': title,
                        'url': url,
                        'name': page_name,
                        'is_current': page == self.tab_page
                    }
                    
                    tabs_info.append(tab_info)
                    
                    status = "🔸 ATUAL" if page == self.tab_page else "  "
                    name_str = f" [{page_name}]" if page_name else ""
                    print(f"   {status} {i+1}. {title}{name_str}")
                    print(f"        URL: {url}")
                    
                except Exception as e:
                    print(f"   ❌ Erro ao ler aba {i+1}: {e}")
            
            return tabs_info
            
        except Exception as e:
            print(f"   ❌ Erro ao listar abas: {e}")
            return []
    
    def switch_to_tab(self, page_name: str) -> bool:
        """
        Muda para uma aba específica
        
        Args:
            page_name (str): Nome da página para mudar
        
        Returns:
            bool: True se mudou com sucesso, False caso contrário
        """
        try:
            page = self.get_page(page_name)
            if not page:
                print(f"   ❌ Página '{page_name}' não encontrada")
                return False
            
            page.bring_to_front()
            self.tab_page = page
            
            print(f"   ✅ Mudou para aba: {page_name}")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao mudar para aba: {e}")
            return False

    def fill_search_field_pdv(self, search_text: str, page_name: str = None) -> bool:
        """
        Preenche o campo de busca de produto
        
        Args:
            search_text (str): Texto para preencher no campo de busca
            page_name (str, optional): Nome da página específica
        
        Returns:
            bool: True se preencheu com sucesso, False caso contrário
        """
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página encontrada")
                return False
            
            print(f"\n🔍 Preenchendo campo de busca com: '{search_text}'")
            
            # Seletores para o campo de busca baseado no HTML fornecido
            search_selectors = [
                'input[type="search"][data-placeholder*="Digite para buscar" i]',  # Mais específico
                'input[type="search"]',  # Por tipo
                'input[data-placeholder*="buscar" i]',  # Por placeholder
                'input[data-placeholder*="produto" i]',  # Por "produto" no placeholder
                'input[autocomplete="off"][type="search"]',  # Por autocomplete + tipo
                'input.mat-input-element[type="search"]',  # Por classe + tipo
                'input[role="combobox"]',  # Por role
                'input[aria-autocomplete="list"]'  # Por aria-autocomplete
            ]
            
            # Tenta cada seletor
            for selector in search_selectors:
                try:
                    element = page.locator(selector)
                    if element.count() > 0:
                        # Aguarda o elemento estar visível
                        element.wait_for(state="visible", timeout=5000)
                        
                        # Preenche o campo (sem pressionar Enter)
                        element.fill(search_text)
                        
                        print(f"   ✓ Campo preenchido usando seletor: {selector}")
                        return True
                        
                except Exception as e:
                    print(f"   ⚠️ Falha no seletor '{selector}': {e}")
                    continue
            
            print("   ❌ Campo de busca não encontrado com nenhum seletor")
            return False
            
        except Exception as e:
            print(f"   ❌ Erro ao preencher campo de busca: {e}")
            return False

    def unit_pdv(self, units: int, page_name: str = None) -> bool:
        """
        Pressiona '*', digita o número de unidades e pressiona Enter
        
        Args:
            units (int): Número de unidades a digitar
            page_name (str, optional): Nome da página específica
        
        Returns:
            bool: True se executou com sucesso, False caso contrário
        """
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n🔢 Inserindo {units} unidades no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.5)  # Pequena pausa para garantir foco
            
            # Pressiona a tecla "*"
            page.keyboard.press("*")
            print(f"   ✓ Tecla '*' pressionada")
            
            # Aguarda um momento para o campo abrir
            time.sleep(0.5)
            
            # Digita o número de unidades
            page.keyboard.type(str(units))
            print(f"   ✓ Número '{units}' digitado")
            
            # Aguarda um momento antes de pressionar Enter
            time.sleep(0.3)
            
            # Pressiona Enter
            page.keyboard.press("Enter")
            print(f"   ✓ Enter pressionado")
            
            print(f"   ✅ {units} unidades inseridas com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao inserir unidades: {e}")
            return False

    def enter_pdv(self, page_name: str = None) -> bool:
        """
        Pressiona apenas a tecla Enter
        
        Args:
            page_name (str, optional): Nome da página específica
        
        Returns:
            bool: True se executou com sucesso, False caso contrário
        """
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando Enter no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            # Pressiona Enter
            page.keyboard.press("Enter")
            
            print(f"   ✅ Enter pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False
    
    def next_pdv(self, page_name: str = None) -> bool:
        """
        Pressiona a seta para baixo
        
        Args:
            page_name (str, optional): Nome da página específica
        
        Returns:
            bool: True se executou com sucesso, False caso contrário
        """
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⬇️ Navegando para próximo item no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            # Pressiona seta para baixo
            page.keyboard.press("ArrowDown")
            
            print(f"   ✅ Seta para baixo pressionada!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar seta para baixo: {e}")
            return False
    
    def previous_pdv(self, page_name: str = None) -> bool:
        """
        Pressiona a seta para cima (método extra para navegação)
        
        Args:
            page_name (str, optional): Nome da página específica
        
        Returns:
            bool: True se executou com sucesso, False caso contrário
        """
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⬆️ Navegando para item anterior no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            # Pressiona seta para cima
            page.keyboard.press("ArrowUp")
            
            print(f"   ✅ Seta para cima pressionada!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar seta para cima: {e}")
            return False

    def debit_pdv(self, page_name: str = None) -> bool:
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando 'c' no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            page.keyboard.press("F3")
            time.sleep(0.3)
            page.keyboard.press("c")
            time.sleep(0.3)
            page.keyboard.press("Enter")
            time.sleep(0.3)
            page.keyboard.press("F3")
            
            print(f"   ✅ Débito pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False

    def credit_pdv(self, page_name: str = None) -> bool:
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando 'd' no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            page.keyboard.press("F3")
            time.sleep(0.3)
            page.keyboard.press("d")
            time.sleep(0.3)
            page.keyboard.press("Enter")
            time.sleep(0.3)
            page.keyboard.press("F3")
            
            print(f"   ✅ Crédito pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False

    def pix_pdv(self, page_name: str = None) -> bool:
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando 'b' no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            page.keyboard.press("F3")
            time.sleep(0.3)
            page.keyboard.press("b")
            time.sleep(0.3)
            page.keyboard.press("Enter")
            time.sleep(0.3)
            page.keyboard.press("F3")
            
            print(f"   ✅ Pix pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False

    def f3_pdv(self, page_name: str = None) -> bool:
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando 'F3' no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            # Pressiona Enter
            page.keyboard.press("F3")
            
            print(f"   ✅ F3 pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False

    def discount_pdv(self, page_name: str = None) -> bool:
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando 'CONTROL+D' no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            # Pressiona Enter
            page.keyboard.down("Control")
            page.keyboard.press("d")
            page.keyboard.up("Control")
            
            print(f"   ✅ CONTROL+D pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False

    def change_price_pdv(self, page_name: str = None) -> bool:
        try:
            # Decide qual página usar
            page = self.get_page(page_name) if page_name else self.tab_page
            if not page:
                print("   ❌ Nenhuma página PDV encontrada")
                return False
            
            print(f"\n⏎ Pressionando 'HOME' no PDV...")
            
            # Garante que a página está em foco
            page.bring_to_front()
            time.sleep(0.3)
            
            # Pressiona Enter
            page.keyboard.press("Home")
            
            print(f"   ✅ HOME pressionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao pressionar Enter: {e}")
            return False