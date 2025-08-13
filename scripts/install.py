# install_requirements.py - Script de instalação das dependências
"""
Script para instalar todas as dependências necessárias para o sistema de voz
Execute este arquivo primeiro antes de usar os módulos
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala um pacote usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Erro ao instalar {package}")
        return False

def check_system_requirements():
    """Verifica requisitos do sistema"""
    print("Verificando requisitos do sistema...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("✗ Python 3.7+ é necessário")
        return False
    else:
        print(f"✓ Python {python_version.major}.{python_version.minor}")
    
    # Verificar sistema operacional
    import platform
    system = platform.system()
    print(f"✓ Sistema operacional: {system}")
    
    if system == "Linux":
        print("Nota: No Linux, você pode precisar instalar:")
        print("  sudo apt-get install portaudio19-dev python3-pyaudio")
        print("  sudo apt-get install espeak espeak-data")
    
    return True

def install_all_requirements():
    """Instala todas as dependências necessárias"""
    
    print("=== INSTALAÇÃO DO SISTEMA DE VOZ BRASILEIRO ===\n")
    
    if not check_system_requirements():
        return False
    
    # Lista de pacotes necessários
    packages = [
        "pyttsx3",           # Síntese de voz
        "SpeechRecognition", # Reconhecimento de voz
        "pyaudio",          # Interface de áudio
        "requests",         # Para requisições HTTP (usado pelo SpeechRecognition)
    ]
    
    print(f"\nInstalando {len(packages)} pacotes necessários...\n")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
        print()
    
    print(f"Instalação concluída: {success_count}/{len(packages)} pacotes instalados com sucesso")
    
    if success_count == len(packages):
        print("\n✓ Todas as dependências foram instaladas com sucesso!")
        print("\nPróximos passos:")
        print("1. Execute 'python voice_manager.py' para testar o sistema")
        print("2. Configure vozes brasileiras no seu sistema operacional")
        print("3. Teste o microfone e ajuste as configurações se necessário")
        return True
    else:
        print(f"\n✗ {len(packages) - success_count} pacotes falharam na instalação")
        print("Verifique os erros acima e tente instalar manualmente")
        return False

def create_requirements_txt():
    """Cria arquivo requirements.txt"""
    requirements_content = """# Sistema de Voz Brasileiro - Dependências
# Instale com: pip install -r requirements.txt

