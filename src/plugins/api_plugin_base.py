"""
Módulo Base para Plugins de API de Tradução
Define a interface que todos os plugins de API devem implementar
"""

import os
import importlib.util
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class PluginInfo:
    """Informações sobre um plugin de API"""
    name: str
    display_name: str
    description: str
    version: str
    author: str
    requires_api_key: bool
    free_tier_limit: int  # Caracteres por mês no plano gratuito (0 = ilimitado)
    rate_limit: float  # Requisições por segundo


class APIPluginBase(ABC):
    """
    Classe base abstrata para plugins de API de tradução.
    
    Todos os plugins de API devem herdar desta classe e implementar
    os métodos abstratos definidos aqui.
    
    Exemplo de uso:
        class MyAPIPlugin(APIPluginBase):
            def get_info(self) -> PluginInfo:
                return PluginInfo(
                    name="my_api",
                    display_name="My Translation API",
                    description="Plugin para My Translation API",
                    version="1.0.0",
                    author="Seu Nome",
                    requires_api_key=True,
                    free_tier_limit=500000,
                    rate_limit=5.0
                )
            
            def translate(self, text, source_lang, target_lang):
                # Implementação da tradução
                pass
    """
    
    def __init__(self):
        """Inicializa o plugin"""
        self._api_key: Optional[str] = None
        self._enabled: bool = True
        self._config: Dict[str, Any] = {}
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """
        Retorna informações sobre o plugin.
        
        Returns:
            PluginInfo com os dados do plugin
        """
        pass
    
    @abstractmethod
    def translate(self, text: str, source_lang: str = 'en', 
                  target_lang: str = 'pt') -> Optional[str]:
        """
        Traduz um texto usando a API.
        
        Args:
            text: Texto a ser traduzido
            source_lang: Código do idioma de origem (ex: 'en', 'es')
            target_lang: Código do idioma de destino (ex: 'pt', 'pt-br')
            
        Returns:
            Texto traduzido ou None em caso de erro
        """
        pass
    
    @abstractmethod
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                        target_lang: str = 'pt') -> Dict[str, str]:
        """
        Traduz múltiplos textos de uma vez.
        
        Args:
            texts: Lista de textos a serem traduzidos
            source_lang: Código do idioma de origem
            target_lang: Código do idioma de destino
            
        Returns:
            Dicionário {texto_original: texto_traduzido}
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> Tuple[bool, str]:
        """
        Testa a conexão com a API.
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        pass
    
    def set_api_key(self, api_key: str):
        """
        Define a chave de API.
        
        Args:
            api_key: Chave de API
        """
        self._api_key = api_key
    
    def get_api_key(self) -> Optional[str]:
        """Retorna a chave de API configurada"""
        return self._api_key
    
    def is_enabled(self) -> bool:
        """Verifica se o plugin está habilitado"""
        return self._enabled
    
    def set_enabled(self, enabled: bool):
        """Habilita ou desabilita o plugin"""
        self._enabled = enabled
    
    def get_config(self) -> Dict[str, Any]:
        """Retorna a configuração do plugin"""
        return self._config.copy()
    
    def set_config(self, config: Dict[str, Any]):
        """Define a configuração do plugin"""
        self._config = config.copy()
    
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """
        Retorna lista de idiomas suportados.
        
        Returns:
            Lista de tuplas (código, nome) ex: [('en', 'English'), ('pt', 'Portuguese')]
        """
        # Lista padrão - plugins podem sobrescrever
        return [
            ('en', 'English'),
            ('pt', 'Portuguese'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('it', 'Italian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('zh', 'Chinese'),
            ('ru', 'Russian'),
        ]


class PluginManager:
    """
    Gerenciador de plugins de API de tradução.
    
    Responsável por descobrir, carregar e gerenciar plugins de API.
    """
    
    def __init__(self, plugins_dir: str = None):
        """
        Inicializa o gerenciador de plugins.
        
        Args:
            plugins_dir: Diretório onde os plugins estão localizados
        """
        if plugins_dir is None:
            # Diretório padrão: plugins/api dentro do src
            base_dir = os.path.dirname(os.path.abspath(__file__))
            plugins_dir = os.path.join(base_dir, 'api')
        
        self.plugins_dir = plugins_dir
        self._plugins: Dict[str, APIPluginBase] = {}
        self._config_file = os.path.join(plugins_dir, 'plugins_config.json')
        
        # Cria diretório se não existir
        os.makedirs(plugins_dir, exist_ok=True)
        
        # Carrega plugins
        self._discover_plugins()
        self._load_config()
    
    def _discover_plugins(self):
        """Descobre e carrega todos os plugins no diretório"""
        if not os.path.exists(self.plugins_dir):
            return
        
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith('_plugin.py'):
                plugin_path = os.path.join(self.plugins_dir, filename)
                self._load_plugin(plugin_path)
    
    def _load_plugin(self, plugin_path: str) -> bool:
        """
        Carrega um plugin de um arquivo Python.
        
        Args:
            plugin_path: Caminho para o arquivo do plugin
            
        Returns:
            True se carregou com sucesso
        """
        try:
            # Carrega o módulo dinamicamente
            module_name = os.path.basename(plugin_path)[:-3]  # Remove .py
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Procura classes que herdam de APIPluginBase
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, APIPluginBase) and 
                    attr is not APIPluginBase):
                    
                    # Instancia o plugin
                    plugin = attr()
                    info = plugin.get_info()
                    self._plugins[info.name] = plugin
                    print(f"Plugin carregado: {info.display_name} v{info.version}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao carregar plugin {plugin_path}: {e}")
            return False
    
    def _load_config(self):
        """Carrega configurações salvas dos plugins"""
        if not os.path.exists(self._config_file):
            return
        
        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            for plugin_name, plugin_config in config.items():
                if plugin_name in self._plugins:
                    plugin = self._plugins[plugin_name]
                    
                    if 'api_key' in plugin_config:
                        plugin.set_api_key(plugin_config['api_key'])
                    
                    if 'enabled' in plugin_config:
                        plugin.set_enabled(plugin_config['enabled'])
                    
                    if 'config' in plugin_config:
                        plugin.set_config(plugin_config['config'])
                        
        except Exception as e:
            print(f"Erro ao carregar configuração de plugins: {e}")
    
    def save_config(self):
        """Salva configurações dos plugins"""
        config = {}
        
        for name, plugin in self._plugins.items():
            config[name] = {
                'api_key': plugin.get_api_key(),
                'enabled': plugin.is_enabled(),
                'config': plugin.get_config()
            }
        
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configuração de plugins: {e}")
    
    def get_plugin(self, name: str) -> Optional[APIPluginBase]:
        """
        Obtém um plugin pelo nome.
        
        Args:
            name: Nome do plugin
            
        Returns:
            Instância do plugin ou None
        """
        return self._plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, APIPluginBase]:
        """Retorna todos os plugins carregados"""
        return self._plugins.copy()
    
    def get_enabled_plugins(self) -> Dict[str, APIPluginBase]:
        """Retorna apenas os plugins habilitados"""
        return {
            name: plugin 
            for name, plugin in self._plugins.items() 
            if plugin.is_enabled()
        }
    
    def get_plugin_info_list(self) -> List[PluginInfo]:
        """Retorna lista de informações de todos os plugins"""
        return [plugin.get_info() for plugin in self._plugins.values()]
    
    def register_plugin(self, plugin: APIPluginBase) -> bool:
        """
        Registra um plugin manualmente (sem carregar de arquivo).
        
        Args:
            plugin: Instância do plugin
            
        Returns:
            True se registrou com sucesso
        """
        try:
            info = plugin.get_info()
            self._plugins[info.name] = plugin
            return True
        except Exception as e:
            print(f"Erro ao registrar plugin: {e}")
            return False
    
    def unregister_plugin(self, name: str) -> bool:
        """
        Remove um plugin do gerenciador.
        
        Args:
            name: Nome do plugin
            
        Returns:
            True se removeu com sucesso
        """
        if name in self._plugins:
            del self._plugins[name]
            return True
        return False
    
    def reload_plugins(self):
        """Recarrega todos os plugins do diretório"""
        self._plugins.clear()
        self._discover_plugins()
        self._load_config()
