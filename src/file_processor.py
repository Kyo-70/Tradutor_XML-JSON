"""
Módulo de Processamento de Arquivos
Responsável por extrair, processar e reinserir traduções em arquivos JSON/XML/CSV

Melhorias implementadas:
- Detecção automática de encoding
- Suporte a múltiplos encodings (UTF-8, Latin-1, etc.)
- Suporte a arquivos CSV com extração inteligente
- Melhor tratamento de erros
"""

import re
import json
import csv
import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import shutil
import os
from datetime import datetime
from pathlib import Path
from io import StringIO


def detect_encoding(filepath: str) -> str:
    """
    Detecta o encoding de um arquivo automaticamente.

    Tenta usar chardet se disponível, caso contrário usa heurística simples.

    Args:
        filepath: Caminho do arquivo

    Returns:
        Nome do encoding detectado (ex: 'utf-8', 'latin-1')
    """
    try:
        # Tenta usar chardet para detecção precisa
        import chardet

        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result.get('encoding', 'utf-8')
            confidence = result.get('confidence', 0)

            # Se confiança for baixa, usa fallback
            if confidence < 0.7:
                encoding = _detect_encoding_fallback(raw_data)

            return encoding or 'utf-8'

    except ImportError:
        # chardet não disponível, usa fallback
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            return _detect_encoding_fallback(raw_data)

    except Exception:
        return 'utf-8'


def _detect_encoding_fallback(raw_data: bytes) -> str:
    """
    Detecção de encoding por heurística quando chardet não está disponível.

    Args:
        raw_data: Bytes do arquivo

    Returns:
        Encoding detectado
    """
    # Tenta UTF-8 primeiro (mais comum)
    try:
        raw_data.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        pass

    # Verifica BOM (Byte Order Mark)
    if raw_data.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-sig'
    if raw_data.startswith(b'\xff\xfe'):
        return 'utf-16-le'
    if raw_data.startswith(b'\xfe\xff'):
        return 'utf-16-be'

    # Tenta outros encodings comuns
    encodings_to_try = ['latin-1', 'cp1252', 'iso-8859-1', 'cp1250', 'shift_jis', 'gb2312']

    for encoding in encodings_to_try:
        try:
            raw_data.decode(encoding)
            return encoding
        except (UnicodeDecodeError, LookupError):
            continue

    # Fallback final
    return 'utf-8'


@dataclass
class TranslationEntry:
    """Representa uma entrada de tradução"""
    index: int
    original_text: str
    translated_text: str = ""
    position: int = 0  # Posição no arquivo original
    context: str = ""  # Contexto (linha completa)
    csv_info: dict = None  # Informações específicas para CSV (coluna, delimitador, etc.)


