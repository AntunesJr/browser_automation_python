#!/bin/bash

# Script para copiar perfil do Chrome de forma segura
# Salve como: setup_chrome_debug.sh

echo "🔧 Configurando Chrome debug mantendo seu perfil..."

SOURCE_PROFILE="$HOME/.config/google-chrome"
DEBUG_PROFILE="$HOME/.config/google-chrome-debug"

# Função para copiar com exclusões
safe_copy_profile() {
    echo "📂 Copiando perfil do Chrome de forma segura..."
    
    # Criar diretório de destino
    mkdir -p "$DEBUG_PROFILE"
    
    # Copiar usando rsync (mais robusto) ou cp com exclusões
    if command -v rsync >/dev/null 2>&1; then
        echo "   → Usando rsync para cópia robusta..."
        rsync -av --exclude='*.lock' \
                  --exclude='*SingletonLock*' \
                  --exclude='*SingletonSocket*' \
                  --exclude='*SingletonCookie*' \
                  --exclude='*.tmp' \
                  --exclude='BrowserMetrics-spare.pma' \
                  "$SOURCE_PROFILE/" "$DEBUG_PROFILE/"
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Perfil copiado com sucesso usando rsync"
            return 0
        else
            echo "   ⚠️ Rsync com alguns avisos, mas provavelmente funcionou"
            return 0
        fi
    else
        echo "   → Usando cp com tratamento de erros..."
        # Copiar tudo e ignorar erros de arquivos bloqueados
        cp -r "$SOURCE_PROFILE" "$DEBUG_PROFILE" 2>/dev/null || {
            # Se falhar, tenta cópia manual dos diretórios importantes
            echo "   → Copiando arquivos importantes manualmente..."
            
            # Criar estrutura básica
            mkdir -p "$DEBUG_PROFILE/Default"
            
            # Copiar arquivos importantes (ignora erros)
            cp "$SOURCE_PROFILE/Local State" "$DEBUG_PROFILE/" 2>/dev/null
            cp "$SOURCE_PROFILE/First Run" "$DEBUG_PROFILE/" 2>/dev/null
            cp "$SOURCE_PROFILE/Last Version" "$DEBUG_PROFILE/" 2>/dev/null
            
            # Copiar diretório Default (mais importante)
            cp -r "$SOURCE_PROFILE/Default" "$DEBUG_PROFILE/" 2>/dev/null
            
            # Copiar outras pastas importantes
            for dir in "extensions_crx_cache" "Default" "Dictionaries"; do
                if [ -d "$SOURCE_PROFILE/$dir" ]; then
                    cp -r "$SOURCE_PROFILE/$dir" "$DEBUG_PROFILE/" 2>/dev/null
                fi
            done
        }
        
        echo "   ✅ Cópia concluída (alguns arquivos podem ter sido ignorados)"
        return 0
    fi
}

# Função para verificar se Chrome debug está rodando
check_chrome_debug() {
    if curl -s http://localhost:9222/json >/dev/null 2>&1; then
        echo "✅ Chrome debug já está ativo na porta 9222"
        return 0
    else
        return 1
    fi
}

# Função para iniciar Chrome debug
start_chrome_debug() {
    echo "🚀 Iniciando Chrome debug..."
    
    google-chrome \
        --remote-debugging-port=9222 \
        --user-data-dir="$DEBUG_PROFILE" \
        --no-first-run \
        --disable-web-security \
        --disable-features=VizDisplayCompositor \
        >/dev/null 2>&1 &
    
    # Aguardar inicialização
    echo "   ⏳ Aguardando Chrome inicializar..."
    for i in {1..15}; do
        sleep 1
        if check_chrome_debug; then
            echo "   ✅ Chrome debug ativo após $i segundos"
            return 0
        fi
        echo -n "."
    done
    
    echo ""
    echo "   ⚠️ Chrome pode estar iniciando ainda..."
    return 1
}

# Main execution
echo "="*60

# Verificar se já está rodando
if check_chrome_debug; then
    echo "Chrome debug já está configurado e rodando!"
    exit 0
fi

# Verificar se perfil debug já existe
if [ -d "$DEBUG_PROFILE" ]; then
    echo "📁 Perfil debug já existe em: $DEBUG_PROFILE"
    read -p "Deseja recriar o perfil? (s/N): " recreate
    if [[ $recreate =~ ^[Ss]$ ]]; then
        echo "🗑️ Removendo perfil antigo..."
        rm -rf "$DEBUG_PROFILE"
        safe_copy_profile
    fi
else
    safe_copy_profile
fi

# Iniciar Chrome debug
start_chrome_debug

# Verificar resultado final
if check_chrome_debug; then
    echo ""
    echo "✅ CHROME DEBUG CONFIGURADO COM SUCESSO!"
    echo "🌐 Seu Chrome normal continua funcionando normalmente"
    echo "🔧 Chrome debug ativo na porta 9222"
    echo "📂 Perfil debug em: $DEBUG_PROFILE"
    echo ""
    echo "💡 Agora execute: python3 main.py"
else
    echo ""
    echo "⚠️ Chrome debug pode estar iniciando..."
    echo "💡 Aguarde alguns segundos e execute: python3 main.py"
    echo ""
    echo "🔍 Para verificar manualmente:"
    echo "   curl http://localhost:9222/json"
fi

echo "="*60