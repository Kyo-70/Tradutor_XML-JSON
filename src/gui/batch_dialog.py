"""
Diálogo de Processamento em Lote
Interface para traduzir múltiplos arquivos de uma vez
"""

import os
from typing import List, Dict, Optional

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QProgressBar, QFileDialog,
    QComboBox, QCheckBox, QGroupBox, QMessageBox, QHeaderView,
    QSplitter, QWidget, QTabWidget, QTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from batch_processor import BatchProcessor, BatchFileInfo, BatchResult
from regex_profiles import RegexProfileManager
from database import TranslationMemory
from smart_translator import SmartTranslator


class BatchExtractionThread(QThread):
    """Thread para extração de textos em lote"""
    progress = Signal(int, int, str)
    finished = Signal(bool, str)
    
    def __init__(self, processor: BatchProcessor, profile_name: str):
        super().__init__()
        self.processor = processor
        self.profile_name = profile_name
    
    def run(self):
        try:
            self.processor.set_progress_callback(
                lambda c, t, m: self.progress.emit(c, t, m)
            )
            self.processor.extract_all_texts(self.profile_name)
            self.finished.emit(True, "Extração concluída")
        except Exception as e:
            self.finished.emit(False, str(e))


class BatchSaveThread(QThread):
    """Thread para salvar arquivos em lote"""
    progress = Signal(int, int, str)
    finished = Signal(object)
    
    def __init__(self, processor: BatchProcessor, output_dir: str, create_backup: bool):
        super().__init__()
        self.processor = processor
        self.output_dir = output_dir
        self.create_backup = create_backup
    
    def run(self):
        try:
            self.processor.set_progress_callback(
                lambda c, t, m: self.progress.emit(c, t, m)
            )
            result = self.processor.save_all_files(self.output_dir, self.create_backup)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(None)