class FileProcessor:
    """
    Processa arquivos JSON, XML e CSV para extração e inserção de traduções.

    Suporta detecção automática de encoding para arquivos de jogos
    que podem usar diferentes codificações.
    """

    # Encodings comuns em jogos
    COMMON_GAME_ENCODINGS = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'shift_jis']

    def __init__(self, regex_profile=None):
        """
        Inicializa o processador

        Args:
            regex_profile: Perfil de regex a ser usado
        """
        self.regex_profile = regex_profile
        self.original_content: str = ""
        self.entries: List[TranslationEntry] = []
        self.file_type: str = ""
        self.detected_encoding: str = "utf-8"
        self.filepath: Optional[str] = None

    def load_file(self, filepath: str, encoding: str = None) -> bool:
        """
        Carrega um arquivo para processamento com detecção automática de encoding.

        Args:
            filepath: Caminho do arquivo
            encoding: Encoding específico (None = detectar automaticamente)

        Returns:
            True se carregou com sucesso
        """
        try:
            self.filepath = filepath

            # Detecta encoding se não especificado
            if encoding is None:
                self.detected_encoding = detect_encoding(filepath)
            else:
                self.detected_encoding = encoding

            # Tenta carregar com o encoding detectado
            try:
                with open(filepath, 'r', encoding=self.detected_encoding) as f:
                    self.original_content = f.read()
            except UnicodeDecodeError:
                # Fallback para outros encodings
                for fallback_encoding in self.COMMON_GAME_ENCODINGS:
                    if fallback_encoding == self.detected_encoding:
                        continue
                    try:
                        with open(filepath, 'r', encoding=fallback_encoding) as f:
                            self.original_content = f.read()
                        self.detected_encoding = fallback_encoding
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    # Último recurso: lê com errors='replace'
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        self.original_content = f.read()
                    self.detected_encoding = 'utf-8'

            # Detecta tipo de arquivo
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.json':
                self.file_type = 'json'
            elif ext == '.xml':
                self.file_type = 'xml'
            elif ext == '.csv':
                self.file_type = 'csv'
            else:
                return False

            return True

        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return False

    def get_detected_encoding(self) -> str:
        """Retorna o encoding detectado do arquivo"""
        return self.detected_encoding

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
            elif self.file_type == 'csv':
                self._extract_csv_default()
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

    def _extract_csv_default(self):
        """
        Extração padrão para arquivos CSV de localização de jogos.
        
        Comportamento:
        1. Detecta automaticamente o delimitador (; ou ,)
        2. Localiza a posição da coluna BRASILIAN no cabeçalho
        3. Extrai textos da coluna ENGLISH (para traduzir)
        4. Armazena informações para inserir traduções na coluna BRASILIAN
        """
        try:
            # Detecta o delimitador analisando a primeira linha
            first_line = self.original_content.split('\n')[0]
            delimiter = ';' if ';' in first_line else ','
            
            # Cria um leitor CSV
            csv_file = StringIO(self.original_content)
            reader = csv.reader(csv_file, delimiter=delimiter)
            
            # Lê o cabeçalho
            try:
                header = next(reader)
            except StopIteration:
                print("Arquivo CSV vazio")
                return
            
            # Procura a coluna ENGLISH (fonte) e BRASILIAN (destino)
            english_column = None
            brasilian_column = None
            
            # Variações possíveis dos nomes das colunas
            english_variants = ['ENGLISH', 'EN', 'INGLÊS', 'INGLES']
            brasilian_variants = ['BRASILIAN', 'BRAZILIAN', 'PORTUGUESE', 'PT-BR', 'PTBR', 'PT_BR', 'PORTUGUES', 'PORTUGUÊS']
            
            for col_index, col_name in enumerate(header):
                col_upper = col_name.strip().upper()
                
                # Procura coluna ENGLISH
                if col_upper in english_variants:
                    english_column = col_index
                    print(f"✓ Coluna ENGLISH encontrada na posição {col_index}")
                
                # Procura coluna BRASILIAN
                if col_upper in brasilian_variants:
                    brasilian_column = col_index
                    print(f"✓ Coluna BRASILIAN encontrada na posição {col_index}")
            
            # Valida se encontrou as colunas necessárias
            if english_column is None:
                print("⚠️  Coluna ENGLISH não encontrada. Usando primeira coluna de texto.")
                # Fallback: usa a segunda coluna (primeira geralmente é ID)
                english_column = 1 if len(header) > 1 else 0
            
            if brasilian_column is None:
                print("⚠️  Coluna BRASILIAN não encontrada. Não será possível inserir traduções.")
                return
            
            # Processa cada linha do CSV
            lines = self.original_content.split('\n')
            
            # row_index começa em 1 porque o cabeçalho é a linha 0
            # Mas no array lines, o cabeçalho é lines[0], então a primeira linha de dados é lines[1]
            for row_index, row in enumerate(reader, start=1):
                # Verifica se a linha tem as colunas necessárias
                if english_column >= len(row):
                    continue
                
                # Obtém o texto em inglês (fonte para tradução)
                english_text = row[english_column].strip() if english_column < len(row) else ""
                
                # Ignora células vazias
                if not english_text or len(english_text) < 2:
                    continue
                
                # Ignora números puros
                if english_text.replace('.', '').replace(',', '').replace('-', '').isdigit():
                    continue
                
                # Ignora valores que parecem IDs ou códigos (contém / ou _)
                if '/' in english_text or '_' in english_text:
                    # Mas permite se tiver espaços (ex: "Template 1" é OK)
                    if ' ' not in english_text:
                        continue
                
                # Obtém a chave (primeira coluna) para contexto
                key = row[0] if len(row) > 0 else "?"
                
                # Obtém o valor atual da coluna BRASILIAN (pode estar vazio)
                current_brasilian = row[brasilian_column].strip() if brasilian_column < len(row) else ""
                
                # Cria contexto rico com informações da linha
                context_parts = [
                    f"Chave: {key}",
                    f"English: {english_text}",
                ]
                
                if current_brasilian:
                    context_parts.append(f"Brasilian atual: {current_brasilian}")
                else:
                    context_parts.append(f"Brasilian: (vazio)")
                
                context_parts.append(f"Posição BRASILIAN: coluna {brasilian_column}")
                context = " | ".join(context_parts)
                
                # Encontra a linha completa no conteúdo original
                line_number = row_index  # +1 para o cabeçalho
                original_line = lines[line_number] if line_number < len(lines) else ""
                
                # Calcula a posição onde a tradução deve ser inserida
                # Precisamos encontrar a posição da célula BRASILIAN na linha original
                position_info = {
                    'line_number': line_number,
                    'brasilian_column': brasilian_column,
                    'delimiter': delimiter,
                    'original_line': original_line,
                    'key': key
                }
                
                entry = TranslationEntry(
                    index=len(self.entries),
                    original_text=english_text,  # Mostra o texto em inglês
                    position=line_number,  # Armazena o número da linha
                    context=context,
                    csv_info=position_info
                )
                
                self.entries.append(entry)
        
        except Exception as e:
            print(f"Erro ao extrair textos do CSV: {e}")
            import traceback
            traceback.print_exc()

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
        Aplica traduções ao conteúdo original.
        Para arquivos CSV de localização, insere traduções na coluna BRASILIAN.
        
        Args:
            translations: Dicionário {texto_original_em_ingles: texto_traduzido_em_portugues}
        
        Returns:
            Conteúdo traduzido
        """
        # Para arquivos CSV, usa lógica especial
        if self.file_type == 'csv' and self.entries and hasattr(self.entries[0], 'csv_info') and self.entries[0].csv_info is not None:
            return self._apply_translations_csv(translations)
        
        # Para outros tipos, usa lógica padrão
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
    
    def _apply_translations_csv(self, translations: Dict[str, str]) -> str:
        """
        Aplica traduções especificamente para arquivos CSV de localização.
        Insere traduções na coluna BRASILIAN mantendo a estrutura intacta.
        
        Args:
            translations: Dicionário {texto_em_ingles: texto_traduzido}
        
        Returns:
            Conteúdo CSV com traduções aplicadas
        """
        try:
            lines = self.original_content.split('\n')
            
            # Processa cada entrada que tem tradução
            for entry in self.entries:
                if entry.original_text not in translations:
                    continue
                
                if not hasattr(entry, 'csv_info') or entry.csv_info is None:
                    continue
                
                csv_info = entry.csv_info
                line_number = csv_info['line_number']
                brasilian_column = csv_info['brasilian_column']
                delimiter = csv_info['delimiter']
                
                # Verifica se a linha existe
                if line_number >= len(lines):
                    continue
                
                original_line = lines[line_number]
                translated_text = translations[entry.original_text]
                
                # Divide a linha em células
                cells = original_line.split(delimiter)
                
                # Verifica se a coluna BRASILIAN existe
                if brasilian_column >= len(cells):
                    # Se não existe, adiciona células vazias até chegar lá
                    while len(cells) <= brasilian_column:
                        cells.append('')
                
                # Insere a tradução na coluna BRASILIAN
                cells[brasilian_column] = translated_text
                
                # Reconstrói a linha
                new_line = delimiter.join(cells)
                lines[line_number] = new_line
            
            # Reconstrói o conteúdo completo
            return '\n'.join(lines)
        
        except Exception as e:
            print(f"Erro ao aplicar traduções no CSV: {e}")
            import traceback
            traceback.print_exc()
            return self.original_content

    def save_file(self, filepath: str, content: str, create_backup: bool = True,
                  encoding: str = None) -> bool:
        """
        Salva o arquivo traduzido preservando o encoding original.

        Args:
            filepath: Caminho do arquivo
            content: Conteúdo a ser salvo
            create_backup: Se deve criar backup do original
            encoding: Encoding para salvar (None = usa o detectado)

        Returns:
            True se salvou com sucesso
        """
        try:
            # Usa encoding original se não especificado
            save_encoding = encoding or self.detected_encoding

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

                # Salva o backup com encoding original
                with open(backup_path, 'w', encoding=save_encoding) as f:
                    f.write(self.original_content)

            # Salva arquivo traduzido com encoding original
            with open(filepath, 'w', encoding=save_encoding) as f:
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
            'progress': (translated / total * 100) if total > 0 else 0,
            'encoding': self.detected_encoding,
            'file_type': self.file_type
        }
