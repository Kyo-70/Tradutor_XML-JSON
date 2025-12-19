"""
Janela Principal da Interface Gráfica
Interface moderna e escura para tradução de jogos com segurança e otimização
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path para funcionar com PyInstaller
if getattr(sys, 'frozen', False):
    # Executando como executável
    BASE_DIR = os.path.dirname(sys.executable)
    INTERNAL_DIR = os.path.join(BASE_DIR, '_internal')
    if os.path.exists(INTERNAL_DIR):
        sys.path.insert(0, INTERNAL_DIR)
    sys.path.insert(0, BASE_DIR)
else:
    # Executando como script
    sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QTableWidget, QTableWidgetItem, QLabel,
                              QFileDialog, QComboBox, QProgressBar, QMessageBox,
                              QHeaderView, QLineEdit, QDialog, QTextEdit, QGroupBox,
                              QTabWidget, QSpinBox, QCheckBox, QSplitter, QFrame,
                              QStatusBar, QToolBar, QMenu, QMenuBar, QApplication)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QSettings
from PySide6.QtGui import QPalette, QColor, QFont, QAction, QIcon, QKeySequence, QShortcut

# Imports com tratamento de erro para funcionar tanto como script quanto executável
try:
    from database import TranslationMemory, create_new_database
    from regex_profiles import RegexProfileManager
    from file_processor import FileProcessor, TranslationEntry
    from smart_translator import SmartTranslator
    from translation_api import TranslationAPIManager
    from logger import app_logger
    from security import (SecurityValidator, ResourceMonitor, ChunkProcessor,
                         AutoSaveManager, LIMITS, is_safe_to_proceed, 
                         safe_operation, memory_safe)
except ImportError:
    # Tenta import relativo
    from src.database import TranslationMemory, create_new_database
    from src.regex_profiles import RegexProfileManager
    from src.file_processor import FileProcessor, TranslationEntry
    from src.smart_translator import SmartTranslator
    from src.translation_api import TranslationAPIManager
    from src.logger import app_logger
    from src.security import (SecurityValidator, ResourceMonitor, ChunkProcessor,
                             AutoSaveManager, LIMITS, is_safe_to_proceed, 
                             safe_operation, memory_safe)

# Import do editor de regex
try:
    from gui.regex_editor import RegexProfileManagerDialog, ImportTranslationDialog
except ImportError:
    try:
        from regex_editor import RegexProfileManagerDialog, ImportTranslationDialog
    except ImportError:
        from src.gui.regex_editor import RegexProfileManagerDialog, ImportTranslationDialog

# ============================================================================
# UI CONSTANTS
# ============================================================================

# Geometria padrão da janela
DEFAULT_WINDOW_X = 100
DEFAULT_WINDOW_Y = 100
DEFAULT_WINDOW_WIDTH = 1300
DEFAULT_WINDOW_HEIGHT = 800

# Settings para persistência
# Constantes usadas pelo QSettings para identificação da aplicação no sistema de armazenamento persistente
# No Windows: armazenado no registro ou em arquivos .ini em AppData
# No Linux/Mac: armazenado em arquivos de configuração específicos do sistema
SETTINGS_ORG_NAME = "ManusAI"  # Nome da organização/desenvolvedor
SETTINGS_APP_NAME = "GameTranslator"  # Nome da aplicação

# Cores para linhas da tabela (tema escuro)
class TableColors:
    """Cores usadas nas tabelas para manter consistência visual"""
    BASE_ROW = QColor(40, 40, 40)           # Cor de fundo para linhas pares
    ALTERNATE_ROW = QColor(50, 50, 50)      # Cor de fundo para linhas ímpares
    TRANSLATED_ROW = QColor(40, 60, 40)     # Cor de fundo para linhas traduzidas

# ============================================================================
# WORKER THREADS
# ============================================================================

class TranslationWorker(QThread):
    """Thread para processamento de tradução em background"""
    
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, texts, api_manager, smart_translator):
        super().__init__()
        self.texts = texts
        self.api_manager = api_manager
        self.smart_translator = smart_translator
        self._cancelled = False
    
    def cancel(self):
        """Cancela a operação"""
        self._cancelled = True
    
    def run(self):
        """Executa tradução automática com segurança"""
        try:
            results = {}
            total = len(self.texts)
            monitor = ResourceMonitor()
            
            for i, text in enumerate(self.texts):
                if self._cancelled:
                    self.status.emit("Operação cancelada")
                    break
                
                # Verifica recursos periodicamente
                if i % 10 == 0:
                    ok, msg = monitor.check_resources()
                    if not ok:
                        monitor.force_gc_if_needed()
                
                # Primeiro tenta tradução inteligente
                translation = self.smart_translator.translate(text)
                
                # Se não encontrou, tenta API
                if not translation and self.api_manager.active_api:
                    translation = self.api_manager.translate(text)
                
                if translation:
                    results[text] = translation
                
                # Atualiza progresso
                progress_value = int((i + 1) / total * 100)
                self.progress.emit(progress_value)
                self.status.emit(f"Traduzindo {i+1}/{total}...")
            
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))

class FileLoadWorker(QThread):
    """Thread para carregar arquivos grandes"""
    
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(list)
    error = Signal(str)
    
    def __init__(self, file_processor, filepath, profile):
        super().__init__()
        self.file_processor = file_processor
        self.filepath = filepath
        self.profile = profile
    
    def run(self):
        """Carrega arquivo com segurança"""
        try:
            self.status.emit("Validando arquivo...")
            
            # Valida arquivo
            ok, msg = SecurityValidator.validate_file_path(self.filepath)
            if not ok:
                self.error.emit(msg)
                return
            
            ok, msg = SecurityValidator.validate_file_size(self.filepath)
            if not ok:
                self.error.emit(msg)
                return
            
            self.progress.emit(20)
            self.status.emit("Carregando arquivo...")
            
            # Carrega arquivo
            if not self.file_processor.load_file(self.filepath):
                self.error.emit("Falha ao carregar arquivo")
                return
            
            self.progress.emit(50)
            self.status.emit("Extraindo textos...")
            
            # Extrai textos
            entries = self.file_processor.extract_texts()
            
            # Valida quantidade
            if len(entries) > LIMITS.MAX_ENTRIES_PER_FILE:
                self.error.emit(f"Arquivo muito grande: {len(entries)} entradas (máximo: {LIMITS.MAX_ENTRIES_PER_FILE})")
                return
            
            self.progress.emit(100)
            self.finished.emit(entries)
            
        except Exception as e:
            self.error.emit(str(e))

# ============================================================================
# DIÁLOGOS
# ============================================================================

class DatabaseSelectorDialog(QDialog):
    """Diálogo para selecionar ou criar banco de dados"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.selected_db_path = None
        
        self.setWindowTitle("Selecionar Banco de Dados")
        self.setGeometry(300, 300, 500, 200)
        self.setModal(True)
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Informação
        info_label = QLabel(
            "Selecione um banco de dados existente ou crie um novo.\n"
            "O banco de dados armazena todas as suas traduções."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Campo de caminho
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Caminho do banco de dados (.db)")
        path_layout.addWidget(self.path_input)
        
        btn_browse = QPushButton("Procurar...")
        btn_browse.clicked.connect(self.browse_database)
        path_layout.addWidget(btn_browse)
        
        layout.addLayout(path_layout)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        btn_new = QPushButton("Criar Novo")
        btn_new.clicked.connect(self.create_new_database)
        buttons_layout.addWidget(btn_new)
        
        btn_open = QPushButton("Abrir Selecionado")
        btn_open.clicked.connect(self.open_selected)
        buttons_layout.addWidget(btn_open)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancel)
        
        layout.addLayout(buttons_layout)
    
    def browse_database(self):
        """Procura um banco de dados existente"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Banco de Dados",
            "",
            "Banco de Dados (*.db);;Todos os Arquivos (*)"
        )
        
        if filepath:
            self.path_input.setText(filepath)
    
    def create_new_database(self):
        """Cria um novo banco de dados"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Criar Novo Banco de Dados",
            "translation_memory.db",
            "Banco de Dados (*.db)"
        )
        
        if filepath:
            if not filepath.endswith('.db'):
                filepath += '.db'
            
            if create_new_database(filepath):
                self.selected_db_path = filepath
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", "Falha ao criar banco de dados")
    
    def open_selected(self):
        """Abre o banco de dados selecionado"""
        filepath = self.path_input.text().strip()
        
        if not filepath:
            QMessageBox.warning(self, "Aviso", "Selecione um banco de dados")
            return
        
        if not os.path.exists(filepath):
            QMessageBox.warning(self, "Aviso", "Arquivo não encontrado")
            return
        
        self.selected_db_path = filepath
        self.accept()

