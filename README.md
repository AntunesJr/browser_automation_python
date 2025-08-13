# Browser Automation Python v2.0

🚀 **Sistema de automação de browsers via Chrome DevTools Protocol com controle por comandos de voz e mouse.**

## 📋 Visão Geral

Sistema avançado de automação que permite:
- ✅ **Controle de PDV via comandos de voz** (Google Speech + ChatGPT)
- ✅ **Automação via Chrome DevTools Protocol** (CDP)
- ✅ **Sistema de credenciais criptografado** (AES-256)
- ✅ **Controle por botões do mouse** personalizáveis
- ✅ **Multi-threading** para operações simultâneas
- ✅ **Interface amigável** com logs coloridos

### 🔄 **Mudanças na v2.0**

| **Antes (v1.x)** | **Agora (v2.0)** |
|------------------|------------------|
| ❌ Selenium + Firefox + GeckoDriver | ✅ Playwright + Chrome CDP |
| ❌ Configuração complexa | ✅ Instalação automática |
| ❌ Detecção fácil de bots | ✅ Stealth nativo via CDP |
| ❌ Performance limitada | ✅ Performance otimizada |

## 🛠️ Pré-requisitos

### **Sistema Operacional**
- 🐧 **Linux** (Debian/Ubuntu recomendado)
- 🍎 **macOS** (com Homebrew)
- 🪟 **Windows** (com WSL recomendado)

### **Software Base**
- 🐍 **Python 3.8+**
- 🌐 **Acesso à internet** (para instalação)
- 💾 **2GB de espaço livre**

## ⚡ Instalação Rápida

### **1️⃣ Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
```

### **2️⃣ Execute a Configuração Automática**
```bash
# Configuração completa (recomendado)
python3 custom_setup.py

# OU execute etapa por etapa:
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
python3 custom_setup.py
```

### **3️⃣ Verifique a Instalação**
```bash
python3 test_installation.py
```

### **4️⃣ Configure as Credenciais**
```bash
# Crie suas credenciais
create_cred "seu@email.com" "suaSenha123" --username "seuNome"

# Verifique se funcionou
check_cred
```

### **5️⃣ Execute o Sistema**
```bash
# Inicie o Chrome debug
./start_chrome_debug.sh

# Em outro terminal, execute o programa
python3 main.py
```

## 🔧 Instalação Detalhada

### **Linux (Debian/Ubuntu)**

```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python e dependências
sudo apt install -y python3 python3-pip python3-venv python3-dev python3-tk

# 3. Clonar e configurar
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 -m venv .venv
source .venv/bin/activate

# 4. Instalação automática
python3 custom_setup.py

# 5. Teste
python3 test_installation.py
```

### **macOS**

```bash
# 1. Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar Python
brew install python3

# 3. Clonar e configurar
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 -m venv .venv
source .venv/bin/activate

# 4. Instalação automática
python3 custom_setup.py
```

### **Windows (WSL Recomendado)**

```powershell
# 1. Instalar WSL2 + Ubuntu
wsl --install -d Ubuntu

# 2. No Ubuntu WSL, seguir os passos do Linux
# 3. Ou usar Python nativo do Windows:

# Baixar Python de python.org
# Clonar repositório
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python -m venv .venv
.venv\Scripts\activate
python custom_setup.py
```

## 🎯 Como Usar

### **Comando de Voz PDV**

1. **Inicie o sistema:**
```bash
./start_chrome_debug.sh
python3 main.py
```

2. **Use os comandos de voz:**
   - 🎤 **Pressione o botão do mouse configurado** para ativar
   - 🗣️ **Fale o comando** (ex: "pesquisar coca cola")
   - ✅ **O sistema processa automaticamente**

### **Comandos Disponíveis**

| **Comando** | **Ação** | **Exemplo** |
|-------------|----------|-------------|
| `pesquisar [produto]` | Busca produto no PDV | "pesquisar coca cola" |
| `X unidades` | Define quantidade | "5 unidades", "duas unidades" |
| `enter` / `confirmar` | Pressiona Enter | "confirmar" |
| `próximo` / `baixo` | Próximo item | "próximo" |
| `login` | Faz login automático | "login" |
| `débito` | Finaliza no débito | "débito" |
| `crédito` | Finaliza no crédito | "crédito" |
| `pix` | Finaliza no PIX | "pix" |
| `desconto` | Aplica desconto | "desconto" |
| `limpar` | Limpa campo | "limpar" |
| `sair programa` | Encerra sistema | "sair programa" |

### **Configuração dos Botões do Mouse**

```bash
# Identifique seus botões
python3 main.py --identify

# Edite o arquivo main.py e altere:
VOICE_TRIGGER_BUTTON = mouse.Button.button8  # Seu botão preferido
```

## 📁 Estrutura do Projeto

```
browser_automation_python/
├── 📄 main.py                    # Programa principal
├── 📄 custom_setup.py            # Configuração automática
├── 📄 test_installation.py       # Verificação da instalação
├── 📄 start_chrome_debug.sh      # Script para Chrome debug
├── 📄 requirements.txt           # Dependências Python
├── 📄 README.md                  # Esta documentação
├── 📁 browser/                   # Módulo de controle de browser
│   ├── 📄 __init__.py
│   └── 📄 browser_cdp.py         # Controle via CDP
├── 📁 credentials/               # Sistema de credenciais
│   ├── 📄 __init__.py
│   ├── 📄 credentials.py         # Gerenciador principal
│   ├── 📁 commands/              # Comandos CLI
│   │   ├── 📄 check_cred.py      # Verificar credenciais
│   │   ├── 📄 create_cred.py     # Criar credenciais
│   │   └── 📄 show_cred.py       # Mostrar credenciais
│   ├── 📁 config/                # Configurações
│   │   ├── 📄 config.py          # Config principal
│   │   └── 📄 config_manager.py  # Gerenciador de configs
│   ├── 📁 core/                  # Núcleo do sistema
│   │   ├── 📄 credentials_checker.py
│   │   └── 📄 credentials_reader.py
│   ├── 📁 crypto/                # Criptografia
│   │   ├── 📄 crypto_manager.py
│   │   └── 📄 decrypto_manager.py
│   └── 📁 message/               # Sistema de mensagens
│       ├── 📄 msg_code.py
│       └── 📄 msg_handler.py
└── 📁 tests/                     # Testes automatizados
    └── 📁 unit/
        └── 📄 test_credentials.py
