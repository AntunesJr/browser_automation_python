# ==============================================
# authenticator/config/config_manager.py
# version: 0.0.1
# author: silvioantunes1@hotmail.com
# ==============================================

# Copyright (C) 2025 Silvio Antunes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig, SECURE_FILE_MODE, SECURE_DIR_MODE

# EN: { Name of the file that stores the saved settings. }
# PT: { Nome do arquivo que armazena as configurações salvas. }
# ES: { Nombre del archivo que almacena las configuraciones guardadas. }
CONFIGS_REGISTRY_FILE = 'configs_registry.json'

@dataclass
class ConfigInfo:
    """EN: { Information for configuration records. }"""
    """PT: { Informações para registros de configuração. }"""
    """ES: { Información para registros de configuración. }"""
    name: str
    base_directory: str
    folder_name: str
    credentials_filename: str
    key_filename: str
    created_at: str
    last_used: Optional[str] = None
    description: Optional[str] = None

class ConfigManager:
    """EN: { File manager for credentials and directory names. }"""
    """PT: { Gerenciador de arquivos das credenciais e nomes de diretórios. }"""
    """ES: { Administrador de archivos para credenciales y nombres de directorios. }"""

    def __init__(self, registry_base_dir: Optional[ Path ] = None) -> None:
        """
        EN: {
            Initializes the configuration manager.
            Args:
                registry_base_dir: Base directory to save the configuration registry
                                  (default: ~/.credentials_manager).
        }
        PT: {
            Inicializa o gerenciador de configuração.
            Argumentos:
                registry_base_dir: Diretório base para salvar o registro de configuração
                                  (padrão: ~/.credentials_manager).
        }
        ES: {
            Inicializa el administrador de configuración.
            Argumentos:
                registry_base_dir: Directorio base donde se guarda el registro de configuración
                                  (patrón: ~/.credentials_manager).
        }
        """
        self._registry_base_dir = registry_base_dir or ( Path.home() / '.credentials_manager' )
        self._registry_file = self._registry_base_dir / CONFIGS_REGISTRY_FILE
        self._configs: Dict[ str, ConfigInfo ] = {}
        
        # EN: { Initializes the directory and loads existing configurations. }
        # PT: { Inicializa o diretório e carrega as configurações existentes. }
        # ES: { Inicializa el directorio y carga las configuraciones existentes. }
        self._initialize_registry()
        self._load_configs()
    
    def _initialize_registry(self) -> MsgCode:
        """EN: { Initializes the configuration registry directory. }"""
        """PT: { Inicializa o diretório de registro de configuração. }"""
        """ES: { Inicializa el directorio de registro de configuración. }"""
        try:
            self._registry_base_dir.mkdir( mode=SECURE_DIR_MODE, exist_ok=True )
            return MsgCode.SUCCESS
        except PermissionError:
            return MsgCode.PERMISSION_DIR_ERROR
        except OSError:
            return MsgCode.IO_DIR_ERROR
        except Exception:
            return MsgCode.UNKNOWN_DIR_ERROR
    
    def _load_configs(self) -> MsgCode:
        """EN: { Loads saved settings from the registry file. }"""
        """PT: { Carrega configurações salvas do arquivo de registro. }"""
        """ES: { Carga la configuración guardada del archivo de registro. }"""
        try:
            if self._registry_file.exists():
                with open( self._registry_file, 'r', encoding='utf-8' ) as f:
                    data = json.load( f )
                    self._configs = {
                        name: ConfigInfo( **config_data ) 
                        for name, config_data in data.items()
                    }
            return MsgCode.SUCCESS
        except ( FileNotFoundError, json.JSONDecodeError ):
            # EN: { If the file does not exist or is corrupted, it starts with empty configs. }
            # PT: { Se o arquivo não existir ou estiver corrompido, ele começará com configurações vazias. }
            # EN: { Si el archivo no existe o está corrupto, comenzará con la configuración vacía. }
            self._configs = {}
            return MsgCode.SUCCESS
        except Exception:
            return MsgCode.UNKNOWN_CREDENTIALS_FILE_ERROR
    
    def _save_configs(self) -> MsgCode:
        """Saves settings to registry file."""
        try:
            data = { name: asdict( config ) for name, config in self._configs.items() }
            with open( self._registry_file, 'w', encoding='utf-8' ) as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.chmod( self._registry_file, SECURE_FILE_MODE )
            return MsgCode.SUCCESS
        except Exception:
            return MsgCode.UNKNOWN_CREATE_CREDENTIALS_FILE_ERROR
    
    def register_config(
        self,
        name: str,
        base_directory: Optional[ Path ] = None,
        folder_name: Optional[ str ] = None,
        credentials_filename: Optional[ str ] = None,
        key_filename: Optional[ str ] = None,
        description: Optional[ str ] = None
    ) -> Tuple[ MsgCode, Optional[ CredentialsConfig ] ]:
        """
        EN: {
            Registers a new configuration.
            Args:
                name: Unique name to identify the configuration.
                base_directory: Base directory for the credentials folder.
                folder_name: Name of the credentials folder.
                credentials_filename: Name of the credentials file.
                key_filename: Name of the key file.
                description: Optional description of the configuration.
            Returns:
                Tuple containing:
                    - MsgCode: Status of the operation.
                    - CredentialsConfig: Configuration created (or None in case of error).
        }
        PT: { 
            Registra uma nova configuração.
            Argumentos:
                name: Nome único para identificar a configuração.
                base_directory: Diretório base para a pasta de credenciais.
                folder_name: Nome da pasta de credenciais.
                credentials_filename: Nome do arquivo de credenciais.
                key_filename: Nome do arquivo de chave.
                description: Descrição opcional da configuração.
            Retornos:
                Tuple contendo:
                    - MsgCode: Status da operação.
                    - CredentialsConfig: Configuração criada (ou None em caso de erro).
        }
        ES: {
            Registra una nueva configuración.
            Argumentos:
                name: Nombre único para identificar la configuración.
                base_directory: Directorio base de la carpeta de credenciales.
                folder_name: Nombre de la carpeta de credenciales.
                credentials_filename: Nombre del archivo de credenciales.
                key_filename: Nombre del archivo de claves.
                description: Descripción opcional de la configuración.
            Devuelve:
                Tupla que contiene:
                    - MsgCode: Estado de la operación.
                    - CredentialsConfig: Configuración creada (o None en caso de error).
        }
        """
        if name in self._configs:
            return MsgCode.CONFIG_ALREADY_EXISTS, None
        
        # EN: { Creates the configuration. }
        # PT: { Cria a configuração. }
        # ES: { Crea la configuración. }
        config = CredentialsConfig(
            base_directory=base_directory,
            folder_name=folder_name,
            credentials_filename=credentials_filename,
            key_filename=key_filename
        )
        
        # EN: { Creates the configuration info. }
        # PT: { Cria o info da configuração. }
        # EN: { Crea la info de configuración. }
        config_info = ConfigInfo(
            name=name,
            base_directory=str( config.credentials_dir.parent ),
            folder_name=config.credentials_dir.name,
            credentials_filename=config.credentials_file.name,
            key_filename=config.key_file.name,
            created_at=datetime.now().isoformat(),
            description=description
        )
        
        #EN: { Receives the configuration. }
        #PT: { Recebe a configuração. }
        #ES: { { Recibe la configuración. }
        self._configs[ name ] = config_info
        
        #EN: { Save to file. }
        #PT: { Salva no arquivo. }
        #ES: { Almacena en archivo. }
        save_status = self._save_configs()
        if save_status != MsgCode.SUCCESS:
            #EN { Delete from memory if you cannot save. }
            #PT { Remove da memória se não conseguir salvar. }
            #ES { Eliminar de la memoria si no se puede almacenar. }
            del self._configs[ name ]
            return save_status, None
        
        return MsgCode.SUCCESS, config
    
    def get_config( self, name: str ) -> Tuple[ MsgCode, Optional[ CredentialsConfig ] ]:
        """
        EN: {
            Gets a configuration by name.
            Arguments:
                name: Configuration name.
            Returns:
                Tuple containing:
                    - MsgCode: Operation status
                    - CredentialsConfig: Configuration (or None if not found).
        }
        PT: {
            Obtém uma configuração pelo nome.
            Argumentos:
                name: Nome da configuração.
            Retornos:
                Tuple contendo:
                    - MsgCode: Status da operação
                    - CredentialsConfig: Configurações (ou None se não encontrada).
        }
        ES: {
            Obtiene una configuración por nombre.
            Argumentos:
                name: Nombre de la configuración.
            Devuelve:
                Tupla que contiene:
                    - MsgCode: Estado de la operación
                    - CredentialsConfig: Configuración (o Ninguna si no se encuentra).
        }
        """
        if name not in self._configs:
            return MsgCode.CONFIG_NOT_FOUND, None
        
        config_info = self._configs[ name ]
        
        # EN: { Update last used. }
        # PT: { Atualiza o último uso. }
        # ES: { Actualizar último uso. }
        config_info.last_used = datetime.now().isoformat()
        self._save_configs()
        
        #EN: { Creates and returns the configuration. }
        #PT: { Cria e retorna a configuração. }
        #ES: { Crea y devuelve la configuración. }
        config = CredentialsConfig(
            base_directory=Path( config_info.base_directory ),
            folder_name=config_info.folder_name,
            credentials_filename=config_info.credentials_filename,
            key_filename=config_info.key_filename
        )
        
        return MsgCode.SUCCESS, config
    
    def list_configs( self ) -> List[ ConfigInfo ]:
        """
        EN: {
            Lists all registered configurations.
            Returns:
                List of configuration information
        }
        PT: {
            Lista todas as configurações registradas.
            Retornos:
                Lista de informações das configurações
        }
        """
        return list( self._configs.values() )
    
    def remove_config(self, name: str) -> MsgCode:
        """
        Remove uma configuração do registro.
        Args:
            name: Nome da configuração a ser removida
        Returns:
            MsgCode: Status da operação
        """
        if name not in self._configs:
            return MsgCode.CONFIG_NOT_FOUND
        
        del self._configs[name]
        return self._save_configs()
    
    def check_config_exists(self, name: str) -> Tuple[MsgCode, bool, Optional[Dict[str, bool]]]:
        """
        Verifica se uma configuração existe e se seus arquivos estão presentes.
        Args:
            name: Nome da configuração
        Returns:
            Tuple contendo:
                - MsgCode: Status da operação
                - bool: Se a configuração está registrada
                - dict: Status dos arquivos (directory_exists, credentials_exists, key_exists)
        """
        if name not in self._configs:
            return MsgCode.CONFIG_NOT_FOUND, False, None
        
        config_info = self._configs[name]
        base_path = Path(config_info.base_directory)
        credentials_dir = base_path / config_info.folder_name
        credentials_file = credentials_dir / config_info.credentials_filename
        key_file = credentials_dir / config_info.key_filename
        
        status = {
            'directory_exists': credentials_dir.exists() and credentials_dir.is_dir(),
            'credentials_exists': credentials_file.exists() and credentials_file.is_file(),
            'key_exists': key_file.exists() and key_file.is_file()
        }
        
        return MsgCode.SUCCESS, True, status
    
    def check_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Verifica o status de todas as configurações registradas.
        Returns:
            Dicionário com informações de status de cada configuração
        """
        results = {}
        
        for name in self._configs:
            status_code, exists, file_status = self.check_config_exists(name)
            results[name] = {
                'registered': exists,
                'status_code': status_code,
                'files': file_status,
                'config_info': self._configs[name]
            }
        
        return results
    
    def update_config_description(self, name: str, description: str) -> MsgCode:
        """
        Atualiza a descrição de uma configuração.
        Args:
            name: Nome da configuração
            description: Nova descrição
        Returns:
            MsgCode: Status da operação
        """
        if name not in self._configs:
            return MsgCode.CONFIG_NOT_FOUND
        
        self._configs[name].description = description
        return self._save_configs()