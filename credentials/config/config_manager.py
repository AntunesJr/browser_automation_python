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

# Nome do arquivo que armazena as configurações salvas
CONFIGS_REGISTRY_FILE = 'configs_registry.json'

@dataclass
class ConfigInfo:
    """Informações sobre uma configuração salva."""
    name: str
    base_directory: str
    folder_name: str
    credentials_filename: str
    key_filename: str
    created_at: str
    last_used: Optional[str] = None
    description: Optional[str] = None

class ConfigManager:
    """Gerenciador de múltiplas configurações de credenciais."""
    
    def __init__(self, registry_base_dir: Optional[Path] = None) -> None:
        """
        Inicializa o gerenciador de configurações.
        Args:
            registry_base_dir: Diretório base para salvar o registro de configurações
                             (default: ~/.credentials_manager)
        """
        self._registry_base_dir = registry_base_dir or (Path.home() / '.credentials_manager')
        self._registry_file = self._registry_base_dir / CONFIGS_REGISTRY_FILE
        self._configs: Dict[str, ConfigInfo] = {}
        
        # Inicializa o diretório e carrega configurações existentes
        self._initialize_registry()
        self._load_configs()
    
    def _initialize_registry(self) -> MsgCode:
        """Inicializa o diretório de registro de configurações."""
        try:
            self._registry_base_dir.mkdir(mode=SECURE_DIR_MODE, exist_ok=True)
            return MsgCode.SUCCESS
        except PermissionError:
            return MsgCode.PERMISSION_DIR_ERROR
        except OSError:
            return MsgCode.IO_DIR_ERROR
        except Exception:
            return MsgCode.UNKNOWN_DIR_ERROR
    
    def _load_configs(self) -> MsgCode:
        """Carrega configurações salvas do arquivo de registro."""
        try:
            if self._registry_file.exists():
                with open(self._registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._configs = {
                        name: ConfigInfo(**config_data) 
                        for name, config_data in data.items()
                    }
            return MsgCode.SUCCESS
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existe ou está corrompido, inicia com configs vazias
            self._configs = {}
            return MsgCode.SUCCESS
        except Exception:
            return MsgCode.UNKNOWN_CREDENTIALS_FILE_ERROR
    
    def _save_configs(self) -> MsgCode:
        """Salva configurações no arquivo de registro."""
        try:
            data = {name: asdict(config) for name, config in self._configs.items()}
            with open(self._registry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.chmod(self._registry_file, SECURE_FILE_MODE)
            return MsgCode.SUCCESS
        except Exception:
            return MsgCode.UNKNOWN_CREATE_CREDENTIALS_FILE_ERROR
    
    def register_config(
        self,
        name: str,
        base_directory: Optional[Path] = None,
        folder_name: Optional[str] = None,
        credentials_filename: Optional[str] = None,
        key_filename: Optional[str] = None,
        description: Optional[str] = None
    ) -> Tuple[MsgCode, Optional[CredentialsConfig]]:
        """
        Registra uma nova configuração.
        Args:
            name: Nome único para identificar a configuração
            base_directory: Diretório base para a pasta de credenciais
            folder_name: Nome da pasta de credenciais
            credentials_filename: Nome do arquivo de credenciais
            key_filename: Nome do arquivo de chave
            description: Descrição opcional da configuração
        Returns:
            Tuple contendo:
                - MsgCode: Status da operação
                - CredentialsConfig: Configuração criada (ou None em caso de erro)
        """
        if name in self._configs:
            return MsgCode.CONFIG_ALREADY_EXISTS, None
        
        # Cria a configuração
        config = CredentialsConfig(
            base_directory=base_directory,
            folder_name=folder_name,
            credentials_filename=credentials_filename,
            key_filename=key_filename
        )
        
        # Cria o info da configuração
        config_info = ConfigInfo(
            name=name,
            base_directory=str(config.credentials_dir.parent),
            folder_name=config.credentials_dir.name,
            credentials_filename=config.credentials_file.name,
            key_filename=config.key_file.name,
            created_at=datetime.now().isoformat(),
            description=description
        )
        
        # Registra a configuração
        self._configs[name] = config_info
        
        # Salva no arquivo
        save_status = self._save_configs()
        if save_status != MsgCode.SUCCESS:
            # Remove da memória se não conseguiu salvar
            del self._configs[name]
            return save_status, None
        
        return MsgCode.SUCCESS, config
    
    def get_config(self, name: str) -> Tuple[MsgCode, Optional[CredentialsConfig]]:
        """
        Obtém uma configuração pelo nome.
        Args:
            name: Nome da configuração
        Returns:
            Tuple contendo:
                - MsgCode: Status da operação
                - CredentialsConfig: Configuração (ou None se não encontrada)
        """
        if name not in self._configs:
            return MsgCode.CONFIG_NOT_FOUND, None
        
        config_info = self._configs[name]
        
        # Atualiza o último uso
        config_info.last_used = datetime.now().isoformat()
        self._save_configs()
        
        # Cria e retorna a configuração
        config = CredentialsConfig(
            base_directory=Path(config_info.base_directory),
            folder_name=config_info.folder_name,
            credentials_filename=config_info.credentials_filename,
            key_filename=config_info.key_filename
        )
        
        return MsgCode.SUCCESS, config
    
    def list_configs(self) -> List[ConfigInfo]:
        """
        Lista todas as configurações registradas.
        Returns:
            Lista de informações das configurações
        """
        return list(self._configs.values())
    
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