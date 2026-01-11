"""
Módulo de Gerenciamento de Perfis de Regex
Permite criar, editar e aplicar perfis personalizados de extração de texto

PERSISTÊNCIA DE PERFIS:
- Cada perfil é salvo automaticamente como arquivo JSON no diretório 'profiles/'
- O nome do arquivo é derivado do nome do perfil (slugificado para evitar problemas)
- Na inicialização, todos os arquivos .json do diretório são carregados automaticamente
- Suporta importação e exportação de perfis para compartilhamento
"""

import json
import os
import re
import shutil
import unicodedata
from typing import List, Dict, Optional


def slugify(text: str) -> str:
    """
    Converte texto em um slug seguro para nome de arquivo
    
    Remove acentos, converte para minúsculas, substitui espaços por hífens
    e remove caracteres especiais que podem causar problemas em nomes de arquivo.
    
    NOTA: Permite números e underscores no resultado (parte de \w)
    Isso é intencional para suportar perfis como "v2.0" ou "my_profile"
    
    Args:
        text: Texto a ser convertido
        
    Returns:
        Texto slugificado seguro para uso em nomes de arquivo
        
    Examples:
        >>> slugify("JSON Genérico")
        'json-generico'
        >>> slugify("Bannerlord XML")
        'bannerlord-xml'
        >>> slugify("Profile v2.0")
        'profile-v20'
    """
    # Remove acentos (normalização NFD + remoção de marcas diacríticas)
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    # Converte para minúsculas
    text = text.lower()
    
    # Substitui espaços e caracteres inválidos por hífen
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # Remove hífens do início e fim
    text = text.strip('-')
    
    return text


class RegexProfile:
    """Representa um perfil de regex para extração de texto"""
    
    def __init__(self, name: str, description: str = "", 
                 capture_patterns: List[str] = None,
                 exclude_patterns: List[str] = None,
                 file_type: str = "json"):
        """
        Inicializa um perfil de regex
        
        Args:
            name: Nome do perfil
            description: Descrição do perfil
            capture_patterns: Lista de padrões regex para capturar texto
            exclude_patterns: Lista de padrões regex para excluir texto
            file_type: Tipo de arquivo (json ou xml)
        """
        self.name = name
        self.description = description
        self.capture_patterns = capture_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.file_type = file_type
    
    def to_dict(self) -> dict:
        """Converte o perfil para dicionário"""
        return {
            'name': self.name,
            'description': self.description,
            'capture_patterns': self.capture_patterns,
            'exclude_patterns': self.exclude_patterns,
            'file_type': self.file_type
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RegexProfile':
        """Cria um perfil a partir de um dicionário"""
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            capture_patterns=data.get('capture_patterns', []),
            exclude_patterns=data.get('exclude_patterns', []),
            file_type=data.get('file_type', 'json')
        )