```

## 🎮 Comandos CLI

### **Gerenciamento de Credenciais**

```bash
# Criar credenciais
create_cred "email@exemplo.com" "senha123" --username "nome"

# Verificar status
check_cred                    # Visual detalhado
check_cred_json              # Saída JSON

# Mostrar credenciais (descriptografadas)
show_cred                    # Visual
show_cred_json              # JSON

# Criar via JSON
echo '{"email":"test@test.com","password":"123","username":"test"}' | create_cred_json
```

### **Controle do Sistema**

```bash
# Iniciar Chrome debug
./start_chrome_debug.sh

# Executar programa principal
python3 main.py

# Identificar botões do mouse
python3 main.py --identify

# Verificar instalação
python3 test_installation.py

# Reconfigurar ambiente
python3 custom_setup.py
```

## 🔍 Verificação e Diagnóstico

### **Teste Rápido**
```bash
python3 test_installation.py
```

### **Verificar Chrome Debug**
```bash
# Verificar se Chrome debug está rodando
curl http://localhost:9222/json

# Listar processos Chrome
ps aux | grep chrome

# Matar processos Chrome se necessário
pkill -f chrome
```

### **Logs e Debug**
```bash
# Ver logs detalhados
python3 main.py  # Logs aparecem no terminal

# Verificar arquivos de credenciais
check_cred

# Testar conexão CDP
python3 -c "
from browser.browser_cdp import BrowserCDP
browser = BrowserCDP()
print('Conectado!' if browser.connect() else 'Erro!')
"
```

## ⚠️ Solução de Problemas

### **Chrome não inicia em modo debug**
```bash
# Método 1: Script automático
./start_chrome_debug.sh

# Método 2: Manual
google-chrome-stable --remote-debugging-port=9222 --user-data-dir="$HOME/.config/chrome-debug" &

# Método 3: Perfil temporário
google-chrome-stable --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug" &
```

### **Erro "Module not found"**
```bash
# Reinstalar dependências
pip install -r requirements.txt
python -m playwright install

# Verificar Python path
python3 -c "import sys; print('\n'.join(sys.path))"
```

### **Problemas de permissão no Linux**
```bash
# Adicionar usuário ao grupo de áudio/input
sudo usermod -a -G audio,input $USER

# Verificar variáveis de ambiente
echo $DISPLAY
export DISPLAY=:0  # Se necessário
```

### **Botão do mouse não funciona**
```bash
# Identificar botões
python3 main.py --identify

# Verificar pynput
python3 -c "
from pynput import mouse
print('Mouse position:', mouse.position)
print('Buttons available:', [str(b) for b in mouse.Button])
"
```

### **PDV não responde**
1. ✅ Verificar se Chrome debug está rodando
2. ✅ Verificar se as credenciais estão configuradas
3. ✅ Verificar conexão com internet
4. ✅ Tentar recarregar página: comando de voz "recarregar"

## 🔒 Segurança

- 🔐 **Credenciais criptografadas** com AES-256
- 🔑 **Chaves protegidas** com permissões restritas (600)
- 🛡️ **Perfil isolado** do Chrome para debug
- 🚫 **Sem logs sensíveis** (senhas não aparecem em logs)

## 📊 Performance

- ⚡ **Tempo de resposta**: < 2 segundos para comandos
- 🧠 **Uso de RAM**: ~200-500MB durante execução
- 💾 **Espaço em disco**: ~100MB + browsers
- 🔄 **Multi-threading**: Operações simultâneas PDV + Voice

## 🤝 Contribuição

1. 🍴 Fork o repositório
2. 🌿 Crie uma branch: `git checkout -b feature/nova-feature`
3. 📝 Commit suas mudanças: `git commit -m 'Add nova feature'`
4. 📤 Push para branch: `git push origin feature/nova-feature`
5. 🔄 Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a **GNU General Public License v3.0** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- 📧 **Email**: silvioantunes1@hotmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/browser_automation_python/issues)
- 📚 **Wiki**: [Documentação Completa](https://github.com/seu-usuario/browser_automation_python/wiki)

## 🎉 Changelog

### **v2.0.0** (Atual)
- ✅ Migração para Playwright + Chrome CDP
- ✅ Sistema de instalação automática
- ✅ Comandos de voz aprimorados
- ✅ Interface melhorada
- ✅ Performance otimizada

### **v1.x** (Deprecated)
- ❌ Baseado em Selenium + Firefox
- ❌ Configuração manual complexa
- ❌ Performance limitada

---

<div align="center">

**🚀 Feito com ❤️ para automação inteligente de browsers**

[⬆️ Voltar ao topo](#browser-automation-python-v20)

</div>


2. Execute:
bashcd browser_automation_python
python3 custom_setup.py
python3 test_installation.py
3. Configure suas credenciais:
bashcreate_cred "seu@email.com" "suaSenha123" --username "seuNome"
4. Execute:
bash./start_chrome_debug.sh
python3 main.py