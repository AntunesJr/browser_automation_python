# ==============================================
# authenticator/Credentials.py
# version: 0.1.0
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

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List

from credentials.message.msg_code import MsgCode
from credentials.config.config import CredentialsConfig
from credentials.config.config_manager import ConfigManager, ConfigInfo
from credentials.core.credentials_checker import CredentialsChecker
from credentials.crypto.crypto_manager import CryptoManager
from credentials.core.credentials_reader import CredentialsReader

class Credentials:
    """Core Credential Manager"""

    def __init__(
        self,
        config_name: Optional[ str ] = None,
        base_directory: Optional[ Path ] = None,
        folder_name: Optional[ str ] = None,
        credentials_filename: Optional[ str ] = None,
        key_filename: Optional[ str ] = None
    ) -> None:
        """
        Initializes the credential manager.
        Args:
            config_name: Name of a saved configuration (if provided, other parameters are ignored)
            base_directory: Base directory for the credentials folder (default: home)
            folder_name: Name of the credentials folder (default: .credentials)
            credentials_filename: Name of the credentials file (default: credentials.enc)
            key_filename: Name of the key file (default: key.key)
        """
    
        self._config_manager = ConfigManager()

        if config_name:
            # Use saved configuration
            status, config = self._config_manager.get_config( config_name )
            if status != MsgCode.SUCCESS or not config:
                raise ValueError(f"Configuração '{config_name}' não encontrada")
            self._config = config
            self._current_config_name = config_name
        else:
            # Create new configuration
            self._config = CredentialsConfig(
                base_directory=base_directory,
                folder_name=folder_name,
                credentials_filename=credentials_filename,
                key_filename=key_filename
            )
            self._current_config_name = None
        
        # Initializes components
        self._checker = CredentialsChecker( self._config )
        self._crypto_manager = CryptoManager( self._config )
        self._reader = CredentialsReader( self._config )

    def save_current_config(self, name: str, description: Optional[str] = None) -> MsgCode:
        """
        Salva a configuração atual no registro.
        Args:
            name: Nome para identificar a configuração
            description: Descrição opcional
        Returns:
            MsgCode: Status da operação
        """
        status, _ = self._config_manager.register_config(
            name=name,
            base_directory=self._config.credentials_dir.parent,
            folder_name=self._config.credentials_dir.name,
            credentials_filename=self._config.credentials_file.name,
            key_filename=self._config.key_file.name,
            description=description
        )
        
        if status == MsgCode.SUCCESS:
            self._current_config_name = name
        
        return status
    
    def load_config(self, name: str) -> MsgCode:
        """
        Carrega uma configuração salva.
        Args:
            name: Nome da configuração
        Returns:
            MsgCode: Status da operação
        """
        status, config = self._config_manager.get_config(name)
        if status != MsgCode.SUCCESS or not config:
            return status
        
        # Atualiza configuração e componentes
        self._config = config
        self._current_config_name = name
        self._checker = CredentialsChecker(self._config)
        self._crypto_manager = CryptoManager(self._config)
        self._reader = CredentialsReader(self._config)
        
        return MsgCode.SUCCESS
    
    def list_saved_configs(self) -> List[ ConfigInfo ]:
        """
        Lista todas as configurações salvas.
        Returns:
            Lista de informações das configurações
        """
        return self._config_manager.list_configs()
    
    def check_config_status(self, config_name: Optional[str] = None) -> Tuple[MsgCode, Optional[Dict[str, Any]]]:
        """
        Verifica o status de uma configuração (atual ou especificada).
        Args:
            config_name: Nome da configuração (None para atual)
        Returns:
            Tuple contendo:
                - MsgCode: Status da operação
                - dict: Informações de status
        """
        if config_name is None:
            # Verifica configuração atual
            if self._current_config_name:
                return self._config_manager.check_config_exists(self._current_config_name)
            else:
                # Para configuração não salva, verifica manualmente
                status = {
                    'directory_exists': self._config.credentials_dir.exists(),
                    'credentials_exists': self._config.credentials_file.exists(),
                    'key_exists': self._config.key_file.exists()
                }
                return MsgCode.SUCCESS, status
        else:
            # Verifica configuração específica
            return self._config_manager.check_config_exists(config_name)
    
    def check_all_configs_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Verifica o status de todas as configurações salvas.
        Returns:
            Dicionário com status de todas as configurações
        """
        return self._config_manager.check_all_configs()
    
    def remove_saved_config(self, name: str) -> MsgCode:
        """
        Remove uma configuração do registro.
        Args:
            name: Nome da configuração
        Returns:
            MsgCode: Status da operação
        """
        return self._config_manager.remove_config(name)

    # Métodos originais mantidos para compatibilidade
    def checker(self) -> Tuple[MsgCode, MsgCode, MsgCode]:
        msg00 = self._checker.check_directory()
        if msg00 != MsgCode.SUCCESS:
            return msg00, MsgCode.CREDENTIALS_NULL, MsgCode.PROVIDED_KEY_NULL
        
        msg01 = self._checker.check_credentials_file()
        msg02 = self._checker.check_key_file()
        return msg00, msg01, msg02

    def create_credentials(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
        key_password: Optional[str] = None
    ) -> MsgCode:
        # Garante que o diretório existe
        ensure_status = self._config.ensure_secure_directory()
        if ensure_status != MsgCode.SUCCESS:
            return ensure_status
        
        # Gera e salva chave
        key_status, key = self._crypto_manager.create_key(key_password)
        if key_status != MsgCode.SUCCESS or not key:
            return key_status or MsgCode.CREATE_KEY_ERROR
        
        save_key_status = self._crypto_manager.save_key(key)
        if save_key_status != MsgCode.SUCCESS:
            return save_key_status
        
        # Prepara dados das credenciais
        credentials_data = {
            'username': username,
            'email': email,
            'password': password,
            'additional_data': additional_data or {}
        }
        
        # Criptografa dados
        encrypt_status, encrypted_data = self._crypto_manager.encrypt_data(credentials_data)
        if encrypt_status != MsgCode.SUCCESS or not encrypted_data:
            return encrypt_status or MsgCode.ENCRYPTION_ERROR
        
        # Salva dados criptografados
        return self._crypto_manager.save_encrypted_data(encrypted_data)
    
    def check_config_status(self, config_name: Optional[str] = None) -> Tuple[MsgCode, Optional[Dict[str, Any]]]:
        """
        Verifica o status de uma configuração (atual ou especificada).
        Args:
           config_name: Nome da configuração (None para atual)
        Returns:
           Tuple contendo:
               - MsgCode: Status da operação
               - dict: Informações de status
        """
        if config_name is None:
            # Verifica configuração atual
            if self._current_config_name:
                return self._config_manager.check_config_exists(self._current_config_name)
            else:
                # Para configuração não salva, verifica manualmente
                status = {
                    'directory_exists': self._config.credentials_dir.exists(),
                    'credentials_exists': self._config.credentials_file.exists(),
                    'key_exists': self._config.key_file.exists()
                }
                return MsgCode.SUCCESS, status
        else:
            # Verifica configuração específica
            status_code, exists, file_status = self._config_manager.check_config_exists(config_name)
            return status_code, file_status

    def check_all_configs_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Verifica o status de todas as configurações salvas.
        Returns:
            Dicionário com status de todas as configurações
        """
        return self._config_manager.check_all_configs()

    # Outros métodos originais mantidos...
    def load_credentials(self) -> Tuple[MsgCode, Optional[Dict[str, Any]]]:
        return self._reader._read_credentials()

    def verify_credentials(self, email: str, password: str) -> MsgCode:
        return self._reader.verify_login(email, password)

    def get_username(self) -> Tuple[MsgCode, Optional[str]]:
        return self._reader.get_username()
    
    def get_email(self) -> Tuple[MsgCode, Optional[str]]:
        return self._reader.get_email()
    
    def get_password(self) -> Tuple[MsgCode, Optional[str]]:
        return self._reader.get_password()
    
    def get_additional_data(self) -> Tuple[MsgCode, Optional[Dict[str, Any]]]:
        return self._reader.get_additional_data()
    
    def get_credential_field(self, field_name: str) -> Tuple[MsgCode, Optional[Any]]:
        return self._reader.get_credential_field(field_name)
    
    # Propriedades de configuração
    @property
    def credentials_file_path(self) -> Path:
        return self._config.credentials_file
    
    @property
    def key_file_path(self) -> Path:
        return self._config.key_file
    
    @property
    def credentials_directory(self) -> Path:
        return self._config.credentials_dir
    
    @property
    def current_config_name(self) -> Optional[str]:
        return self._current_config_name

    @property
    def config_manager(self):
       """Acesso ao gerenciador de configurações."""
       return self._config_manager