# 🚀 Guia de Instalação Rápida v2.0

## ⚡ Instalação em 1 Comando

```bash
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 install.py
```

**É isso! 🎉** O script `install.py` faz tudo automaticamente.

---

## 📋 Métodos de Instalação

### 🔥 **Método 1: Ultra-Rápido (Recomendado)**

```bash
# Clone e instale tudo automaticamente
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 install.py
```

### 🛠️ **Método 2: Passo a Passo**

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python

# 2. Crie ambiente virtual (opcional mas recomendado)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Configure ambiente completo
python3 custom_setup.py

# 4. Instale comandos CLI
pip install -e .

# 5. Teste instalação
python3 test_installation.py
```

### 🧪 **Método 3: Manual (Para Desenvolvedores)**

```bash
# Dependências básicas
pip install playwright pynput cryptography requests psutil coloredlogs

# Browsers do Playwright
python -m playwright install chromium

# Instalar o projeto
pip install -e .

# Configurar Chrome debug
./start_chrome_debug.sh

# Executar
python main.py
```

---

## ✅ Verificação da Instalação

### **Teste Rápido**
```bash
# Verifica se tudo está funcionando
python3 test_installation.py
```

### **Teste dos Comandos CLI**
```bash
# Testa todos os comandos instalados
python3 test_commands.py
```

### **Verificação Manual**
```bash
# Comandos devem estar disponíveis:
check_cred                    # ✅
create_cred                   # ✅
browser_automation           # ✅
setup_browser_automation     # ✅

# Módulos devem importar:
python3 -c "from credentials.credentials import Credentials; print('OK')"
python3 -c "from browser.browser_cdp import BrowserCDP; print('OK')"
```

---

## 🎯 Configuração Inicial

### **1. Criar Credenciais**
```bash
create_cred "seu@email.com" "suaSenha123" --username "seuNome"

# Verificar se funcionou
check_cred
```

### **2. Configurar Botão do Mouse**
```bash
# Identificar seus botões
python3 main.py --identify

# Editar main.py e alterar:
# VOICE_TRIGGER_BUTTON = mouse.Button.button8  # Seu botão
```

### **3. Iniciar Chrome Debug**
```bash
./start_chrome_debug.sh

# Verificar se funcionou
curl http://localhost:9222/json
```

### **4. Executar o Sistema**
```bash
browser_automation
# OU: python3 main.py
```

---

## 🔧 Scripts Disponíveis

| **Script** | **Função** | **Uso** |
|------------|------------|---------|
| `install.py` | 🚀 Instalação completa automática | `python3 install.py` |
| `custom_setup.py` | 🛠️ Configuração detalhada do ambiente | `python3 custom_setup.py` |
| `test_installation.py` | 🧪 Verificação da instalação | `python3 test_installation.py` |
| `test_commands.py` | 📋 Teste dos comandos CLI | `python3 test_commands.py` |
| `start_chrome_debug.sh` | 🌐 Iniciar Chrome debug | `./start_chrome_debug.sh` |

---

## 📦 Comandos CLI Instalados

### **Credenciais**
```bash
check_cred                  # Verificar status das credenciais
check_cred_json            # Verificar em formato JSON
create_cred email senha    # Criar novas credenciais
show_cred                  # Mostrar credenciais descriptografadas
show_cred_json            # Mostrar em formato JSON
```

### **Sistema**
```bash
browser_automation         # Executar programa principal
setup_browser_automation   # Reconfigurar ambiente
test_browser_automation    # Testar instalação
identify_mouse_buttons     # Configurar botões do mouse
start_chrome_debug        # Iniciar Chrome debug
```

---

## 🐧 Instalação por Sistema Operacional

### **Ubuntu/Debian**
```bash
# Dependências do sistema
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev python3-tk curl wget

# Instalar projeto
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 install.py
```

### **macOS**
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Dependências
brew install python3

# Instalar projeto
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 install.py
```

### **Windows (WSL)**
```bash
# No PowerShell como Admin:
wsl --install -d Ubuntu

# No Ubuntu WSL:
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 install.py
```

---

## ❓ Resolução de Problemas

### **Erro: "Command not found"**
```bash
# Reinstalar comandos
pip install -e .

# Verificar PATH
echo $PATH
pip show -f browser-automation-python
```

### **Erro: "Chrome não encontrado"**
```bash
# Ubuntu/Debian
python3 custom_setup.py  # Instala automaticamente

# Manual
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update && sudo apt install google-chrome-stable
```

### **Erro: "Module not found"**
```bash
# Reinstalar dependências
pip install -r requirements.txt
python -m playwright install

# Verificar instalação
python3 test_installation.py
```

### **Erro: "Permission denied"**
```bash
# Corrigir permissões
chmod +x start_chrome_debug.sh
chmod 700 .credentials
sudo usermod -a -G audio,input $USER
```

---

## 🎮 Exemplo de Uso Completo

```bash
# 1. Instalação
git clone https://github.com/seu-usuario/browser_automation_python.git
cd browser_automation_python
python3 install.py

# 2. Configurar credenciais
create_cred "meu@email.com" "minhaSenha123" --username "MeuNome"

# 3. Verificar se está OK
check_cred

# 4. Identificar botão do mouse
python3 main.py --identify
# (Clique no botão que quer usar e anote o código)

# 5. Editar configuração (opcional)
nano main.py
# Altere: VOICE_TRIGGER_BUTTON = mouse.Button.button8

# 6. Iniciar Chrome debug
./start_chrome_debug.sh

# 7. Executar sistema
browser_automation

# 8. Usar comandos de voz
# - Pressione o botão do mouse configurado
# - Fale: "pesquisar coca cola"
# - Fale: "5 unidades"
# - Fale: "confirmar"
```

---

## 📊 Status da Instalação

✅ **Se tudo funcionou:**
- Todos os comandos CLI disponíveis
- Chrome debug iniciando corretamente
- Credenciais criptografadas funcionando
- Sistema de voz respondendo

❌ **Se algo não funcionou:**
1. Execute: `python3 test_installation.py`
2. Execute: `python3 test_commands.py`
3. Verifique os erros reportados
4. Execute: `python3 custom_setup.py` novamente

---

## 📞 Suporte

- 🐛 **Problemas**: [GitHub Issues](https://github.com/seu-usuario/browser_automation_python/issues)
- 📧 **Email**: silvioantunes1@hotmail.com
- 📚 **Documentação**: [README.md](README.md)

---

<div align="center">

**🎉 Instalação Completa para Browser Automation v2.0! 🚀**

[⬆️ Voltar ao topo](#-guia-de-instalação-rápida-v20)

</div>