class RegexProfileManager:
    """Gerencia perfis de regex com persistência em arquivos JSON"""
    
    def __init__(self, profiles_dir: str = "profiles"):
        """
        Inicializa o gerenciador de perfis
        
        COMPORTAMENTO DE PERSISTÊNCIA:
        1. Cria o diretório de perfis se não existir
        2. Cria perfis padrão como arquivos .json (se não existirem)
        3. Carrega automaticamente todos os perfis .json do diretório
        
        Args:
            profiles_dir: Diretório para armazenar perfis (padrão: "profiles")
        """
        self.profiles_dir = profiles_dir
        self.profiles: Dict[str, RegexProfile] = {}
        
        # MUDANÇA: Cria diretório se não existir (garante persistência)
        os.makedirs(profiles_dir, exist_ok=True)
        
        # Carrega perfis salvos primeiro (para manter compatibilidade)
        self.load_all_profiles()
        
        # Cria perfis padrão apenas se não existirem
        self._create_default_profiles()
    
    def _get_profile_filepath(self, profile_name: str) -> str:
        """
        Obtém o caminho do arquivo para um perfil
        
        MUDANÇA: Agora usa slugificação para nomes de arquivo seguros
        Isso evita problemas com caracteres especiais em diferentes sistemas operacionais
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            Caminho completo do arquivo JSON do perfil
        """
        filename = slugify(profile_name) + ".json"
        return os.path.join(self.profiles_dir, filename)
    
    def _create_default_profiles(self):
        """
        Cria perfis padrão para tipos comuns de arquivos
        
        MUDANÇA: Agora verifica se o perfil já existe antes de criar
        Isso mantém compatibilidade com perfis existentes e evita sobrescrever customizações
        """
        
        # Lista de perfis padrão a serem criados
        default_profiles = []
        
        # Perfil para JSON genérico
        json_profile = RegexProfile(
            name="JSON Genérico",
            description="Extrai valores de strings em arquivos JSON",
            capture_patterns=[
                r'"([^"]+)"\s*:\s*"([^"]+)"',  # "key": "value"
                r':\s*"([^"]+)"'  # : "value"
            ],
            exclude_patterns=[
                r'"id"\s*:\s*"[^"]+"',  # Ignora IDs
                r'"key"\s*:\s*"[^"]+"',  # Ignora chaves
                r'"name"\s*:\s*"[a-z_]+"',  # Ignora nomes técnicos
                r'"type"\s*:\s*"[^"]+"'  # Ignora tipos
            ],
            file_type="json"
        )
        default_profiles.append(json_profile)
        
        # Perfil para XML genérico
        xml_profile = RegexProfile(
            name="XML Genérico",
            description="Extrai conteúdo de tags XML",
            capture_patterns=[
                r'>([^<>]+)<',  # >text<
                r'<([a-zA-Z_]+)>([^<>]+)</\1>',  # <tag>text</tag>
            ],
            exclude_patterns=[
                r'<id>.*?</id>',  # Ignora tags ID
                r'<key>.*?</key>',  # Ignora tags key
                r'<!--.*?-->',  # Ignora comentários
            ],
            file_type="xml"
        )
        default_profiles.append(xml_profile)
        
        # Perfil para Bannerlord XML
        bannerlord_profile = RegexProfile(
            name="Bannerlord XML",
            description="Perfil específico para arquivos XML do Mount & Blade II: Bannerlord",
            capture_patterns=[
                r'text="([^"]+)"',  # text="value"
                r'<string[^>]*>([^<]+)</string>',  # <string>value</string>
            ],
            exclude_patterns=[
                r'id="[^"]+"',
                r'key="[^"]+"',
                r'<!--.*?-->',
            ],
            file_type="xml"
        )
        default_profiles.append(bannerlord_profile)
        
        # Perfil para RimWorld XML
        rimworld_profile = RegexProfile(
            name="RimWorld XML",
            description="Perfil específico para arquivos XML do RimWorld",
            capture_patterns=[
                r'<label>([^<]+)</label>',
                r'<description>([^<]+)</description>',
                r'<[a-zA-Z_]+>([^<>]+)</[a-zA-Z_]+>',
            ],
            exclude_patterns=[
                r'<defName>.*?</defName>',
                r'<!--.*?-->',
            ],
            file_type="xml"
        )
        default_profiles.append(rimworld_profile)
        
        # Perfil para CSV genérico
        csv_profile = RegexProfile(
            name="CSV Genérico",
            description="Extrai valores da coluna BRASILIAN em arquivos CSV de jogos (delimitados por ; ou ,)",
            capture_patterns=[
                r'"([^"]+)"',  # Valores entre aspas
                r'([^;,\n\r]+)',  # Valores separados por ponto e vírgula ou vírgula
            ],
            exclude_patterns=[
                r'^[0-9]+$',  # Ignora números puros
                r'^[a-z_0-9/]+$',  # Ignora IDs e caminhos
                r'^\s*$',  # Ignora espaços vazios
            ],
            file_type="csv"
        )
        default_profiles.append(csv_profile)
        
        # MUDANÇA: Salva apenas perfis que ainda não existem
        # Isso preserva customizações do usuário em perfis padrão
        for profile in default_profiles:
            if profile.name not in self.profiles:
                self.save_profile(profile)
    
    def save_profile(self, profile: RegexProfile) -> bool:
        """
        Salva um perfil em arquivo JSON
        
        MUDANÇA: Agora usa slugificação para nomes de arquivo seguros
        O arquivo é salvo como {slug}.json, mas o perfil mantém seu nome original
        
        Args:
            profile: Perfil a ser salvo
            
        Returns:
            True se salvou com sucesso, False em caso de erro
        """
        try:
            # MUDANÇA: Usa função helper para obter caminho com slug
            filepath = self._get_profile_filepath(profile.name)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(profile.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Armazena na memória usando o nome original como chave
            self.profiles[profile.name] = profile
            return True
        except Exception as e:
            print(f"Erro ao salvar perfil: {e}")
            return False
    
    def load_profile(self, filepath: str) -> Optional[RegexProfile]:
        """
        Carrega um perfil de arquivo JSON
        
        MUDANÇA: Agora carrega perfis independente do nome do arquivo
        O nome do perfil é lido do campo 'name' dentro do JSON
        
        Args:
            filepath: Caminho do arquivo JSON
            
        Returns:
            Perfil carregado ou None em caso de erro
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            profile = RegexProfile.from_dict(data)
            # Armazena usando o nome original do perfil como chave
            self.profiles[profile.name] = profile
            return profile
        except Exception as e:
            print(f"Erro ao carregar perfil de {filepath}: {e}")
            return None
    
    def load_all_profiles(self):
        """
        Carrega todos os perfis do diretório
        
        MUDANÇA: Agora carrega TODOS os arquivos .json do diretório na inicialização
        Isso garante que perfis criados pela interface sejam carregados automaticamente
        """
        try:
            if not os.path.exists(self.profiles_dir):
                return
                
            for filename in os.listdir(self.profiles_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.profiles_dir, filename)
                    self.load_profile(filepath)
        except Exception as e:
            print(f"Erro ao carregar perfis do diretório {self.profiles_dir}: {e}")
    
    def get_profile(self, name: str) -> Optional[RegexProfile]:
        """
        Obtém um perfil pelo nome
        
        Args:
            name: Nome do perfil
            
        Returns:
            Perfil ou None
        """
        return self.profiles.get(name)
    
    def get_all_profile_names(self) -> List[str]:
        """Retorna lista com nomes de todos os perfis"""
        return list(self.profiles.keys())
    
    def delete_profile(self, name: str) -> bool:
        """
        Deleta um perfil (remove arquivo e da memória)
        
        MUDANÇA: Agora usa slugificação para encontrar o arquivo correto
        
        Args:
            name: Nome do perfil
            
        Returns:
            True se deletou com sucesso, False em caso de erro
        """
        try:
            # MUDANÇA: Usa função helper para obter caminho com slug
            filepath = self._get_profile_filepath(name)
            
            # Remove arquivo se existir
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Remove da memória
            if name in self.profiles:
                del self.profiles[name]
            
            return True
        except Exception as e:
            print(f"Erro ao deletar perfil {name}: {e}")
            return False
    
    def export_profile(self, name: str, export_path: str) -> bool:
        """
        Exporta um perfil para um arquivo (para compartilhamento)
        
        NOVO: Permite exportar perfis para compartilhar com outros usuários
        
        Args:
            name: Nome do perfil a exportar
            export_path: Caminho onde o perfil será exportado
            
        Returns:
            True se exportou com sucesso, False em caso de erro
        """
        try:
            profile = self.get_profile(name)
            if not profile:
                print(f"Perfil '{name}' não encontrado")
                return False
            
            # Salva uma cópia no caminho especificado
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(profile.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro ao exportar perfil: {e}")
            return False
    
    def import_profile(self, import_path: str) -> Optional[RegexProfile]:
        """
        Importa um perfil de um arquivo externo
        
        NOVO: Permite importar perfis compartilhados por outros usuários
        O perfil importado é automaticamente salvo no diretório de perfis
        
        Args:
            import_path: Caminho do arquivo de perfil a importar
            
        Returns:
            Perfil importado ou None em caso de erro
        """
        try:
            # Carrega o perfil do arquivo externo
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            profile = RegexProfile.from_dict(data)
            
            # Verifica se já existe um perfil com o mesmo nome
            if profile.name in self.profiles:
                # Adiciona sufixo para evitar conflito
                # NOTA: Modifica o nome do perfil para evitar sobrescrever o existente
                # O usuário pode renomear manualmente depois se desejar
                base_name = profile.name
                counter = 1
                while f"{base_name} ({counter})" in self.profiles:
                    counter += 1
                profile.name = f"{base_name} ({counter})"
            
            # Salva o perfil importado
            if self.save_profile(profile):
                return profile
            
            return None
        except Exception as e:
            print(f"Erro ao importar perfil de {import_path}: {e}")
            return None