pyttsx3>=2.90
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
requests>=2.25.1
"""
    
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements_content)
        print("✓ Arquivo requirements.txt criado")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar requirements.txt: {e}")
        return False

def test_installation():
    """Testa se as instalações funcionaram"""
    print("\nTestando instalação...")
    
    modules_to_test = [
        ("pyttsx3", "Síntese de voz"),
        ("speech_recognition", "Reconhecimento de voz"),
        ("pyaudio", "Interface de áudio"),
    ]
    
    all_working = True
    for module, description in modules_to_test:
        try:
            __import__(module)
            print(f"✓ {description} - OK")
        except ImportError as e:
            print(f"✗ {description} - ERRO: {e}")
            all_working = False
    
    if all_working:
        print("\n✓ Todos os módulos foram instalados corretamente!")
        
        # Teste básico do TTS
        try:
            import pyttsx3
            engine = pyttsx3.init()
            print("✓ Engine de síntese de voz inicializada")
            engine.stop()
        except Exception as e:
            print(f"⚠ Aviso: Problema com engine de voz: {e}")
        
        # Teste básico do microfone
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            mic = sr.Microphone()
            print("✓ Microfone inicializado")
        except Exception as e:
            print(f"⚠ Aviso: Problema com microfone: {e}")
            
    else:
        print("\n✗ Alguns módulos não foram instalados corretamente")
        print("Tente instalar manualmente os módulos com erro")
    
    return all_working

def show_configuration_tips():
    """Mostra dicas de configuração"""
    print("\n=== DICAS DE CONFIGURAÇÃO ===")
    
    import platform
    system = platform.system()
    
    if system == "Windows":
        print("\nWindows:")
        print("• Vozes brasileiras estão disponíveis em 'Configurações > Hora e idioma > Fala'")
        print("• Instale 'Microsoft Speech Platform' para mais vozes")
        print("• Verifique se o microfone está habilitado nas configurações de privacidade")
        
    elif system == "macOS":
        print("\nmacOS:")
        print("• Vá em 'Preferências do Sistema > Acessibilidade > Fala'")
        print("• Baixe vozes em português em 'Voz do sistema'")
        print("• Verifique permissões do microfone em 'Segurança e Privacidade'")
        
    elif system == "Linux":
        print("\nLinux:")
        print("• Instale vozes do espeak: sudo apt-get install espeak-data")
        print("• Para vozes melhores: sudo apt-get install festival festvox-kallpc16k")
        print("• Teste microfone: arecord -d 5 test.wav && aplay test.wav")
    
    print("\nDicas gerais:")
    print("• Use um microfone de boa qualidade para melhor reconhecimento")
    print("• Fale claramente e não muito rápido")
    print("• Execute em ambiente com pouco ruído de fundo")
    print("• Teste os comandos básicos antes de adicionar comandos personalizados")

def create_example_script():
    """Cria script de exemplo"""
    example_content = '''#!/usr/bin/env python3
# exemplo_uso.py - Exemplo de uso do sistema de voz

"""
Exemplo básico de como usar o sistema de voz brasileiro
Execute este arquivo após instalar as dependências
"""

import time
from voice_manager import VoiceManager

def main():
    # Criar instância do gerenciador
    voice = VoiceManager()
    
    # Saudar usuário
    voice.speak("Olá! Sistema de voz brasileiro inicializado.")
    
    # Definir comandos personalizados
    def apresentar_sistema():
        voice.speak("Este é um sistema de reconhecimento e síntese de voz em português brasileiro.")
        voice.speak("Você pode dizer comandos como: olá, que horas são, volume alto, ou parar.")
    
    def contar_regressiva():
        voice.speak("Iniciando contagem regressiva")
        for i in range(5, 0, -1):
            voice.speak(str(i))
            time.sleep(1)
        voice.speak("Zero! Contagem concluída.")
    
    def informacoes_sistema():
        commands = voice.get_available_commands()
        voice.speak(f"Tenho {len(commands)} comandos disponíveis.")
        voice.speak("Diga 'comandos' para ouvir todos.")
    
    # Registrar comandos
    voice.register_command("apresentar", apresentar_sistema)
    voice.register_command("apresentação", apresentar_sistema)
    voice.register_command("contagem", contar_regressiva)
    voice.register_command("informações", informacoes_sistema)
    voice.register_command("info", informacoes_sistema)
    
    # Iniciar sistema
    try:
        voice.start_listening()
        
        # Manter ativo até ser interrompido
        print("Sistema ativo. Pressione Ctrl+C para encerrar.")
        while voice.is_listening:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\\nEncerrando...")
        voice.stop_listening()

if __name__ == "__main__":
    main()
'''
    
    try:
        with open("exemplo_uso.py", "w", encoding="utf-8") as f:
            f.write(example_content)
        print("✓ Arquivo exemplo_uso.py criado")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar exemplo_uso.py: {e}")
        return False

def main():
    """Função principal do instalador"""
    print("Iniciando instalação do Sistema de Voz Brasileiro...")
    
    # Instalar dependências
    if not install_all_requirements():
        print("\nInstalação falhou. Verifique os erros acima.")
        return
    
    # Criar arquivos auxiliares
    create_requirements_txt()
    create_example_script()
    
    # Testar instalação
    if test_installation():
        show_configuration_tips()
        
        print("\n" + "="*50)
        print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! 🎉")
        print("="*50)
        print("\nArquivos criados:")
        print("• voice_manager.py - Módulo principal")
        print("• text_to_speech.py - Síntese de voz")
        print("• speech_recognition_br.py - Reconhecimento de voz")
        print("• requirements.txt - Lista de dependências")
        print("• exemplo_uso.py - Exemplo de uso")
        print("\nPara começar:")
        print("python exemplo_uso.py")
        
    else:
        print("\n❌ Instalação completada com problemas")
        print("Verifique as mensagens de erro acima")

if __name__ == "__main__":
    main()