class BatchProcessorDialog(QDialog):
    """Diálogo para processamento em lote de múltiplos arquivos"""
    
    def __init__(self, parent, profile_manager: RegexProfileManager,
                 translation_memory: TranslationMemory,
                 smart_translator: SmartTranslator):
        super().__init__(parent)
        self.profile_manager = profile_manager
        self.translation_memory = translation_memory
        self.smart_translator = smart_translator
        self.batch_processor = BatchProcessor(profile_manager)
        
        self.setWindowTitle("Processamento em Lote")
        self.setMinimumSize(900, 600)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        
        # Painel esquerdo - Lista de arquivos
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Grupo de arquivos
        files_group = QGroupBox("Arquivos")
        files_layout = QVBoxLayout(files_group)
        
        # Botões de arquivo
        btn_layout = QHBoxLayout()
        
        self.btn_add_dir = QPushButton("📁 Adicionar Diretório")
        self.btn_add_dir.clicked.connect(self._add_directory)
        btn_layout.addWidget(self.btn_add_dir)
        
        self.btn_add_files = QPushButton("📄 Adicionar Arquivos")
        self.btn_add_files.clicked.connect(self._add_files)
        btn_layout.addWidget(self.btn_add_files)
        
        self.btn_clear = QPushButton("🗑️ Limpar")
        self.btn_clear.clicked.connect(self._clear_files)
        btn_layout.addWidget(self.btn_clear)
        
        files_layout.addLayout(btn_layout)
        
        # Tabela de arquivos
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(["Arquivo", "Tipo", "Tamanho", "Status"])
        self.files_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.files_table.setSelectionBehavior(QTableWidget.SelectRows)
        files_layout.addWidget(self.files_table)
        
        # Checkbox recursivo
        self.chk_recursive = QCheckBox("Incluir subdiretórios")
        self.chk_recursive.setChecked(True)
        files_layout.addWidget(self.chk_recursive)
        
        left_layout.addWidget(files_group)
        
        # Painel direito - Configurações e textos
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Grupo de configurações
        config_group = QGroupBox("Configurações")
        config_layout = QVBoxLayout(config_group)
        
        # Seletor de perfil
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Perfil de Extração:"))
        self.combo_profile = QComboBox()
        self.combo_profile.addItems(self.profile_manager.get_all_profile_names())
        profile_layout.addWidget(self.combo_profile)
        config_layout.addLayout(profile_layout)
        
        # Checkbox de backup
        self.chk_backup = QCheckBox("Criar backup dos arquivos originais")
        self.chk_backup.setChecked(True)
        config_layout.addWidget(self.chk_backup)
        
        right_layout.addWidget(config_group)
        
        # Tabs de textos
        self.tabs = QTabWidget()
        
        # Tab de textos extraídos
        texts_tab = QWidget()
        texts_layout = QVBoxLayout(texts_tab)
        
        self.texts_table = QTableWidget()
        self.texts_table.setColumnCount(3)
        self.texts_table.setHorizontalHeaderLabels(["Arquivo", "Original", "Tradução"])
        self.texts_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.texts_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        texts_layout.addWidget(self.texts_table)
        
        self.tabs.addTab(texts_tab, "Textos Extraídos")
        
        # Tab de estatísticas
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        stats_layout.addWidget(self.stats_text)
        self.tabs.addTab(stats_tab, "Estatísticas")
        
        right_layout.addWidget(self.tabs)
        
        # Adiciona painéis ao splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 600])
        
        layout.addWidget(splitter)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Label de status
        self.status_label = QLabel("Adicione arquivos para começar")
        layout.addWidget(self.status_label)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        self.btn_extract = QPushButton("📥 Extrair Textos")
        self.btn_extract.clicked.connect(self._extract_texts)
        self.btn_extract.setEnabled(False)
        action_layout.addWidget(self.btn_extract)
        
        self.btn_apply_memory = QPushButton("🧠 Aplicar Memória")
        self.btn_apply_memory.clicked.connect(self._apply_memory)
        self.btn_apply_memory.setEnabled(False)
        action_layout.addWidget(self.btn_apply_memory)
        
        self.btn_save = QPushButton("💾 Salvar Todos")
        self.btn_save.clicked.connect(self._save_all)
        self.btn_save.setEnabled(False)
        action_layout.addWidget(self.btn_save)
        
        action_layout.addStretch()
        
        self.btn_close = QPushButton("Fechar")
        self.btn_close.clicked.connect(self.close)
        action_layout.addWidget(self.btn_close)
        
        layout.addLayout(action_layout)
    
    def _add_directory(self):
        """Adiciona um diretório ao lote"""
        directory = QFileDialog.getExistingDirectory(
            self, "Selecionar Diretório"
        )
        
        if directory:
            recursive = self.chk_recursive.isChecked()
            files = self.batch_processor.scan_directory(directory, recursive)
            self._update_files_table()
            self.status_label.setText(f"{len(files)} arquivos encontrados")
            self.btn_extract.setEnabled(len(self.batch_processor.files) > 0)
    
    def _add_files(self):
        """Adiciona arquivos específicos ao lote"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Arquivos",
            "",
            "Arquivos Suportados (*.json *.xml *.csv);;JSON (*.json);;XML (*.xml);;CSV (*.csv)"
        )
        
        if files:
            added = self.batch_processor.add_files(files)
            self._update_files_table()
            self.status_label.setText(f"{len(added)} arquivos adicionados")
            self.btn_extract.setEnabled(len(self.batch_processor.files) > 0)
    
    def _clear_files(self):
        """Limpa a lista de arquivos"""
        self.batch_processor.clear_files()
        self._update_files_table()
        self.texts_table.setRowCount(0)
        self.status_label.setText("Lista de arquivos limpa")
        self.btn_extract.setEnabled(False)
        self.btn_apply_memory.setEnabled(False)
        self.btn_save.setEnabled(False)
    
    def _update_files_table(self):
        """Atualiza a tabela de arquivos"""
        self.files_table.setRowCount(len(self.batch_processor.files))
        
        for i, file_info in enumerate(self.batch_processor.files):
            # Nome do arquivo
            self.files_table.setItem(i, 0, QTableWidgetItem(file_info.filename))
            
            # Tipo
            self.files_table.setItem(i, 1, QTableWidgetItem(file_info.file_type.upper()))
            
            # Tamanho
            size_kb = file_info.size / 1024
            self.files_table.setItem(i, 2, QTableWidgetItem(f"{size_kb:.1f} KB"))
            
            # Status
            status_item = QTableWidgetItem(file_info.status)
            if file_info.status == 'error':
                status_item.setForeground(QColor('#ff6b6b'))
            elif file_info.status == 'completed':
                status_item.setForeground(QColor('#4ecdc4'))
            self.files_table.setItem(i, 3, status_item)
    
    def _extract_texts(self):
        """Extrai textos de todos os arquivos"""
        profile_name = self.combo_profile.currentText()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.btn_extract.setEnabled(False)
        self.status_label.setText("Extraindo textos...")
        
        self.extract_thread = BatchExtractionThread(
            self.batch_processor, profile_name
        )
        self.extract_thread.progress.connect(self._on_extract_progress)
        self.extract_thread.finished.connect(self._on_extract_finished)
        self.extract_thread.start()
    
    def _on_extract_progress(self, current: int, total: int, message: str):
        """Callback de progresso da extração"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(message)
    
    def _on_extract_finished(self, success: bool, message: str):
        """Callback de conclusão da extração"""
        self.progress_bar.setVisible(False)
        self._update_files_table()
        
        if success:
            self._update_texts_table()
            self._update_statistics()
            self.btn_apply_memory.setEnabled(True)
            self.btn_save.setEnabled(True)
            self.status_label.setText(
                f"Extração concluída: {len(self.batch_processor.all_entries)} textos"
            )
        else:
            self.status_label.setText(f"Erro: {message}")
        
        self.btn_extract.setEnabled(True)
    
    def _update_texts_table(self):
        """Atualiza a tabela de textos extraídos"""
        entries = self.batch_processor.all_entries
        self.texts_table.setRowCount(len(entries))
        
        for i, (file_info, entry) in enumerate(entries):
            # Arquivo
            self.texts_table.setItem(i, 0, QTableWidgetItem(file_info.filename))
            
            # Original
            self.texts_table.setItem(i, 1, QTableWidgetItem(entry.original_text))
            
            # Tradução
            trans_item = QTableWidgetItem(entry.translated_text or "")
            if not entry.translated_text:
                trans_item.setForeground(QColor('#888'))
            self.texts_table.setItem(i, 2, trans_item)
    
    def _update_statistics(self):
        """Atualiza as estatísticas"""
        stats = self.batch_processor.get_statistics()
        
        text = f"""
<h3>📊 Estatísticas do Lote</h3>

<table>
<tr><td><b>Total de Arquivos:</b></td><td>{stats['total_files']}</td></tr>
<tr><td><b>Arquivos JSON:</b></td><td>{stats['json_files']}</td></tr>
<tr><td><b>Arquivos XML:</b></td><td>{stats['xml_files']}</td></tr>
<tr><td><b>Tamanho Total:</b></td><td>{stats['total_size'] / 1024:.1f} KB</td></tr>
</table>

<h3>📝 Textos</h3>

<table>
<tr><td><b>Total de Entradas:</b></td><td>{stats['total_entries']}</td></tr>
<tr><td><b>Textos Únicos:</b></td><td>{stats['unique_texts']}</td></tr>
<tr><td><b>Traduzidos:</b></td><td>{stats['translated_entries']}</td></tr>
<tr><td><b>Não Traduzidos:</b></td><td>{stats['untranslated_entries']}</td></tr>
<tr><td><b>Progresso:</b></td><td>{stats['translation_progress']:.1f}%</td></tr>
</table>

<h3>⚠️ Erros</h3>
<p>Arquivos com erro: {stats['files_with_errors']}</p>
        """
        
        self.stats_text.setHtml(text)
    
    def _apply_memory(self):
        """Aplica traduções da memória"""
        if not self.smart_translator:
            QMessageBox.warning(self, "Aviso", "Memória de tradução não disponível")
            return
        
        self.status_label.setText("Aplicando memória de tradução...")
        
        # Aplica traduções
        translations = {}
        for _, entry in self.batch_processor.all_entries:
            if not entry.translated_text:
                translation = self.smart_translator.translate(entry.original_text)
                if translation:
                    translations[entry.original_text] = translation
        
        count = self.batch_processor.apply_translations(translations)
        
        self._update_texts_table()
        self._update_statistics()
        self.status_label.setText(f"{count} traduções aplicadas da memória")
    
    def _save_all(self):
        """Salva todos os arquivos"""
        # Pergunta se quer salvar em diretório diferente
        reply = QMessageBox.question(
            self,
            "Salvar Arquivos",
            "Deseja salvar em um diretório diferente?\n\n"
            "Sim = Escolher diretório de saída\n"
            "Não = Sobrescrever arquivos originais (com backup)",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return
        
        output_dir = None
        if reply == QMessageBox.Yes:
            output_dir = QFileDialog.getExistingDirectory(
                self, "Selecionar Diretório de Saída"
            )
            if not output_dir:
                return
        
        create_backup = self.chk_backup.isChecked()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.btn_save.setEnabled(False)
        self.status_label.setText("Salvando arquivos...")
        
        self.save_thread = BatchSaveThread(
            self.batch_processor, output_dir, create_backup
        )
        self.save_thread.progress.connect(self._on_save_progress)
        self.save_thread.finished.connect(self._on_save_finished)
        self.save_thread.start()
    
    def _on_save_progress(self, current: int, total: int, message: str):
        """Callback de progresso do salvamento"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(message)
    
    def _on_save_finished(self, result: Optional[BatchResult]):
        """Callback de conclusão do salvamento"""
        self.progress_bar.setVisible(False)
        self._update_files_table()
        self.btn_save.setEnabled(True)
        
        if result:
            QMessageBox.information(
                self,
                "Salvamento Concluído",
                f"Arquivos processados: {result.processed_files}\n"
                f"Arquivos com erro: {result.failed_files}\n"
                f"Traduções aplicadas: {result.translated_entries}"
            )
            self.status_label.setText(
                f"Salvamento concluído: {result.processed_files} arquivos"
            )
        else:
            QMessageBox.critical(self, "Erro", "Falha ao salvar arquivos")
            self.status_label.setText("Erro ao salvar arquivos")
