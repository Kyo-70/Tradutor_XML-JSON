"""
Módulo de Processamento em Lote
Permite traduzir múltiplos arquivos de um diretório de uma vez
"""

import os
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from file_processor import FileProcessor, TranslationEntry
from regex_profiles import RegexProfileManager, RegexProfile


@dataclass
class BatchFileInfo:
    """Informações sobre um arquivo no lote"""
    filepath: str
    filename: str
    file_type: str  # 'json' ou 'xml'
    size: int
    entries_count: int = 0
    translated_count: int = 0
    status: str = 'pending'  # pending, processing, completed, error
    error_message: str = ''
    entries: List[TranslationEntry] = field(default_factory=list)


@dataclass
class BatchResult:
    """Resultado do processamento em lote"""
    total_files: int
    processed_files: int
    failed_files: int
    total_entries: int
    translated_entries: int
    skipped_entries: int
    start_time: datetime
    end_time: Optional[datetime] = None
    files: List[BatchFileInfo] = field(default_factory=list)


class BatchProcessor:
    """
    Processador de tradução em lote para múltiplos arquivos.
    
    Permite carregar um diretório inteiro e traduzir todos os arquivos
    XML e JSON de uma vez, consolidando os textos em uma única interface.
    """
    
    SUPPORTED_EXTENSIONS = ['.json', '.xml']
    
    def __init__(self, profile_manager: RegexProfileManager = None):
        """
        Inicializa o processador em lote.
        
        Args:
            profile_manager: Gerenciador de perfis regex
        """
        self.profile_manager = profile_manager or RegexProfileManager()
        self.files: List[BatchFileInfo] = []
        self.all_entries: List[Tuple[BatchFileInfo, TranslationEntry]] = []
        self._progress_callback: Optional[Callable[[int, int, str], None]] = None
    
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Define callback para progresso.
        
        Args:
            callback: Função (current, total, message) chamada durante processamento
        """
        self._progress_callback = callback
    
    def _report_progress(self, current: int, total: int, message: str):
        """Reporta progresso se callback estiver definido"""
        if self._progress_callback:
            self._progress_callback(current, total, message)
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[BatchFileInfo]:
        """
        Escaneia um diretório em busca de arquivos suportados.
        
        Args:
            directory: Caminho do diretório
            recursive: Se True, busca em subdiretórios
            
        Returns:
            Lista de informações dos arquivos encontrados
        """
        self.files = []
        
        if not os.path.isdir(directory):
            return self.files
        
        # Coleta arquivos
        if recursive:
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    self._add_file_if_supported(filepath)
        else:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    self._add_file_if_supported(filepath)
        
        return self.files
    
    def _add_file_if_supported(self, filepath: str):
        """Adiciona arquivo à lista se for suportado"""
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext in self.SUPPORTED_EXTENSIONS:
            try:
                size = os.path.getsize(filepath)
                file_info = BatchFileInfo(
                    filepath=filepath,
                    filename=os.path.basename(filepath),
                    file_type=ext[1:],  # Remove o ponto
                    size=size
                )
                self.files.append(file_info)
            except OSError:
                pass
    
    def add_files(self, filepaths: List[str]) -> List[BatchFileInfo]:
        """
        Adiciona arquivos específicos ao lote.
        
        Args:
            filepaths: Lista de caminhos de arquivos
            
        Returns:
            Lista de arquivos adicionados
        """
        added = []
        
        for filepath in filepaths:
            if os.path.isfile(filepath):
                ext = os.path.splitext(filepath)[1].lower()
                
                if ext in self.SUPPORTED_EXTENSIONS:
                    # Verifica se já não está na lista
                    if not any(f.filepath == filepath for f in self.files):
                        try:
                            size = os.path.getsize(filepath)
                            file_info = BatchFileInfo(
                                filepath=filepath,
                                filename=os.path.basename(filepath),
                                file_type=ext[1:],
                                size=size
                            )
                            self.files.append(file_info)
                            added.append(file_info)
                        except OSError:
                            pass
        
        return added
    
    def remove_file(self, filepath: str) -> bool:
        """
        Remove um arquivo do lote.
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            True se removeu
        """
        for i, file_info in enumerate(self.files):
            if file_info.filepath == filepath:
                self.files.pop(i)
                return True
        return False
    
    def clear_files(self):
        """Limpa a lista de arquivos"""
        self.files = []
        self.all_entries = []
    
    def extract_all_texts(self, profile_name: str = None) -> List[Tuple[BatchFileInfo, TranslationEntry]]:
        """
        Extrai textos de todos os arquivos do lote.
        
        Args:
            profile_name: Nome do perfil regex a usar (None = auto-detectar)
            
        Returns:
            Lista de tuplas (arquivo, entrada) com todos os textos
        """
        self.all_entries = []
        total = len(self.files)
        
        for i, file_info in enumerate(self.files):
            self._report_progress(i + 1, total, f"Extraindo: {file_info.filename}")
            
            try:
                # Determina perfil
                if profile_name:
                    profile = self.profile_manager.get_profile(profile_name)
                else:
                    # Auto-detecta baseado no tipo de arquivo
                    profile = self._auto_detect_profile(file_info)
                
                # Cria processador
                processor = FileProcessor(profile)
                
                # Carrega arquivo
                if not processor.load_file(file_info.filepath):
                    file_info.status = 'error'
                    file_info.error_message = 'Falha ao carregar arquivo'
                    continue
                
                # Extrai textos
                entries = processor.extract_texts()
                file_info.entries = entries
                file_info.entries_count = len(entries)
                file_info.status = 'extracted'
                
                # Adiciona à lista consolidada
                for entry in entries:
                    self.all_entries.append((file_info, entry))
                
            except Exception as e:
                file_info.status = 'error'
                file_info.error_message = str(e)
        
        return self.all_entries
    
    def _auto_detect_profile(self, file_info: BatchFileInfo) -> Optional[RegexProfile]:
        """Auto-detecta o perfil baseado no tipo de arquivo"""
        profiles = self.profile_manager.get_all_profile_names()
        
        # Tenta encontrar perfil genérico para o tipo
        generic_name = f"{file_info.file_type.upper()} Genérico"
        if generic_name in profiles:
            return self.profile_manager.get_profile(generic_name)
        
        # Fallback para qualquer perfil do tipo
        for name in profiles:
            profile = self.profile_manager.get_profile(name)
            if profile and profile.file_type == file_info.file_type:
                return profile
        
        return None
    
    def apply_translations(self, translations: Dict[str, str]) -> int:
        """
        Aplica traduções aos textos extraídos.
        
        Args:
            translations: Dicionário {texto_original: tradução}
            
        Returns:
            Número de traduções aplicadas
        """
        count = 0
        
        for file_info, entry in self.all_entries:
            if entry.original_text in translations:
                entry.translated_text = translations[entry.original_text]
                count += 1
        
        # Atualiza contadores dos arquivos
        for file_info in self.files:
            file_info.translated_count = sum(
                1 for e in file_info.entries if e.translated_text
            )
        
        return count
    
    def save_all_files(self, output_dir: str = None, 
                       create_backup: bool = True) -> BatchResult:
        """
        Salva todos os arquivos com as traduções aplicadas.
        
        Args:
            output_dir: Diretório de saída (None = sobrescreve originais)
            create_backup: Se True, cria backup dos originais
            
        Returns:
            Resultado do processamento
        """
        result = BatchResult(
            total_files=len(self.files),
            processed_files=0,
            failed_files=0,
            total_entries=len(self.all_entries),
            translated_entries=sum(
                1 for _, e in self.all_entries if e.translated_text
            ),
            skipped_entries=sum(
                1 for _, e in self.all_entries if not e.translated_text
            ),
            start_time=datetime.now(),
            files=self.files.copy()
        )
        
        total = len(self.files)
        
        for i, file_info in enumerate(self.files):
            self._report_progress(i + 1, total, f"Salvando: {file_info.filename}")
            
            try:
                # Pula arquivos com erro
                if file_info.status == 'error':
                    result.failed_files += 1
                    continue
                
                # Determina caminho de saída
                if output_dir:
                    # Mantém estrutura de diretórios relativa
                    rel_path = os.path.relpath(file_info.filepath, 
                                               os.path.dirname(file_info.filepath))
                    output_path = os.path.join(output_dir, rel_path)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                else:
                    output_path = file_info.filepath
                
                # Cria dicionário de traduções para este arquivo
                translations = {
                    entry.original_text: entry.translated_text
                    for entry in file_info.entries
                    if entry.translated_text
                }
                
                # Carrega e salva arquivo
                profile = self._auto_detect_profile(file_info)
                processor = FileProcessor(profile)
                
                if processor.load_file(file_info.filepath):
                    content = processor.apply_translations(translations)
                    
                    if processor.save_file(output_path, content, create_backup):
                        file_info.status = 'completed'
                        result.processed_files += 1
                    else:
                        file_info.status = 'error'
                        file_info.error_message = 'Falha ao salvar'
                        result.failed_files += 1
                else:
                    file_info.status = 'error'
                    file_info.error_message = 'Falha ao carregar'
                    result.failed_files += 1
                    
            except Exception as e:
                file_info.status = 'error'
                file_info.error_message = str(e)
                result.failed_files += 1
        
        result.end_time = datetime.now()
        return result
    
    def get_unique_texts(self) -> List[str]:
        """
        Retorna lista de textos únicos de todos os arquivos.
        
        Returns:
            Lista de textos originais únicos
        """
        seen = set()
        unique = []
        
        for _, entry in self.all_entries:
            if entry.original_text not in seen:
                seen.add(entry.original_text)
                unique.append(entry.original_text)
        
        return unique
    
    def get_untranslated_texts(self) -> List[str]:
        """
        Retorna lista de textos ainda não traduzidos.
        
        Returns:
            Lista de textos sem tradução
        """
        seen = set()
        untranslated = []
        
        for _, entry in self.all_entries:
            if not entry.translated_text and entry.original_text not in seen:
                seen.add(entry.original_text)
                untranslated.append(entry.original_text)
        
        return untranslated
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas do lote atual.
        
        Returns:
            Dicionário com estatísticas
        """
        total_entries = len(self.all_entries)
        translated = sum(1 for _, e in self.all_entries if e.translated_text)
        unique_texts = len(set(e.original_text for _, e in self.all_entries))
        
        return {
            'total_files': len(self.files),
            'json_files': sum(1 for f in self.files if f.file_type == 'json'),
            'xml_files': sum(1 for f in self.files if f.file_type == 'xml'),
            'total_size': sum(f.size for f in self.files),
            'total_entries': total_entries,
            'translated_entries': translated,
            'untranslated_entries': total_entries - translated,
            'unique_texts': unique_texts,
            'translation_progress': (translated / total_entries * 100) if total_entries > 0 else 0,
            'files_with_errors': sum(1 for f in self.files if f.status == 'error'),
        }