class DatabaseViewerDialog(QDialog):
    """Diálogo para visualizar e gerenciar o banco de dados"""
    
    def __init__(self, parent, translation_memory: TranslationMemory):
        super().__init__(parent)
        
        self.translation_memory = translation_memory
        
        self.setWindowTitle("Visualizador de Banco de Dados")
        self.setGeometry(150, 150, 1000, 600)
        
        self._create_ui()
        self._load_data()
    
    def _create_ui(self):
        """Cria interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Informações do banco
        info_layout = QHBoxLayout()
        
        stats = self.translation_memory.get_stats()
        self.info_label = QLabel(
            f"📁 Banco: {stats.get('db_path', 'Não conectado')} | "
            f"📊 Total: {stats['total_translations']} traduções | "
            f"🔄 Usos: {stats['total_usage']}"
        )
        info_layout.addWidget(self.info_label)
        
        layout.addLayout(info_layout)
        
        # Barra de busca
        search_layout = QHBoxLayout()
        
        search_layout.addWidget(QLabel("Buscar:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite para buscar...")
        self.search_input.textChanged.connect(self._on_search)
        search_layout.addWidget(self.search_input)
        
        search_layout.addWidget(QLabel("Categoria:"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("Todas")
        self.category_combo.addItems(self.translation_memory.get_categories())
        self.category_combo.currentTextChanged.connect(self._on_filter)
        search_layout.addWidget(self.category_combo)
        
        btn_refresh = QPushButton("🔄 Atualizar")
        btn_refresh.clicked.connect(self._load_data)
        search_layout.addWidget(btn_refresh)
        
        layout.addLayout(search_layout)
        
        # Tabela de traduções
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Texto Original", "Tradução", "Categoria", "Usos", "Atualizado"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # Permite ajuste manual pelo usuário
        header.setSectionResizeMode(2, QHeaderView.Interactive)  # Permite ajuste manual pelo usuário
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        # Define larguras iniciais para as colunas ajustáveis
        self.table.setColumnWidth(1, 350)  # Texto Original
        self.table.setColumnWidth(2, 350)  # Tradução
        
        # Conecta redimensionamento de coluna para reajustar altura das linhas
        header.sectionResized.connect(self._auto_adjust_row_heights)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # Adiciona atalho da tecla Delete para excluir
        delete_shortcut = QShortcut(QKeySequence.Delete, self.table)
        delete_shortcut.activated.connect(self._delete_selected)
        
        layout.addWidget(self.table)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        btn_edit = QPushButton("✏️ Editar Selecionado")
        btn_edit.clicked.connect(self._edit_selected)
        buttons_layout.addWidget(btn_edit)
        
        btn_delete = QPushButton("🗑️ Excluir Selecionado")
        btn_delete.clicked.connect(self._delete_selected)
        buttons_layout.addWidget(btn_delete)
        
        btn_export = QPushButton("📤 Exportar CSV")
        btn_export.clicked.connect(self._export_csv)
        buttons_layout.addWidget(btn_export)
        
        btn_import = QPushButton("📥 Importar CSV")
        btn_import.clicked.connect(self._import_csv)
        buttons_layout.addWidget(btn_import)
        
        buttons_layout.addStretch()
        
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_close)
        
        layout.addLayout(buttons_layout)
    
    def _load_data(self, search_term: str = None, category: str = None):
        """Carrega dados na tabela"""
        if category == "Todas":
            category = None
        
        translations = self.translation_memory.get_all_translations(
            category=category,
            search_term=search_term
        )
        
        self.table.setRowCount(len(translations))
        
        for i, t in enumerate(translations):
            self.table.setItem(i, 0, QTableWidgetItem(str(t['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(t['original_text'][:100]))
            self.table.setItem(i, 2, QTableWidgetItem(t['translated_text'][:100]))
            self.table.setItem(i, 3, QTableWidgetItem(t['category']))
            self.table.setItem(i, 4, QTableWidgetItem(str(t['usage_count'])))
            self.table.setItem(i, 5, QTableWidgetItem(t['updated_at'][:10] if t['updated_at'] else ''))
            
            # Torna ID não editável
            self.table.item(i, 0).setFlags(self.table.item(i, 0).flags() & ~Qt.ItemIsEditable)
        
        # Auto-ajusta altura das linhas após carregar dados
        self._auto_adjust_row_heights()
    
    def _on_search(self, text):
        """Callback de busca"""
        category = self.category_combo.currentText()
        self._load_data(search_term=text if text else None, 
                       category=category if category != "Todas" else None)
    
    def _on_filter(self, category):
        """Callback de filtro por categoria"""
        search = self.search_input.text()
        self._load_data(search_term=search if search else None,
                       category=category if category != "Todas" else None)
    
    def _on_item_double_clicked(self, item):
        """Callback de duplo clique - auto-ajusta altura e inicia edição"""
        # Auto-ajusta altura das linhas quando começar a editar
        self._auto_adjust_row_heights()
        # Nota: A edição será iniciada pelo método _edit_selected se necessário
        self._edit_selected()
    
    def _auto_adjust_row_heights(self):
        """
        Auto-ajusta a altura das linhas baseado no conteúdo.
        
        Calcula a altura necessária para cada linha considerando:
        - Comprimento do texto nas colunas Original e Tradução
        - Largura disponível na coluna
        - Padding adicional para textos longos
        
        Aplica altura mínima padrão e aumenta conforme necessário.
        """
        # Altura mínima padrão
        min_height = 30
        
        # Calcula a altura de cada linha baseado no conteúdo
        for row in range(self.table.rowCount()):
            max_height = min_height
            
            # Verifica colunas de texto (Original e Tradução)
            for col in [1, 2]:  # Apenas colunas de texto original e tradução
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    
                    # Calcula altura baseado no comprimento do texto
                    # Usa a largura da coluna para estimar quebras de linha
                    col_width = self.table.columnWidth(col)
                    
                    if col_width > 0 and text:
                        # Estima quantos caracteres cabem por linha
                        # Usa aproximação de 8 pixels por caractere
                        chars_per_line = max(1, col_width // 8)
                        
                        # Calcula número de linhas necessárias
                        num_lines = max(1, len(text) // chars_per_line + 1)
                        
                        # Altura base por linha de texto (considera fonte e padding)
                        height_per_line = 20
                        
                        # Calcula altura necessária
                        required_height = num_lines * height_per_line + 10  # +10 para padding
                        
                        # Adiciona padding extra para textos muito longos
                        if len(text) > 200:
                            required_height += 10
                        elif len(text) > 100:
                            required_height += 5
                        
                        max_height = max(max_height, required_height)
            
            # Define altura máxima razoável para evitar linhas gigantes
            max_allowed_height = 200
            final_height = min(max_height, max_allowed_height)
            
            # Aplica a altura calculada
            self.table.setRowHeight(row, final_height)
    
    def _edit_selected(self):
        """Edita tradução selecionada"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Aviso", "Selecione uma tradução para editar")
            return
        
        row = selected[0].row()
        translation_id = int(self.table.item(row, 0).text())
        
        # Busca dados completos
        data = self.translation_memory.get_translation_by_id(translation_id)
        if not data:
            return
        
        # Diálogo de edição
        dialog = EditTranslationDialog(self, data)
        if dialog.exec() == QDialog.Accepted:
            # Atualiza no banco
            self.translation_memory.update_translation(
                translation_id,
                translated_text=dialog.translated_text,
                category=dialog.category,
                notes=dialog.notes
            )
            self._load_data()
    
    def _delete_selected(self):
        """Exclui tradução selecionada"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Aviso", "Selecione uma tradução para excluir")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir a tradução selecionada?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            row = selected[0].row()
            translation_id = int(self.table.item(row, 0).text())
            
            if self.translation_memory.delete_translation(translation_id):
                self._load_data()
                QMessageBox.information(self, "Sucesso", "Tradução excluída!")
    
    def _export_csv(self):
        """Exporta para CSV"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar para CSV",
            "translations.csv",
            "CSV Files (*.csv)"
        )
        
        if filepath:
            if self.translation_memory.export_to_file(filepath):
                QMessageBox.information(self, "Sucesso", f"Exportado para:\n{filepath}")
            else:
                QMessageBox.critical(self, "Erro", "Falha ao exportar")
    
    def _import_csv(self):
        """Importa de CSV"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Importar de CSV",
            "",
            "CSV Files (*.csv)"
        )
        
        if filepath:
            imported, errors = self.translation_memory.import_from_file(filepath)
            QMessageBox.information(
                self, 
                "Importação Concluída",
                f"Importados: {imported}\nErros: {errors}"
            )
            self._load_data()

class EditTranslationDialog(QDialog):
    """Diálogo para editar uma tradução"""
    
    def __init__(self, parent, data: dict):
        super().__init__(parent)
        
        self.data = data
        self.translated_text = data['translated_text']
        self.category = data['category']
        self.notes = data['notes']
        
        self.setWindowTitle("Editar Tradução")
        self.setGeometry(350, 350, 500, 300)
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface"""
        layout = QVBoxLayout(self)
        
        # Texto original (somente leitura)
        layout.addWidget(QLabel("Texto Original:"))
        original_text = QTextEdit()
        original_text.setPlainText(self.data['original_text'])
        original_text.setReadOnly(True)
        original_text.setMaximumHeight(80)
        layout.addWidget(original_text)
        
        # Tradução
        layout.addWidget(QLabel("Tradução:"))
        self.translation_input = QTextEdit()
        self.translation_input.setPlainText(self.data['translated_text'])
        self.translation_input.setMaximumHeight(80)
        layout.addWidget(self.translation_input)
        
        # Categoria
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Categoria:"))
        self.category_input = QLineEdit()
        self.category_input.setText(self.data['category'])
        cat_layout.addWidget(self.category_input)
        layout.addLayout(cat_layout)
        
        # Notas
        layout.addWidget(QLabel("Notas:"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(self.data['notes'])
        self.notes_input.setMaximumHeight(60)
        layout.addWidget(self.notes_input)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        btn_save = QPushButton("Salvar")
        btn_save.clicked.connect(self._save)
        buttons_layout.addWidget(btn_save)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancel)
        
        layout.addLayout(buttons_layout)
    
    def _save(self):
        """Salva alterações"""
        self.translated_text = self.translation_input.toPlainText()
        self.category = self.category_input.text()
        self.notes = self.notes_input.toPlainText()
        self.accept()

class SettingsDialog(QDialog):
    """Diálogo de configurações"""
    
    def __init__(self, parent, api_manager, translation_memory, profile_manager):
        super().__init__(parent)
        
        self.api_manager = api_manager
        self.translation_memory = translation_memory
        self.profile_manager = profile_manager
        
        self.setWindowTitle("Configurações")
        self.setGeometry(200, 200, 600, 500)
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Tabs
        tabs = QTabWidget()
        
        # Tab de API
        api_tab = QWidget()
        api_layout = QVBoxLayout(api_tab)
        
        # Informação sobre APIs gratuitas
        info_label = QLabel(
            "💡 <b>APIs Gratuitas Disponíveis:</b><br>"
            "• <b>LibreTranslate</b> - 100% gratuito, sem limites<br>"
            "• <b>MyMemory</b> - Gratuito, 5000 chars/dia<br>"
            "• <b>DeepL Free</b> - 500.000 chars/mês<br>"
            "• <b>Google Free</b> - 500.000 chars/mês"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background-color: #2d5a27; padding: 10px; border-radius: 5px;")
        api_layout.addWidget(info_label)
        
        # Status das APIs configuradas
        status_group = QGroupBox("📋 Status das APIs Configuradas")
        status_layout = QVBoxLayout()
        self.api_status_labels = {}
        
        # Obtém informações das APIs
        available_apis = self.api_manager.get_available_apis()
        
        # DeepL
        deepl_status = "✅ Configurada" if 'deepl' in available_apis else "⏳ Não configurada"
        self.api_status_labels['deepl'] = QLabel(f"<b>DeepL:</b> {deepl_status}")
        status_layout.addWidget(self.api_status_labels['deepl'])
        
        # Google
        google_status = "✅ Configurada" if 'google' in available_apis else "⏳ Não configurada"
        self.api_status_labels['google'] = QLabel(f"<b>Google:</b> {google_status}")
        status_layout.addWidget(self.api_status_labels['google'])
        
        # MyMemory
        mymemory_status = "✅ Configurada" if 'mymemory' in available_apis else "⏳ Não configurada"
        self.api_status_labels['mymemory'] = QLabel(f"<b>MyMemory:</b> {mymemory_status}")
        status_layout.addWidget(self.api_status_labels['mymemory'])
        
        # LibreTranslate
        libre_status = "✅ Configurada" if 'libre' in available_apis else "⏳ Não configurada"
        self.api_status_labels['libre'] = QLabel(f"<b>LibreTranslate:</b> {libre_status}")
        status_layout.addWidget(self.api_status_labels['libre'])
        
        status_group.setLayout(status_layout)
        api_layout.addWidget(status_group)
        
        # APIs Gratuitas (sem chave)
        free_group = QGroupBox("🆓 APIs Gratuitas (Sem Chave)")
        free_layout = QVBoxLayout()
        
        # LibreTranslate
        libre_layout = QHBoxLayout()
        libre_layout.addWidget(QLabel("LibreTranslate:"))
        self.libre_server_input = QLineEdit()
        self.libre_server_input.setPlaceholderText("URL do servidor (deixe vazio para servidor público)")
        libre_layout.addWidget(self.libre_server_input)
        btn_save_libre = QPushButton("Ativar")
        btn_save_libre.clicked.connect(self.save_libre)
        libre_layout.addWidget(btn_save_libre)
        free_layout.addLayout(libre_layout)
        
        # MyMemory
        mymemory_layout = QHBoxLayout()
        mymemory_layout.addWidget(QLabel("MyMemory:"))
        self.mymemory_email_input = QLineEdit()
        self.mymemory_email_input.setPlaceholderText("Email (opcional, aumenta limite diário)")
        mymemory_layout.addWidget(self.mymemory_email_input)
        btn_save_mymemory = QPushButton("Ativar")
        btn_save_mymemory.clicked.connect(self.save_mymemory)
        mymemory_layout.addWidget(btn_save_mymemory)
        free_layout.addLayout(mymemory_layout)
        
        free_group.setLayout(free_layout)
        api_layout.addWidget(free_group)
        
        # APIs com Chave (Planos Gratuitos)
        paid_group = QGroupBox("🔑 APIs com Chave (Planos Gratuitos Disponíveis)")
        paid_layout = QVBoxLayout()
        
        # DeepL
        deepl_layout = QHBoxLayout()
        deepl_layout.addWidget(QLabel("DeepL:"))
        self.deepl_key_input = QLineEdit()
        self.deepl_key_input.setPlaceholderText("Chave API (gratuita em deepl.com/pro-api)")
        self.deepl_key_input.setEchoMode(QLineEdit.Password)
        deepl_layout.addWidget(self.deepl_key_input)
        btn_save_deepl = QPushButton("Salvar")
        btn_save_deepl.clicked.connect(self.save_deepl_key)
        deepl_layout.addWidget(btn_save_deepl)
        paid_layout.addLayout(deepl_layout)
        
        # Google
        google_layout = QHBoxLayout()
        google_layout.addWidget(QLabel("Google:"))
        self.google_key_input = QLineEdit()
        self.google_key_input.setPlaceholderText("Chave API (gratuita em cloud.google.com)")
        self.google_key_input.setEchoMode(QLineEdit.Password)
        google_layout.addWidget(self.google_key_input)
        btn_save_google = QPushButton("Salvar")
        btn_save_google.clicked.connect(self.save_google_key)
        google_layout.addWidget(btn_save_google)
        paid_layout.addLayout(google_layout)
        
        paid_group.setLayout(paid_layout)
        api_layout.addWidget(paid_group)
        
        # Seletor de API ativa
        active_group = QGroupBox("⚡ API Ativa")
        active_layout = QHBoxLayout()
        active_layout.addWidget(QLabel("Usar:"))
        self.combo_active_api = QComboBox()
        self.combo_active_api.addItems(["Nenhuma"] + self.api_manager.get_available_apis())
        self.combo_active_api.currentTextChanged.connect(self._on_api_changed)
        active_layout.addWidget(self.combo_active_api)
        active_group.setLayout(active_layout)
        api_layout.addWidget(active_group)
        
        # Estatísticas de uso
        self.usage_group = QGroupBox("📊 Uso das APIs (Este Mês)")
        self.usage_layout = QVBoxLayout()
        self._update_usage_display()
        self.usage_group.setLayout(self.usage_layout)
        api_layout.addWidget(self.usage_group)
        
        btn_refresh_usage = QPushButton("Atualizar Estatísticas")
        btn_refresh_usage.clicked.connect(self._update_usage_display)
        api_layout.addWidget(btn_refresh_usage)
        
        api_layout.addStretch()
        tabs.addTab(api_tab, "APIs de Tradução")
        
        # Tab de Segurança
        security_tab = QWidget()
        security_layout = QVBoxLayout(security_tab)
        
        security_group = QGroupBox("Limites de Segurança")
        limits_layout = QVBoxLayout()
        
        limits_layout.addWidget(QLabel(f"• Tamanho máximo de arquivo: {LIMITS.MAX_FILE_SIZE_MB} MB"))
        limits_layout.addWidget(QLabel(f"• Uso máximo de memória: {LIMITS.MAX_MEMORY_USAGE_MB} MB"))
        limits_layout.addWidget(QLabel(f"• Uso máximo de CPU: {LIMITS.MAX_CPU_PERCENT}%"))
        limits_layout.addWidget(QLabel(f"• Máximo de entradas por arquivo: {LIMITS.MAX_ENTRIES_PER_FILE}"))
        limits_layout.addWidget(QLabel(f"• Timeout de operações: {LIMITS.OPERATION_TIMEOUT_SEC}s"))
        
        security_group.setLayout(limits_layout)
        security_layout.addWidget(security_group)
        
        # Monitor de recursos
        monitor_group = QGroupBox("Monitor de Recursos")
        monitor_layout = QVBoxLayout()
        
        monitor = ResourceMonitor()
        self.memory_label = QLabel(f"Memória em uso: {monitor.get_memory_usage_mb():.1f} MB")
        self.cpu_label = QLabel(f"CPU: {monitor.get_cpu_percent():.1f}%")
        
        monitor_layout.addWidget(self.memory_label)
        monitor_layout.addWidget(self.cpu_label)
        
        btn_refresh_monitor = QPushButton("Atualizar")
        btn_refresh_monitor.clicked.connect(self._refresh_monitor)
        monitor_layout.addWidget(btn_refresh_monitor)
        
        monitor_group.setLayout(monitor_layout)
        security_layout.addWidget(monitor_group)
        
        security_layout.addStretch()
        tabs.addTab(security_tab, "Segurança")
        
        # Tab de Logs
        logs_tab = QWidget()
        logs_layout = QVBoxLayout(logs_tab)
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlainText(app_logger.get_recent_logs(100))
        logs_layout.addWidget(self.logs_text)
        
        btn_refresh_logs = QPushButton("Atualizar Logs")
        btn_refresh_logs.clicked.connect(lambda: self.logs_text.setPlainText(app_logger.get_recent_logs(100)))
        logs_layout.addWidget(btn_refresh_logs)
        
        tabs.addTab(logs_tab, "Logs")
        
        layout.addWidget(tabs)
        
        # Botão fechar
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
    
    def save_libre(self):
        """Ativa LibreTranslate (gratuito)"""
        server = self.libre_server_input.text().strip() or None
        self.api_manager.add_libre(server)
        self._refresh_api_combo()
        self._update_api_status()
        QMessageBox.information(
            self, 
            "Sucesso", 
            "LibreTranslate ativado!\n\n"
            "🎉 Esta API é 100% gratuita e sem limites de uso!"
        )
        app_logger.info("LibreTranslate configurado")
    
    def save_mymemory(self):
        """Ativa MyMemory (gratuito)"""
        email = self.mymemory_email_input.text().strip() or None
        self.api_manager.add_mymemory(email)
        self._refresh_api_combo()
        self._update_api_status()
        limit = "10.000 chars/dia" if email else "5.000 chars/dia"
        QMessageBox.information(
            self, 
            "Sucesso", 
            f"MyMemory ativado!\n\n"
            f"🎉 Limite gratuito: {limit}"
        )
        app_logger.info("MyMemory configurado")
    
    def save_deepl_key(self):
        """Salva chave DeepL"""
        key = self.deepl_key_input.text().strip()
        if key:
            self.api_manager.add_deepl(key)
            self._refresh_api_combo()
            self._update_api_status()
            QMessageBox.information(
                self, 
                "Sucesso", 
                "Chave DeepL salva!\n\n"
                "📊 Limite gratuito: 500.000 chars/mês"
            )
            app_logger.info("Chave DeepL configurada")
        else:
            QMessageBox.warning(self, "Erro", "Digite uma chave válida!")
    
    def save_google_key(self):
        """Salva chave Google"""
        key = self.google_key_input.text().strip()
        if key:
            self.api_manager.add_google(key)
            self._refresh_api_combo()
            self._update_api_status()
            QMessageBox.information(
                self, 
                "Sucesso", 
                "Chave Google salva!\n\n"
                "📊 Limite gratuito: 500.000 chars/mês"
            )
            app_logger.info("Chave Google configurada")
        else:
            QMessageBox.warning(self, "Erro", "Digite uma chave válida!")
    
    def _refresh_api_combo(self):
        """Atualiza combo de APIs disponíveis"""
        self.combo_active_api.clear()
        self.combo_active_api.addItems(["Nenhuma"] + self.api_manager.get_available_apis())
    
    def _update_api_status(self):
        """Atualiza os indicadores de status das APIs configuradas"""
        available_apis = self.api_manager.get_available_apis()
        
        # Atualiza DeepL
        if 'deepl' in self.api_status_labels:
            deepl_status = "✅ Configurada" if 'deepl' in available_apis else "⏳ Não configurada"
            self.api_status_labels['deepl'].setText(f"<b>DeepL:</b> {deepl_status}")
        
        # Atualiza Google
        if 'google' in self.api_status_labels:
            google_status = "✅ Configurada" if 'google' in available_apis else "⏳ Não configurada"
            self.api_status_labels['google'].setText(f"<b>Google:</b> {google_status}")
        
        # Atualiza MyMemory
        if 'mymemory' in self.api_status_labels:
            mymemory_status = "✅ Configurada" if 'mymemory' in available_apis else "⏳ Não configurada"
            self.api_status_labels['mymemory'].setText(f"<b>MyMemory:</b> {mymemory_status}")
        
        # Atualiza LibreTranslate
        if 'libre' in self.api_status_labels:
            libre_status = "✅ Configurada" if 'libre' in available_apis else "⏳ Não configurada"
            self.api_status_labels['libre'].setText(f"<b>LibreTranslate:</b> {libre_status}")
    
    def _on_api_changed(self, api_name):
        """Callback quando API é alterada"""
        if api_name != "Nenhuma":
            self.api_manager.set_active_api(api_name)
            app_logger.info(f"API ativa alterada para: {api_name}")
    
    def _update_usage_display(self):
        """Atualiza exibição de uso das APIs"""
        # Limpa layout anterior
        while self.usage_layout.count():
            item = self.usage_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Obtém estatísticas
        stats = self.api_manager.get_usage_stats()
        
        # DeepL
        deepl = stats.get('deepl', {})
        deepl_used = deepl.get('used', 0)
        deepl_limit = deepl.get('limit', 500000)
        deepl_pct = (deepl_used / deepl_limit * 100) if deepl_limit > 0 else 0
        self.usage_layout.addWidget(QLabel(
            f"DeepL: {deepl_used:,} / {deepl_limit:,} chars ({deepl_pct:.1f}%)"
        ))
        
        # Google
        google = stats.get('google', {})
        google_used = google.get('used', 0)
        google_limit = google.get('limit', 500000)
        google_pct = (google_used / google_limit * 100) if google_limit > 0 else 0
        self.usage_layout.addWidget(QLabel(
            f"Google: {google_used:,} / {google_limit:,} chars ({google_pct:.1f}%)"
        ))
        
        # MyMemory
        mymemory = stats.get('mymemory', {})
        mm_used = mymemory.get('used_today', 0)
        mm_limit = mymemory.get('daily_limit', 5000)
        mm_pct = (mm_used / mm_limit * 100) if mm_limit > 0 else 0
        self.usage_layout.addWidget(QLabel(
            f"MyMemory (hoje): {mm_used:,} / {mm_limit:,} chars ({mm_pct:.1f}%)"
        ))
        
        # LibreTranslate
        self.usage_layout.addWidget(QLabel(
            "LibreTranslate: ∞ (sem limites)"
        ))
    
    def _refresh_monitor(self):
        """Atualiza monitor de recursos"""
        monitor = ResourceMonitor()
        self.memory_label.setText(f"Memória em uso: {monitor.get_memory_usage_mb():.1f} MB")
        self.cpu_label.setText(f"CPU: {monitor.get_cpu_percent():.1f}%")

# ============================================================================
# JANELA PRINCIPAL
# ============================================================================

class MainWindow(QMainWindow):
    """Janela principal do aplicativo"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializa componentes
        self.translation_memory = TranslationMemory()  # Sem conexão inicial
        self.profile_manager = RegexProfileManager()
        self.smart_translator = None  # Inicializado após conectar ao banco
        self.api_manager = TranslationAPIManager()
        self.file_processor = None
        self.current_file = None
        self.entries = []
        
        # Monitor de recursos
        self.resource_monitor = ResourceMonitor()
        
        # Configura interface
        self.setWindowTitle("Game Translator - Sistema de Tradução para Jogos e Mods")
        self.setGeometry(DEFAULT_WINDOW_X, DEFAULT_WINDOW_Y, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Aplica tema escuro
        self._apply_dark_theme()
        
        # Cria interface
        self._create_menu_bar()
        self._create_ui()
        self._create_status_bar()
        
        # Restaura configurações da janela após UI estar criada
        self._restore_window_settings()
        
        # Timer para atualizar status de recursos
        self.resource_timer = QTimer()
        self.resource_timer.timeout.connect(self._update_resource_status)
        self.resource_timer.start(5000)  # A cada 5 segundos
        
        # Log inicial
        app_logger.info("Aplicativo iniciado")
        
        # Solicita seleção de banco de dados
        QTimer.singleShot(100, self._prompt_database_selection)
    
    def _apply_dark_theme(self):
        """Aplica tema escuro profissional"""
        palette = QPalette()
        
        # Cores principais
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
        palette.setColor(QPalette.ToolTipBase, QColor(220, 220, 220))
        palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
        palette.setColor(QPalette.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)
        
        # Estilo adicional
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px 16px;
                color: #dcdcdc;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666;
            }
            QTableWidget {
                background-color: #282828;
                alternate-background-color: #323232;
                gridline-color: #444;
                border: 1px solid #555;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2a82da;
            }
            QHeaderView::section {
                background-color: #3a3a3a;
                padding: 8px;
                border: 1px solid #555;
                font-weight: bold;
            }
            QComboBox {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                color: #dcdcdc;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 1px solid #666;
            }
            QComboBox::drop-down {
                border: none;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 4px;
                text-align: center;
                background-color: #282828;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
            }
            QLineEdit {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                color: #dcdcdc;
            }
            QLabel {
                color: #dcdcdc;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QMenuBar {
                background-color: #2a2a2a;
                color: #dcdcdc;
            }
            QMenuBar::item:selected {
                background-color: #3a3a3a;
            }
            QMenu {
                background-color: #2a2a2a;
                color: #dcdcdc;
                border: 1px solid #555;
            }
            QMenu::item:selected {
                background-color: #2a82da;
            }
            QStatusBar {
                background-color: #2a2a2a;
                color: #dcdcdc;
            }
            QTabWidget::pane {
                border: 1px solid #555;
            }
            QTabBar::tab {
                background-color: #3a3a3a;
                color: #dcdcdc;
                padding: 8px 16px;
                border: 1px solid #555;
            }
            QTabBar::tab:selected {
                background-color: #2a82da;
            }
            QTextEdit {
                background-color: #282828;
                color: #dcdcdc;
                border: 1px solid #555;
            }
        """)
    
    def _create_menu_bar(self):
        """Cria barra de menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        action_new_db = QAction("Novo Banco de Dados...", self)
        action_new_db.setShortcut("Ctrl+Shift+N")
        action_new_db.triggered.connect(self._create_new_database)
        file_menu.addAction(action_new_db)
        
        action_open_db = QAction("Abrir Banco de Dados...", self)
        action_open_db.setShortcut("Ctrl+D")
        action_open_db.triggered.connect(self._open_database)
        file_menu.addAction(action_open_db)
        
        file_menu.addSeparator()
        
        action_import = QAction("Importar Arquivo...", self)
        action_import.setShortcut("Ctrl+O")
        action_import.triggered.connect(self.import_file)
        file_menu.addAction(action_import)
        
        action_save = QAction("Salvar Arquivo", self)
        action_save.setShortcut("Ctrl+S")
        action_save.triggered.connect(self.save_file)
        file_menu.addAction(action_save)
        
        file_menu.addSeparator()
        
        action_exit = QAction("Sair", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)
        
        # Menu Banco de Dados
        db_menu = menubar.addMenu("Banco de Dados")
        
        action_view_db = QAction("Visualizar Banco de Dados...", self)
        action_view_db.setShortcut("Ctrl+B")
        action_view_db.triggered.connect(self._view_database)
        db_menu.addAction(action_view_db)
        
        action_export_db = QAction("Exportar para CSV...", self)
        action_export_db.setShortcut("Ctrl+E")
        action_export_db.triggered.connect(self._export_database)
        db_menu.addAction(action_export_db)
        
        action_import_db = QAction("Importar de CSV...", self)
        action_import_db.triggered.connect(self._import_database)
        db_menu.addAction(action_import_db)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu("Ferramentas")
        
        action_profiles = QAction("Gerenciar Perfis Regex...", self)
        action_profiles.setShortcut("Ctrl+P")
        action_profiles.triggered.connect(self._open_profile_manager)
        tools_menu.addAction(action_profiles)
        
        action_import_trans = QAction("Importar Traduções...", self)
        action_import_trans.setShortcut("Ctrl+I")
        action_import_trans.triggered.connect(self._import_translations)
        tools_menu.addAction(action_import_trans)
        
        tools_menu.addSeparator()
        
        action_settings = QAction("Configurações...", self)
        action_settings.setShortcut("Ctrl+,")
        action_settings.triggered.connect(self.open_settings)
        tools_menu.addAction(action_settings)
        
        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        
        action_shortcuts = QAction("Atalhos de Teclado", self)
        action_shortcuts.setShortcut("F1")
        action_shortcuts.triggered.connect(self._show_shortcuts)
        help_menu.addAction(action_shortcuts)
        
        help_menu.addSeparator()
        
        action_about = QAction("Sobre", self)
        action_about.triggered.connect(self._show_about)
        help_menu.addAction(action_about)
    
    def _create_ui(self):
        """Cria a interface do usuário"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Cabeçalho
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Info do banco de dados
        self.db_info_label = QLabel("⚠️ Nenhum banco de dados conectado")
        self.db_info_label.setStyleSheet("color: #ffa500; font-weight: bold;")
        main_layout.addWidget(self.db_info_label)
        
        # Barra de ferramentas
        toolbar_layout = self._create_toolbar()
        main_layout.addLayout(toolbar_layout)
        
        # Tabela de traduções
        self.table = self._create_translation_table()
        main_layout.addWidget(self.table)
        
        # Barra de progresso
        progress_layout = QHBoxLayout()
        self.status_label = QLabel("Pronto")
        progress_layout.addWidget(self.status_label)
        progress_layout.addStretch()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(300)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        main_layout.addLayout(progress_layout)
    
    def _create_header(self):
        """Cria o cabeçalho da aplicação"""
        layout = QVBoxLayout()
        
        title = QLabel("Game Translator")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Sistema Profissional de Tradução para Jogos e Mods")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        return layout
    
    def _create_toolbar(self):
        """Cria a barra de ferramentas"""
        layout = QHBoxLayout()
        
        # Botão importar arquivo
        self.btn_import = QPushButton("📁 Importar Arquivo")
        self.btn_import.clicked.connect(self.import_file)
        layout.addWidget(self.btn_import)
        
        # Seletor de perfil
        layout.addWidget(QLabel("Perfil:"))
        self.combo_profile = QComboBox()
        self.combo_profile.addItems(self.profile_manager.get_all_profile_names())
        layout.addWidget(self.combo_profile)
        
        # Botão editar perfis
        self.btn_edit_profiles = QPushButton("✏️")
        self.btn_edit_profiles.setToolTip("Gerenciar Perfis Regex (Ctrl+P)")
        self.btn_edit_profiles.setMaximumWidth(40)
        self.btn_edit_profiles.clicked.connect(self._open_profile_manager)
        layout.addWidget(self.btn_edit_profiles)
        
        # Botão traduzir automaticamente
        self.btn_auto_translate = QPushButton("🤖 Traduzir Auto (F5)")
        self.btn_auto_translate.setToolTip(
            "Traduzir usando API:\n"
            "• Sem seleção: traduz todas as linhas não traduzidas\n"
            "• Com seleção: traduz apenas as linhas selecionadas"
        )
        self.btn_auto_translate.clicked.connect(self.auto_translate)
        self.btn_auto_translate.setEnabled(False)
        self.btn_auto_translate.setShortcut("F5")
        layout.addWidget(self.btn_auto_translate)
        
        # Botão aplicar traduções inteligentes
        self.btn_smart_translate = QPushButton("⚡ Aplicar Memória")
        self.btn_smart_translate.setToolTip(
            "Aplicar traduções da memória:\n"
            "• Sem seleção: aplica a todas as linhas não traduzidas\n"
            "• Com seleção: aplica apenas às linhas selecionadas"
        )
        self.btn_smart_translate.clicked.connect(self.apply_smart_translations)
        self.btn_smart_translate.setEnabled(False)
        layout.addWidget(self.btn_smart_translate)
        
        # Botão salvar
        self.btn_save = QPushButton("💾 Salvar")
        self.btn_save.clicked.connect(self.save_file)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)
        
        # Botão visualizar banco
        self.btn_view_db = QPushButton("🗄️ Ver Banco")
        self.btn_view_db.clicked.connect(self._view_database)
        layout.addWidget(self.btn_view_db)
        
        # Botão configurações
        self.btn_settings = QPushButton("⚙️ Config")
        self.btn_settings.clicked.connect(self.open_settings)
        layout.addWidget(self.btn_settings)
        
        layout.addStretch()
        
        return layout
    
    def _create_translation_table(self):
        """Cria a tabela de traduções"""
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["#", "Texto Original", "Tradução", "Status"])
        
        # Configurações da tabela
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.ExtendedSelection)  # Permite seleção múltipla
        table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        
        # Ajusta largura das colunas
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # Permite ajuste manual pelo usuário
        header.setSectionResizeMode(2, QHeaderView.Interactive)  # Permite ajuste manual pelo usuário
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Define larguras iniciais para as colunas ajustáveis
        table.setColumnWidth(1, 400)  # Texto Original
        table.setColumnWidth(2, 400)  # Tradução
        
        # Conecta redimensionamento de coluna para reajustar altura das linhas
        header.sectionResized.connect(lambda: self._auto_adjust_row_heights())
        
        # Conecta evento de edição
        table.itemChanged.connect(self.on_translation_edited)
        
        # Auto-ajusta altura quando clicar para editar (duplo-clique ou tecla Edit)
        # Conecta ao signal de duplo-clique para ajustar antes de editar
        table.itemDoubleClicked.connect(lambda item: self._auto_adjust_row_heights())
        
        # Adiciona atalhos de copiar e colar
        copy_shortcut = QShortcut(QKeySequence.Copy, table)
        copy_shortcut.activated.connect(self.copy_selected_rows)
        
        paste_shortcut = QShortcut(QKeySequence.Paste, table)
        paste_shortcut.activated.connect(self.paste_rows)
        
        # Adiciona atalho de Delete para limpar traduções
        delete_shortcut = QShortcut(QKeySequence.Delete, table)
        delete_shortcut.activated.connect(self._clear_selected_translations)
        
        return table
    
    def _create_status_bar(self):
        """Cria a barra de status"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Labels de status
        self.stats_label = QLabel("Total: 0 | Traduzidas: 0 | Pendentes: 0")
        self.statusBar.addWidget(self.stats_label)
        
        self.statusBar.addPermanentWidget(QLabel(" | "))
        
        self.resource_label = QLabel("RAM: 0 MB | CPU: 0%")
        self.statusBar.addPermanentWidget(self.resource_label)
    
    def _update_resource_status(self):
        """Atualiza status de recursos na barra de status"""
        memory = self.resource_monitor.get_memory_usage_mb()
        cpu = self.resource_monitor.get_cpu_percent()
        
        # Cor baseada no uso
        if memory > LIMITS.MAX_MEMORY_USAGE_MB * 0.8:
            color = "#ff6b6b"  # Vermelho
        elif memory > LIMITS.MAX_MEMORY_USAGE_MB * 0.5:
            color = "#ffa500"  # Laranja
        else:
            color = "#4ecdc4"  # Verde
        
        self.resource_label.setText(f"RAM: {memory:.0f} MB | CPU: {cpu:.0f}%")
        self.resource_label.setStyleSheet(f"color: {color};")
    
    def _prompt_database_selection(self):
        """Solicita seleção de banco de dados ao iniciar"""
        dialog = DatabaseSelectorDialog(self)
        
        if dialog.exec() == QDialog.Accepted and dialog.selected_db_path:
            self._connect_database(dialog.selected_db_path)
        else:
            self.db_info_label.setText("⚠️ Nenhum banco de dados conectado - Selecione um no menu Arquivo")
    
    def _connect_database(self, db_path: str):
        """Conecta a um banco de dados"""
        if self.translation_memory.connect(db_path):
            self.smart_translator = SmartTranslator(self.translation_memory)
            
            stats = self.translation_memory.get_stats()
            self.db_info_label.setText(
                f"✅ Banco conectado: {os.path.basename(db_path)} | "
                f"📊 {stats['total_translations']} traduções"
            )
            self.db_info_label.setStyleSheet("color: #4ecdc4; font-weight: bold;")
            
            app_logger.info(f"Banco de dados conectado: {db_path}")
        else:
            QMessageBox.critical(self, "Erro", "Falha ao conectar ao banco de dados")
    
    def _create_new_database(self):
        """Cria um novo banco de dados"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Criar Novo Banco de Dados",
            "translation_memory.db",
            "Banco de Dados (*.db)"
        )
        
        if filepath:
            if not filepath.endswith('.db'):
                filepath += '.db'
            
            if create_new_database(filepath):
                self._connect_database(filepath)
            else:
                QMessageBox.critical(self, "Erro", "Falha ao criar banco de dados")
    
    def _open_database(self):
        """Abre um banco de dados existente"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Banco de Dados",
            "",
            "Banco de Dados (*.db)"
        )
        
        if filepath:
            self._connect_database(filepath)
    
    def _view_database(self):
        """Abre visualizador do banco de dados"""
        if not self.translation_memory.is_connected():
            QMessageBox.warning(self, "Aviso", "Conecte a um banco de dados primeiro")
            return
        
        dialog = DatabaseViewerDialog(self, self.translation_memory)
        dialog.exec()
    
    def _export_database(self):
        """Exporta banco de dados para CSV"""
        if not self.translation_memory.is_connected():
            QMessageBox.warning(self, "Aviso", "Conecte a um banco de dados primeiro")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar para CSV",
            "translations.csv",
            "CSV Files (*.csv)"
        )
        
        if filepath:
            if self.translation_memory.export_to_file(filepath):
                QMessageBox.information(self, "Sucesso", f"Exportado para:\n{filepath}")
            else:
                QMessageBox.critical(self, "Erro", "Falha ao exportar")
    
    def _import_database(self):
        """Importa traduções de CSV"""
        if not self.translation_memory.is_connected():
            QMessageBox.warning(self, "Aviso", "Conecte a um banco de dados primeiro")
            return
        
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Importar de CSV",
            "",
            "CSV Files (*.csv)"
        )
        
        if filepath:
            imported, errors = self.translation_memory.import_from_file(filepath)
            QMessageBox.information(
                self,
                "Importação Concluída",
                f"Importados: {imported}\nErros: {errors}"
            )
    
    def import_file(self):
        """Importa arquivo para tradução"""
        # Verifica banco de dados
        if not self.translation_memory.is_connected():
            reply = QMessageBox.question(
                self,
                "Banco de Dados",
                "Nenhum banco de dados conectado.\nDeseja selecionar um agora?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self._prompt_database_selection()
            
            if not self.translation_memory.is_connected():
                return
        
        # Verifica recursos
        ok, msg = is_safe_to_proceed()
        if not ok:
            QMessageBox.warning(self, "Recursos Insuficientes", msg)
            return
        
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo",
            "",
            "Arquivos Suportados (*.json *.xml);;Arquivos JSON (*.json);;Arquivos XML (*.xml)"
        )
        
        if not filepath:
            return
        
        try:
            self.status_label.setText("Validando arquivo...")
            self.progress_bar.setValue(10)
            
            # Valida arquivo
            ok, msg = SecurityValidator.validate_file_path(filepath)
            if not ok:
                QMessageBox.warning(self, "Arquivo Inválido", msg)
                return
            
            ok, msg = SecurityValidator.validate_file_size(filepath)
            if not ok:
                QMessageBox.warning(self, "Arquivo Muito Grande", msg)
                return
            
            app_logger.info(f"Importando arquivo: {filepath}")
            
            # Obtém perfil selecionado
            profile_name = self.combo_profile.currentText()
            profile = self.profile_manager.get_profile(profile_name)
            
            # Cria processador
            self.file_processor = FileProcessor(profile)
            
            self.status_label.setText("Carregando arquivo...")
            self.progress_bar.setValue(30)
            
            # Carrega arquivo
            if not self.file_processor.load_file(filepath):
                raise Exception("Falha ao carregar arquivo")
            
            self.status_label.setText("Extraindo textos...")
            self.progress_bar.setValue(50)
            
            # Extrai textos
            self.entries = self.file_processor.extract_texts()
            
            # Valida quantidade
            if len(self.entries) > LIMITS.MAX_ENTRIES_PER_FILE:
                QMessageBox.warning(
                    self,
                    "Arquivo Muito Grande",
                    f"O arquivo contém {len(self.entries)} entradas.\n"
                    f"Máximo permitido: {LIMITS.MAX_ENTRIES_PER_FILE}"
                )
                return
            
            self.status_label.setText("Aplicando memória de tradução...")
            self.progress_bar.setValue(70)
            
            # Aplica traduções da memória
            self._apply_memory_translations()
            
            self.status_label.setText("Atualizando interface...")
            self.progress_bar.setValue(90)
            
            # Atualiza tabela
            self._populate_table()
            
            # Atualiza status
            self.current_file = filepath
            self.status_label.setText(f"Arquivo carregado: {os.path.basename(filepath)}")
            self.progress_bar.setValue(100)
            self._update_statistics()
            
            # Habilita botões
            self.btn_auto_translate.setEnabled(True)
            self.btn_smart_translate.setEnabled(True)
            self.btn_save.setEnabled(True)
            
            app_logger.log_file_operation("import", filepath, True)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao importar arquivo:\n{str(e)}")
            app_logger.error(f"Erro ao importar arquivo: {e}", exc_info=True)
            self.status_label.setText("Erro ao carregar arquivo")
            self.progress_bar.setValue(0)
    
    def _apply_memory_translations(self):
        """Aplica traduções da memória aos textos extraídos"""
        if not self.smart_translator:
            return
        
        for entry in self.entries:
            translation = self.smart_translator.translate(entry.original_text)
            if translation:
                entry.translated_text = translation
    
    def _populate_table(self):
        """Popula a tabela com as entradas"""
        self.table.blockSignals(True)  # Bloqueia sinais durante população
        
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.entries))
        
        for i, entry in enumerate(self.entries):
            # Coluna de índice
            index_item = QTableWidgetItem(str(i + 1))
            index_item.setFlags(index_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 0, index_item)
            
            # Coluna de texto original
            original_item = QTableWidgetItem(entry.original_text)
            original_item.setFlags(original_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 1, original_item)
            
            # Coluna de tradução
            translation_item = QTableWidgetItem(entry.translated_text)
            self.table.setItem(i, 2, translation_item)
            
            # Coluna de status
            if entry.translated_text:
                status_item = QTableWidgetItem("✅")
                for col in range(4):
                    if self.table.item(i, col):
                        self.table.item(i, col).setBackground(TableColors.TRANSLATED_ROW)
            else:
                status_item = QTableWidgetItem("⏳")
            
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 3, status_item)
        
        # Auto-ajusta altura das linhas baseado no conteúdo
        self._auto_adjust_row_heights()
        
        self.table.blockSignals(False)  # Reativa sinais
    
    def _auto_adjust_row_heights(self):
        """
        Auto-ajusta a altura das linhas baseado no conteúdo.
        
        Calcula a altura necessária para cada linha considerando:
        - Comprimento do texto nas colunas Original e Tradução
        - Largura disponível na coluna
        - Padding adicional para textos longos
        
        Aplica altura mínima padrão e aumenta conforme necessário.
        """
        # Altura mínima padrão
        min_height = 30
        
        # Calcula a altura de cada linha baseado no conteúdo
        for row in range(self.table.rowCount()):
            max_height = min_height
            
            # Verifica colunas de texto (Original e Tradução)
            for col in [1, 2]:  # Apenas colunas de texto original e tradução
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    
                    # Calcula altura baseado no comprimento do texto
                    # Usa a largura da coluna para estimar quebras de linha
                    col_width = self.table.columnWidth(col)
                    
                    if col_width > 0 and text:
                        # Estima quantos caracteres cabem por linha
                        # Usa aproximação de 8 pixels por caractere
                        chars_per_line = max(1, col_width // 8)
                        
                        # Calcula número de linhas necessárias
                        num_lines = max(1, len(text) // chars_per_line + 1)
                        
                        # Altura base por linha de texto (considera fonte e padding)
                        height_per_line = 20
                        
                        # Calcula altura necessária
                        required_height = num_lines * height_per_line + 10  # +10 para padding
                        
                        # Adiciona padding extra para textos muito longos
                        if len(text) > 200:
                            required_height += 10
                        elif len(text) > 100:
                            required_height += 5
                        
                        max_height = max(max_height, required_height)
            
            # Define altura máxima razoável para evitar linhas gigantes
            max_allowed_height = 200
            final_height = min(max_height, max_allowed_height)
            
            # Aplica a altura calculada
            self.table.setRowHeight(row, final_height)
    
    def on_translation_edited(self, item):
        """Callback quando uma tradução é editada"""
        if item.column() != 2:  # Apenas coluna de tradução
            return
        
        row = item.row()
        if row < len(self.entries):
            # Atualiza entrada
            self.entries[row].translated_text = item.text()
            
            # Adiciona à memória
            original = self.entries[row].original_text
            translated = item.text()
            
            if translated and self.translation_memory.is_connected():
                self.translation_memory.add_translation(original, translated)
                
                if self.smart_translator:
                    self.smart_translator.learn_pattern(original, translated)
                
                app_logger.log_translation(original, translated, "manual")
                
                # Atualiza status visual
                self.table.item(row, 3).setText("✅")
                for col in range(4):
                    if self.table.item(row, col):
                        self.table.item(row, col).setBackground(TableColors.TRANSLATED_ROW)
            
            # Auto-ajusta altura da linha editada
            self._auto_adjust_row_heights()
            
            self._update_statistics()
    
    def _clear_selected_translations(self):
        """
        Limpa as traduções das linhas selecionadas.
        
        Funcionalidade:
        - Remove o texto de tradução das células selecionadas
        - Atualiza o status visual para "pendente" (⏳)
        - Atualiza as entradas de tradução
        - Atualiza estatísticas
        
        Operações:
        - Bloqueia sinais durante a limpeza para evitar triggers múltiplos
        - Remove cor de fundo das linhas limpas
        - Registra operação no log
        """
        selected_rows = sorted(set(item.row() for item in self.table.selectedItems()))
        
        if not selected_rows:
            self.status_label.setText("Nenhuma linha selecionada")
            return
        
        # Confirma ação
        reply = QMessageBox.question(
            self,
            "Confirmar Limpeza",
            f"Limpar tradução de {len(selected_rows)} linha(s) selecionada(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Bloqueia sinais durante atualização
        self.table.blockSignals(True)
        
        cleared_count = 0
        for row in selected_rows:
            if row < len(self.entries):
                # Limpa a tradução
                self.entries[row].translated_text = ""
                
                # Atualiza item da tabela
                translation_item = self.table.item(row, 2)
                if translation_item:
                    translation_item.setText("")
                
                # Atualiza status visual
                status_item = self.table.item(row, 3)
                if status_item:
                    status_item.setText("⏳")
                
                # Remove cor de fundo (volta ao padrão)
                for col in range(4):
                    item = self.table.item(row, col)
                    if item:
                        # Reseta cor de fundo baseado em alternating rows
                        if row % 2 == 0:
                            item.setBackground(TableColors.BASE_ROW)
                        else:
                            item.setBackground(TableColors.ALTERNATE_ROW)
                
                cleared_count += 1
        
        self.table.blockSignals(False)
        
        # Atualiza estatísticas
        self._update_statistics()
        
        self.status_label.setText(f"{cleared_count} tradução(ões) limpa(s)")
        app_logger.info(f"Limpas {cleared_count} traduções via tecla Delete")
    
    def copy_selected_rows(self):
        """
        Copia linhas selecionadas para a área de transferência.
        
        Formato de saída: TSV (tab-separated values)
        Cada linha: "Original\\tTradução"
        
        Atualiza o status da interface e registra a operação no log.
        Não requer parâmetros - opera nas linhas selecionadas na tabela.
        """
        selected_rows = sorted(set(item.row() for item in self.table.selectedItems()))
        
        if not selected_rows:
            self.status_label.setText("Nenhuma linha selecionada para copiar")
            return
        
        # Formato: Original\tTradução (tab-separated para fácil edição em notepad)
        clipboard_data = []
        for row in selected_rows:
            if row < len(self.entries):
                original = self.entries[row].original_text
                translation = self.entries[row].translated_text or ""
                clipboard_data.append(f"{original}\t{translation}")
        
        # Copia para área de transferência
        clipboard_text = "\n".join(clipboard_data)
        QApplication.clipboard().setText(clipboard_text)
        
        self.status_label.setText(f"{len(selected_rows)} linha(s) copiada(s)")
        app_logger.info(f"Copiadas {len(selected_rows)} linhas para área de transferência")
    
    def paste_rows(self):
        """
        Cola dados da área de transferência nas linhas selecionadas.
        
        Formatos aceitos:
        - TSV completo: "Original\\tTradução" (uma linha por entrada)
        - Apenas traduções: "Tradução" (uma linha por entrada)
        
        Funcionalidades:
        - Suporta diferentes quebras de linha (Windows, Unix, Mac)
        - Preserva tabs dentro do texto de tradução
        - Ignora traduções vazias após strip()
        - Atualiza automaticamente a memória de tradução
        - Valida null para todos os items da tabela
        
        Não requer parâmetros - opera nas linhas selecionadas e na área de transferência.
        """
        clipboard_text = QApplication.clipboard().text()
        
        if not clipboard_text:
            self.status_label.setText("Área de transferência vazia")
            return
        
        # Pega linhas selecionadas
        selected_rows = sorted(set(item.row() for item in self.table.selectedItems()))
        
        # Parse do conteúdo da área de transferência
        # Formato esperado: Original\tTradução (uma linha por entrada)
        # Usa splitlines() para compatibilidade com diferentes formatos de quebra de linha
        clipboard_lines = clipboard_text.strip().splitlines()
        
        if not selected_rows:
            # Se nenhuma linha selecionada, não faz nada
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione as linhas onde deseja colar as traduções."
            )
            return
        
        # Se há mais dados para colar do que linhas selecionadas
        if len(clipboard_lines) > len(selected_rows):
            reply = QMessageBox.question(
                self,
                "Confirmar Colagem",
                f"Há {len(clipboard_lines)} linha(s) na área de transferência, "
                f"mas apenas {len(selected_rows)} linha(s) selecionada(s).\n\n"
                "As primeiras linhas serão coladas nas selecionadas. Continuar?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # Cola os dados
        self.table.blockSignals(True)  # Bloqueia sinais durante atualização
        
        pasted_count = 0
        for i, row in enumerate(selected_rows):
            if i >= len(clipboard_lines):
                break
            
            if row >= len(self.entries):
                continue
            
            # Parse da linha (formato: Original\tTradução ou apenas Tradução)
            parts = clipboard_lines[i].split('\t')
            
            # Extrai a tradução baseado no número de campos
            if len(parts) >= 2:
                # Se tem original e tradução (formato TSV completo)
                # Une todos os campos após o primeiro para preservar tabs na tradução
                translation = '\t'.join(parts[1:]).strip()
            else:
                # Se tem apenas um campo, usa como tradução
                translation = parts[0].strip()
            
            # Atualiza apenas se há tradução não vazia
            # strip() já remove espaços, então a verificação 'not translation' é suficiente
            if not translation:
                continue
            
            # Atualiza entrada
            original = self.entries[row].original_text
            self.entries[row].translated_text = translation
            
            # Atualiza item da tabela (com verificação de null)
            translation_item = self.table.item(row, 2)
            if translation_item:
                translation_item.setText(translation)
            
            # Adiciona à memória
            if self.translation_memory.is_connected():
                self.translation_memory.add_translation(original, translation)
                
                if self.smart_translator:
                    self.smart_translator.learn_pattern(original, translation)
                
                app_logger.log_translation(original, translation, "paste")
            
            # Atualiza status visual (com verificação de null para todos os items)
            status_item = self.table.item(row, 3)
            if status_item:
                status_item.setText("✅")
            
            for col in range(4):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(TableColors.TRANSLATED_ROW)
            
            pasted_count += 1
        
        self.table.blockSignals(False)  # Reativa sinais
        
        # Auto-ajusta altura das linhas após colar
        self._auto_adjust_row_heights()
        
        # Atualiza estatísticas
        self._update_statistics()
        
        self.status_label.setText(f"{pasted_count} tradução(ões) colada(s)")
        app_logger.info(f"Coladas {pasted_count} traduções da área de transferência")
    
    def apply_smart_translations(self):
        """Aplica traduções inteligentes usando padrões"""
        if not self.smart_translator:
            QMessageBox.warning(self, "Aviso", "Conecte a um banco de dados primeiro")
            return
        
        try:
            self.status_label.setText("Aplicando traduções inteligentes...")
            
            # Verifica se há linhas selecionadas
            selected_rows = sorted(set(item.row() for item in self.table.selectedItems()))
            
            if selected_rows:
                # Aplica apenas às linhas selecionadas que não têm tradução
                untranslated = []
                for row in selected_rows:
                    if row < len(self.entries) and not self.entries[row].translated_text:
                        untranslated.append(self.entries[row].original_text)
                
                if not untranslated:
                    QMessageBox.information(
                        self, 
                        "Informação", 
                        "Todas as linhas selecionadas já estão traduzidas!"
                    )
                    return
                
                info_message = f"{len(untranslated)} linha(s) selecionada(s)"
            else:
                # Se nenhuma linha selecionada, aplica a todas não traduzidas
                untranslated = [e.original_text for e in self.entries if not e.translated_text]
                
                if not untranslated:
                    QMessageBox.information(self, "Informação", "Todos os textos já estão traduzidos!")
                    return
                
                info_message = f"todas as {len(untranslated)} linhas não traduzidas"
            
            # Aplica tradução inteligente
            translations = self.smart_translator.auto_translate_batch(untranslated)
            
            # Atualiza entradas
            count = 0
            for entry in self.entries:
                if not entry.translated_text and entry.original_text in translations:
                    entry.translated_text = translations[entry.original_text]
                    count += 1
            
            # Atualiza tabela
            self._populate_table()
            self._update_statistics()
            
            self.status_label.setText(f"Traduções inteligentes aplicadas: {count}")
            QMessageBox.information(
                self, 
                "Sucesso", 
                f"{count} traduções aplicadas automaticamente em {info_message}!\n\n"
                "💡 Dica: Selecione linhas específicas para aplicar tradução apenas a elas."
            )
            
            app_logger.info(f"Traduções inteligentes aplicadas: {count}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar traduções:\n{str(e)}")
            app_logger.error(f"Erro ao aplicar traduções inteligentes: {e}", exc_info=True)
    
    def auto_translate(self):
        """Inicia tradução automática via API"""
        if not self.api_manager.active_api:
            QMessageBox.warning(
                self,
                "API não configurada",
                "Configure uma API de tradução nas configurações antes de usar esta função."
            )
            self.open_settings()
            return
        
        # Verifica se há linhas selecionadas
        selected_rows = sorted(set(item.row() for item in self.table.selectedItems()))
        
        if selected_rows:
            # Traduz apenas as linhas selecionadas que não têm tradução
            untranslated = []
            for row in selected_rows:
                if row < len(self.entries) and not self.entries[row].translated_text:
                    untranslated.append(self.entries[row].original_text)
            
            if not untranslated:
                QMessageBox.information(
                    self, 
                    "Informação", 
                    "Todas as linhas selecionadas já estão traduzidas!"
                )
                return
            
            confirm_message = (
                f"Traduzir {len(untranslated)} linha(s) selecionada(s) usando {self.api_manager.active_api.upper()}?\n\n"
                "Isso pode consumir créditos da API."
            )
        else:
            # Se nenhuma linha selecionada, traduz todas não traduzidas
            untranslated = [e.original_text for e in self.entries if not e.translated_text]
            
            if not untranslated:
                QMessageBox.information(self, "Informação", "Todos os textos já estão traduzidos!")
                return
            
            confirm_message = (
                f"Traduzir TODAS as {len(untranslated)} linhas não traduzidas usando {self.api_manager.active_api.upper()}?\n\n"
                "Isso pode consumir créditos da API.\n\n"
                "💡 Dica: Selecione linhas específicas para traduzir apenas essas."
            )
        
        # Confirma ação
        reply = QMessageBox.question(
            self,
            "Confirmar Tradução Automática",
            confirm_message,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Inicia worker thread
        self.status_label.setText("Traduzindo automaticamente...")
        self.btn_auto_translate.setEnabled(False)
        
        self.worker = TranslationWorker(untranslated, self.api_manager, self.smart_translator)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_auto_translate_finished)
        self.worker.error.connect(self.on_auto_translate_error)
        self.worker.start()
    
    def on_auto_translate_finished(self, translations):
        """Callback quando tradução automática termina"""
        # Atualiza entradas
        count = 0
        for entry in self.entries:
            if not entry.translated_text and entry.original_text in translations:
                entry.translated_text = translations[entry.original_text]
                
                # Adiciona à memória
                if self.translation_memory.is_connected():
                    self.translation_memory.add_translation(
                        entry.original_text,
                        entry.translated_text
                    )
                count += 1
        
        # Atualiza interface
        self._populate_table()
        self._update_statistics()
        
        self.status_label.setText(f"Tradução automática concluída: {count} textos")
        self.progress_bar.setValue(0)
        self.btn_auto_translate.setEnabled(True)
        
        QMessageBox.information(self, "Sucesso", f"{count} textos traduzidos automaticamente!")
        app_logger.info(f"Tradução automática concluída: {count} textos")
    
    def on_auto_translate_error(self, error):
        """Callback quando ocorre erro na tradução automática"""
        self.status_label.setText("Erro na tradução automática")
        self.progress_bar.setValue(0)
        self.btn_auto_translate.setEnabled(True)
        
        QMessageBox.critical(self, "Erro", f"Erro na tradução automática:\n{error}")
        app_logger.error(f"Erro na tradução automática: {error}")
    
    def save_file(self):
        """Salva arquivo traduzido"""
        if not self.file_processor or not self.current_file:
            return
        
        try:
            self.status_label.setText("Salvando arquivo...")
            
            # Cria dicionário de traduções
            translations = {
                entry.original_text: entry.translated_text
                for entry in self.entries
                if entry.translated_text
            }
            
            # Aplica traduções
            translated_content = self.file_processor.apply_translations(translations)
            
            # Salva arquivo (com backup automático)
            if self.file_processor.save_file(self.current_file, translated_content, create_backup=True):
                self.status_label.setText("Arquivo salvo com sucesso!")
                
                # Obtém o caminho da pasta de backups
                file_dir = os.path.dirname(os.path.abspath(self.current_file))
                backup_dir = os.path.join(file_dir, "backups")
                
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    f"Arquivo traduzido salvo com sucesso!\n\n"
                    f"Um backup do original foi criado em:\n{backup_dir}"
                )
                app_logger.log_file_operation("save", self.current_file, True)
            else:
                raise Exception("Falha ao salvar arquivo")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar arquivo:\n{str(e)}")
            app_logger.error(f"Erro ao salvar arquivo: {e}", exc_info=True)
            self.status_label.setText("Erro ao salvar arquivo")
    
    def open_settings(self):
        """Abre diálogo de configurações"""
        dialog = SettingsDialog(self, self.api_manager, self.translation_memory, self.profile_manager)
        dialog.exec()
    
    def _update_statistics(self):
        """Atualiza estatísticas na interface"""
        total = len(self.entries)
        translated = sum(1 for e in self.entries if e.translated_text)
        pending = total - translated
        
        self.stats_label.setText(f"Total: {total} | Traduzidas: {translated} | Pendentes: {pending}")
        
        if total > 0:
            progress = int(translated / total * 100)
            self.progress_bar.setValue(progress)
    
    def _open_profile_manager(self):
        """Abre gerenciador de perfis regex"""
        dialog = RegexProfileManagerDialog(self, self.profile_manager)
        dialog.profile_changed.connect(self._refresh_profiles)
        dialog.exec()
    
    def _refresh_profiles(self):
        """Atualiza lista de perfis no combo"""
        current = self.combo_profile.currentText()
        self.combo_profile.clear()
        self.combo_profile.addItems(self.profile_manager.get_all_profile_names())
        
        # Tenta manter o perfil selecionado
        idx = self.combo_profile.findText(current)
        if idx >= 0:
            self.combo_profile.setCurrentIndex(idx)
    
    def _import_translations(self):
        """Importa traduções de arquivo existente"""
        if not self.entries:
            QMessageBox.warning(self, "Aviso", "Carregue um arquivo primeiro")
            return
        
        dialog = ImportTranslationDialog(self, self.entries, self.translation_memory)
        
        if dialog.exec() == QDialog.Accepted and dialog.imported_translations:
            # Aplica traduções importadas
            count = 0
            for entry in self.entries:
                if not entry.translated_text:
                    # Busca correspondência
                    for original, translation in dialog.imported_translations.items():
                        if entry.original_text == original or entry.original_text in original:
                            entry.translated_text = translation
                            count += 1
                            
                            # Adiciona à memória
                            if self.translation_memory.is_connected():
                                self.translation_memory.add_translation(
                                    entry.original_text,
                                    translation
                                )
                            break
            
            # Atualiza interface
            self._populate_table()
            self._update_statistics()
            
            QMessageBox.information(
                self,
                "Importação Concluída",
                f"{count} traduções importadas com sucesso!"
            )
    
    def _show_shortcuts(self):
        """Mostra diálogo de atalhos de teclado"""
        shortcuts = """
        <h2>⌨️ Atalhos de Teclado</h2>
        
        <h3>Arquivo</h3>
        <table>
        <tr><td><b>Ctrl+O</b></td><td>Importar arquivo</td></tr>
        <tr><td><b>Ctrl+S</b></td><td>Salvar arquivo</td></tr>
        <tr><td><b>Ctrl+D</b></td><td>Abrir banco de dados</td></tr>
        <tr><td><b>Ctrl+Shift+N</b></td><td>Novo banco de dados</td></tr>
        <tr><td><b>Ctrl+Q</b></td><td>Sair</td></tr>
        </table>
        
        <h3>Banco de Dados</h3>
        <table>
        <tr><td><b>Ctrl+B</b></td><td>Visualizar banco de dados</td></tr>
        <tr><td><b>Ctrl+E</b></td><td>Exportar para CSV</td></tr>
        </table>
        
        <h3>Ferramentas</h3>
        <table>
        <tr><td><b>Ctrl+P</b></td><td>Gerenciar perfis regex</td></tr>
        <tr><td><b>Ctrl+I</b></td><td>Importar traduções</td></tr>
        <tr><td><b>Ctrl+,</b></td><td>Configurações</td></tr>
        </table>
        
        <h3>Tradução</h3>
        <table>
        <tr><td><b>F5</b></td><td>Traduzir automaticamente</td></tr>
        <tr><td><b>Ctrl+C</b></td><td>Copiar linhas selecionadas</td></tr>
        <tr><td><b>Ctrl+V</b></td><td>Colar traduções</td></tr>
        </table>
        
        <h3>Ajuda</h3>
        <table>
        <tr><td><b>F1</b></td><td>Mostrar atalhos</td></tr>
        </table>
        """
        
        QMessageBox.information(self, "Atalhos de Teclado", shortcuts)
    
    def _show_about(self):
        """Mostra diálogo Sobre"""
        QMessageBox.about(
            self,
            "Sobre Game Translator",
            "<h2>Game Translator v1.0.0</h2>"
            "<p>Sistema Profissional de Tradução para Jogos e Mods</p>"
            "<p><b>Características:</b></p>"
            "<ul>"
            "<li>Preservação total da estrutura de arquivos</li>"
            "<li>Memória de tradução com SQLite</li>"
            "<li>Tradução inteligente com padrões</li>"
            "<li>Suporte a APIs de tradução</li>"
            "<li>Sistema de segurança integrado</li>"
            "</ul>"
            "<p>Desenvolvido por <b>Manus AI</b></p>"
        )
    
    def _save_window_settings(self):
        """Salva a geometria da janela"""
        try:
            settings = QSettings(SETTINGS_ORG_NAME, SETTINGS_APP_NAME)
            settings.setValue("geometry", self.saveGeometry())
            app_logger.info("Geometria da janela salva")
        except Exception as e:
            app_logger.error(f"Erro ao salvar configurações da janela: {e}")
    
    def _restore_window_settings(self):
        """Restaura a geometria da janela"""
        try:
            settings = QSettings(SETTINGS_ORG_NAME, SETTINGS_APP_NAME)
            
            # Restaura geometria se existir (explicit default None)
            geometry = settings.value("geometry", None)
            if geometry:
                success = self.restoreGeometry(geometry)
                if success:
                    app_logger.info("Geometria da janela restaurada")
                else:
                    app_logger.warning("Falha ao restaurar geometria da janela - usando geometria padrão")
        except Exception as e:
            app_logger.error(f"Erro ao restaurar configurações da janela: {e}")
            # Continua com geometria padrão em caso de erro
    
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        # Verifica se há alterações não salvas
        if self.entries:
            unsaved = sum(1 for e in self.entries if e.translated_text and not e.original_text)
            
            if unsaved > 0:
                reply = QMessageBox.question(
                    self,
                    "Sair",
                    "Há traduções não salvas. Deseja sair mesmo assim?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.No:
                    event.ignore()
                    return
        
        # Salva configurações da janela
        self._save_window_settings()
        
        # Fecha conexão com banco de dados
        if self.translation_memory:
            self.translation_memory.close()
        
        # Para timer de recursos
        self.resource_timer.stop()
        
        app_logger.info("Aplicativo encerrado")
        event.accept()
