"""
Módulo de Processamento de Arquivos
Responsável por extrair, processar e reinserir traduções em arquivos JSON/XML
"""

import re
import json
import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import shutil
import os
from datetime import datetime
from pathlib import Path

@dataclass
class TranslationEntry:
    """Representa uma entrada de tradução"""
    index: int
    original_text: str
    translated_text: str = ""
    position: int = 0  # Posição no arquivo original
    context: str = ""  # Contexto (linha completa)
    
class FileProcessor:
    """Processa arquivos JSON e XML para extração e inserção de traduções"""
    
    def __init__(self, regex_profile=None):
        """
        Inicializa o processador
        
        Args:
            regex_profile: Perfil de regex a ser usado
        """
        self.regex_profile = regex_profile
        self.original_content = ""
        self.entries: List[TranslationEntry] = []
        self.file_type = ""
    
    def load_file(self, filepath: str) -> bool:
        """
        Carrega um arquivo para processamento
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            True se carregou com sucesso
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.original_content = f.read()
            
            # Detecta tipo de arquivo
            if filepath.endswith('.json'):
                self.file_type = 'json'
            elif filepath.endswith('.xml'):
                self.file_type = 'xml'
            else:
                return False
            
            return True
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return False
    
    def extract_texts(self) -> List[TranslationEntry]:
        """
        Extrai textos traduzíveis do arquivo
        
        Returns:
            Lista de entradas de tradução
        """
        self.entries = []
        
        if not self.regex_profile:
            # Usa extração padrão se não houver perfil
            if self.file_type == 'json':
                self._extract_json_default()
            elif self.file_type == 'xml':
                self._extract_xml_default()
        else:
            # Usa perfil de regex personalizado
            self._extract_with_profile()
        
        return self.entries
    
    def _extract_json_default(self):
        """Extração padrão para JSON"""
        # Padrão: captura valores de strings
        pattern = r'"([^"]+)"\s*:\s*"([^"]+)"'
        
        for match in re.finditer(pattern, self.original_content):
            key = match.group(1)
            value = match.group(2)
            
            # Ignora chaves técnicas comuns
            if key.lower() in ['id', 'key', 'type', 'name'] and len(value) < 50:
                continue
            
            # Ignora valores que parecem IDs ou códigos
            if re.match(r'^[a-z_0-9]+$', value):
                continue
            
            entry = TranslationEntry(
                index=len(self.entries),
                original_text=value,
                position=match.start(2),
                context=match.group(0)
            )
            self.entries.append(entry)
    
    def _extract_xml_default(self):
        """Extração padrão para XML"""
        # Padrão: captura conteúdo entre tags
        pattern = r'>([^<>]+)<'
        
        for match in re.finditer(pattern, self.original_content):
            text = match.group(1).strip()
            
            # Ignora textos vazios ou muito curtos
            if len(text) < 2:
                continue
            
            # Ignora números puros
            if text.isdigit():
                continue
            
            # Ignora valores que parecem IDs
            if re.match(r'^[a-z_0-9]+$', text):
                continue
            
            entry = TranslationEntry(
                index=len(self.entries),
                original_text=text,
                position=match.start(1),
                context=match.group(0)
            )
            self.entries.append(entry)
    
    def _extract_with_profile(self):
        """Extração usando perfil de regex personalizado"""
        # Primeiro, aplica padrões de exclusão
        excluded_positions = set()
        
        for exclude_pattern in self.regex_profile.exclude_patterns:
            try:
                for match in re.finditer(exclude_pattern, self.original_content):
                    excluded_positions.add((match.start(), match.end()))
            except re.error as e:
                print(f"Erro no padrão de exclusão '{exclude_pattern}': {e}")
        
        # Depois, aplica padrões de captura
        for capture_pattern in self.regex_profile.capture_patterns:
            try:
                for match in re.finditer(capture_pattern, self.original_content):
                    # Pega o último grupo capturado (geralmente o texto)
                    groups = match.groups()
                    if not groups:
                        continue
                    
                    text = groups[-1].strip()
                    
                    # Ignora textos vazios
                    if not text or len(text) < 2:
                        continue
                    
                    # Verifica se está em região excluída
                    position = match.start()
                    is_excluded = any(start <= position <= end 
                                    for start, end in excluded_positions)
                    
                    if is_excluded:
                        continue
                    
                    entry = TranslationEntry(
                        index=len(self.entries),
                        original_text=text,
                        position=position,
                        context=match.group(0)
                    )
                    self.entries.append(entry)
                    
            except re.error as e:
                print(f"Erro no padrão de captura '{capture_pattern}': {e}")
        
        # Remove duplicatas mantendo a primeira ocorrência
        seen = set()
        unique_entries = []
        for entry in self.entries:
            if entry.original_text not in seen:
                seen.add(entry.original_text)
                entry.index = len(unique_entries)
                unique_entries.append(entry)
        
        self.entries = unique_entries
    
    def apply_translations(self, translations: Dict[str, str]) -> str:
        """
        Aplica traduções ao conteúdo original
        
        Args:
            translations: Dicionário {texto_original: texto_traduzido}
            
        Returns:
            Conteúdo traduzido
        """
        result = self.original_content
        
        # Ordena entradas por posição (de trás para frente para não afetar posições)
        sorted_entries = sorted(self.entries, key=lambda e: e.position, reverse=True)
        
        for entry in sorted_entries:
            if entry.original_text in translations:
                translated = translations[entry.original_text]
                
                # Substitui apenas na posição exata
                before = result[:entry.position]
                after = result[entry.position + len(entry.original_text):]
                result = before + translated + after
        
        return result
    
    def save_file(self, filepath: str, content: str, create_backup: bool = True) -> bool:
        """
        Salva o arquivo traduzido
        
        Args:
            filepath: Caminho do arquivo
            content: Conteúdo a ser salvo
            create_backup: Se deve criar backup do original
            
        Returns:
            True se salvou com sucesso
        """
        try:
            # Cria backup se solicitado
            if create_backup and self.original_content:
                # Cria pasta de backups no mesmo diretório do arquivo
                file_dir = os.path.dirname(os.path.abspath(filepath))
                backup_dir = os.path.join(file_dir, "backups")
                
                # Cria o diretório se não existir
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                
                # Cria o nome do backup com timestamp
                filename = os.path.basename(filepath)
                backup_filename = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = os.path.join(backup_dir, backup_filename)
                
                # Salva o backup
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(self.original_content)
            
            # Salva arquivo traduzido
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            return False
    
    def get_statistics(self) -> dict:
        """
        Retorna estatísticas do processamento
        
        Returns:
            Dicionário com estatísticas
        """
        total = len(self.entries)
        translated = sum(1 for e in self.entries if e.translated_text)
        
        return {
            'total_entries': total,
            'translated': translated,
            'pending': total - translated,
            'progress': (translated / total * 100) if total > 0 else 0
        }
