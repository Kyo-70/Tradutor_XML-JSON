"""
Editor de Perfis Regex
Interface para criar, editar e gerenciar perfis de regex personalizados
"""

import re
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                              QLabel, QLineEdit, QTextEdit, QComboBox,
                              QGroupBox, QListWidget, QListWidgetItem,
                              QMessageBox, QSplitter, QFrame, QTabWidget,
                              QWidget, QTableWidget, QTableWidgetItem,
                              QHeaderView, QInputDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

import sys
import os
from pathlib import Path

# Adiciona path para imports
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    sys.path.insert(0, BASE_DIR)
else:
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from regex_profiles import RegexProfileManager, RegexProfile
except ImportError:
    from src.regex_profiles import RegexProfileManager, RegexProfile


class RegexTestWidget(QWidget):
    """Widget para testar regex em tempo real"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_ui()
    
    def _create_ui(self):
        layout = QVBoxLayout(self)
        
        # Texto de teste
        layout.addWidget(QLabel("Texto de Teste:"))
        self.test_input = QTextEdit()
        self.test_input.setPlaceholderText(
            'Cole aqui um exemplo do arquivo para testar o regex...\n\n'
            'Exemplo JSON:\n'
            '{"name": "Soldier", "description": "A brave warrior"}\n\n'
            'Exemplo XML:\n'
            '<item><name>Sword</name><desc>A sharp blade</desc></item>'
        )
        self.test_input.setMaximumHeight(150)
        layout.addWidget(self.test_input)
        
        # Regex para testar
        regex_layout = QHBoxLayout()
        regex_layout.addWidget(QLabel("Regex:"))
        self.regex_input = QLineEdit()
        self.regex_input.setPlaceholderText('Ex: "([^"]+)"\\s*:\\s*"([^"]+)"')
        regex_layout.addWidget(self.regex_input)
        
        btn_test = QPushButton("🔍 Testar")
        btn_test.clicked.connect(self.test_regex)
        regex_layout.addWidget(btn_test)
        
        layout.addLayout(regex_layout)
        
        # Resultados
        layout.addWidget(QLabel("Resultados:"))
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["#", "Match Completo", "Grupos Capturados"])
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        layout.addWidget(self.results_table)
    
    def test_regex(self):
        """Testa o regex no texto"""
        text = self.test_input.toPlainText()
        pattern = self.regex_input.text()
        
        if not text or not pattern:
            QMessageBox.warning(self, "Aviso", "Digite o texto e o regex para testar")
            return
        
        try:
            regex = re.compile(pattern)
            matches = list(regex.finditer(text))
            
            self.results_table.setRowCount(len(matches))
            
            for i, match in enumerate(matches):
                self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.results_table.setItem(i, 1, QTableWidgetItem(match.group(0)[:50]))
                
                groups = match.groups()
                groups_str = " | ".join(str(g) for g in groups if g)
                self.results_table.setItem(i, 2, QTableWidgetItem(groups_str[:100]))
            
            if not matches:
                QMessageBox.information(self, "Resultado", "Nenhuma correspondência encontrada")
            else:
                QMessageBox.information(self, "Resultado", f"{len(matches)} correspondência(s) encontrada(s)")
                
        except re.error as e:
            QMessageBox.critical(self, "Erro de Regex", f"Regex inválido:\n{str(e)}")
    
    def set_regex(self, pattern: str):
        """Define o regex para teste"""
        self.regex_input.setText(pattern)


class RegexPatternEditor(QWidget):
    """Widget para editar lista de padrões regex"""
    
    patterns_changed = Signal()
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self._create_ui()
    
    def _create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Cabeçalho
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(f"<b>{self.title}</b>"))
        header_layout.addStretch()
        
        btn_add = QPushButton("+ Adicionar")
        btn_add.clicked.connect(self.add_pattern)
        header_layout.addWidget(btn_add)
        
        layout.addLayout(header_layout)
        
        # Lista de padrões
        self.pattern_list = QListWidget()
        self.pattern_list.setAlternatingRowColors(True)
        self.pattern_list.itemDoubleClicked.connect(self.edit_pattern)
        layout.addWidget(self.pattern_list)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        
        btn_edit = QPushButton("✏️ Editar")
        btn_edit.clicked.connect(self.edit_selected)
        btn_layout.addWidget(btn_edit)
        
        btn_remove = QPushButton("🗑️ Remover")
        btn_remove.clicked.connect(self.remove_selected)
        btn_layout.addWidget(btn_remove)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
    
    def add_pattern(self):
        """Adiciona novo padrão"""
        text, ok = QInputDialog.getText(
            self,
            "Adicionar Padrão",
            "Digite o padrão regex:",
            QLineEdit.Normal
        )
        
        if ok and text:
            # Valida regex
            try:
                re.compile(text)
                self.pattern_list.addItem(text)
                self.patterns_changed.emit()
            except re.error as e:
                QMessageBox.critical(self, "Erro", f"Regex inválido:\n{str(e)}")
    
    def edit_pattern(self, item):
        """Edita padrão existente"""
        text, ok = QInputDialog.getText(
            self,
            "Editar Padrão",
            "Edite o padrão regex:",
            QLineEdit.Normal,
            item.text()
        )
        
        if ok and text:
            try:
                re.compile(text)
                item.setText(text)
                self.patterns_changed.emit()
            except re.error as e:
                QMessageBox.critical(self, "Erro", f"Regex inválido:\n{str(e)}")
    
    def edit_selected(self):
        """Edita padrão selecionado"""
        item = self.pattern_list.currentItem()
        if item:
            self.edit_pattern(item)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um padrão para editar")
    
    def remove_selected(self):
        """Remove padrão selecionado"""
        row = self.pattern_list.currentRow()
        if row >= 0:
            self.pattern_list.takeItem(row)
            self.patterns_changed.emit()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um padrão para remover")
    
    def get_patterns(self) -> list:
        """Retorna lista de padrões"""
        return [self.pattern_list.item(i).text() 
                for i in range(self.pattern_list.count())]
    
    def set_patterns(self, patterns: list):
        """Define lista de padrões"""
        self.pattern_list.clear()
        for pattern in patterns:
            self.pattern_list.addItem(pattern)


class ProfileEditorDialog(QDialog):
    """Diálogo para editar um perfil de regex"""
    
    def __init__(self, parent, profile: RegexProfile = None):
        super().__init__(parent)
        
        self.profile = profile
        self.result_profile = None
        
        self.setWindowTitle("Editor de Perfil Regex")
        self.setGeometry(200, 200, 900, 700)
        self.setModal(True)
        
        self._create_ui()
        
        if profile:
            self._load_profile()
    
    def _create_ui(self):
        layout = QVBoxLayout(self)
        
        # Informações básicas
        info_group = QGroupBox("Informações do Perfil")
        info_layout = QVBoxLayout()
        
        # Nome
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nome:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex: Meu Jogo XML")
        name_layout.addWidget(self.name_input)
        info_layout.addLayout(name_layout)
        
        # Descrição
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Descrição:"))
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Ex: Perfil para arquivos XML do meu jogo")
        desc_layout.addWidget(self.desc_input)
        info_layout.addLayout(desc_layout)
        
        # Tipo de arquivo
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Tipo de Arquivo:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["json", "xml"])
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        info_layout.addLayout(type_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        
        # Painel esquerdo - Padrões
        patterns_widget = QWidget()
        patterns_layout = QVBoxLayout(patterns_widget)
        patterns_layout.setContentsMargins(0, 0, 0, 0)
        
        # Padrões de captura
        self.capture_editor = RegexPatternEditor("Padrões de Captura (textos a traduzir)")
        patterns_layout.addWidget(self.capture_editor)
        
        # Padrões de exclusão
        self.exclude_editor = RegexPatternEditor("Padrões de Exclusão (textos a ignorar)")
        patterns_layout.addWidget(self.exclude_editor)
        
        splitter.addWidget(patterns_widget)
        
        # Painel direito - Teste
        test_widget = QWidget()
        test_layout = QVBoxLayout(test_widget)
        test_layout.setContentsMargins(0, 0, 0, 0)
        
        test_group = QGroupBox("Testar Regex")
        test_group_layout = QVBoxLayout()
        self.test_widget = RegexTestWidget()
        test_group_layout.addWidget(self.test_widget)
        test_group.setLayout(test_group_layout)
        test_layout.addWidget(test_group)
        
        splitter.addWidget(test_widget)
        
        splitter.setSizes([450, 450])
        layout.addWidget(splitter)
        
        # Dicas
        tips_label = QLabel(
            "<b>💡 Dicas de Regex:</b><br>"
            "• <code>\"([^\"]+)\"</code> - Captura texto entre aspas<br>"
            "• <code>&lt;tag&gt;([^&lt;]+)&lt;/tag&gt;</code> - Captura conteúdo de tag XML<br>"
            "• <code>text=\"([^\"]+)\"</code> - Captura valor de atributo<br>"
            "• Use <code>()</code> para definir grupos de captura"
        )
        tips_label.setStyleSheet("background-color: #2d4a5a; padding: 10px; border-radius: 5px;")
        layout.addWidget(tips_label)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_test_capture = QPushButton("🔍 Testar Captura")
        btn_test_capture.clicked.connect(self._test_capture_pattern)
        btn_layout.addWidget(btn_test_capture)
        
        btn_layout.addStretch()
        
        btn_save = QPushButton("💾 Salvar Perfil")
        btn_save.clicked.connect(self._save_profile)
        btn_layout.addWidget(btn_save)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        layout.addLayout(btn_layout)
    
    def _load_profile(self):
        """Carrega dados do perfil no formulário"""
        self.name_input.setText(self.profile.name)
        self.desc_input.setText(self.profile.description)
        
        idx = self.type_combo.findText(self.profile.file_type)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)
        
        self.capture_editor.set_patterns(self.profile.capture_patterns)
        self.exclude_editor.set_patterns(self.profile.exclude_patterns)
    
    def _test_capture_pattern(self):
        """Testa o primeiro padrão de captura"""
        patterns = self.capture_editor.get_patterns()
        if patterns:
            self.test_widget.set_regex(patterns[0])
        else:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos um padrão de captura")
    
    def _save_profile(self):
        """Salva o perfil"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Digite um nome para o perfil")
            return
        
        capture_patterns = self.capture_editor.get_patterns()
        if not capture_patterns:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos um padrão de captura")
            return
        
        self.result_profile = RegexProfile(
            name=name,
            description=self.desc_input.text().strip(),
            capture_patterns=capture_patterns,
            exclude_patterns=self.exclude_editor.get_patterns(),
            file_type=self.type_combo.currentText()
        )
        
        self.accept()


class RegexProfileManagerDialog(QDialog):
    """Diálogo principal para gerenciar perfis de regex"""
    
    profile_changed = Signal()
    
    def __init__(self, parent, profile_manager: RegexProfileManager):
        super().__init__(parent)
        
        self.profile_manager = profile_manager
        
        self.setWindowTitle("Gerenciador de Perfis Regex")
        self.setGeometry(150, 150, 800, 500)
        
        self._create_ui()
        self._load_profiles()
    
    def _create_ui(self):
        layout = QVBoxLayout(self)
        
        # Cabeçalho
        header = QLabel("<h2>📋 Gerenciador de Perfis Regex</h2>")
        layout.addWidget(header)
        
        info = QLabel(
            "Os perfis de regex definem como o programa extrai textos dos arquivos.\n"
            "Crie perfis personalizados para diferentes tipos de jogos e formatos."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #888;")
        layout.addWidget(info)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Lista de perfis
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        
        list_layout.addWidget(QLabel("<b>Perfis Disponíveis:</b>"))
        
        self.profile_list = QListWidget()
        self.profile_list.setAlternatingRowColors(True)
        self.profile_list.currentItemChanged.connect(self._on_profile_selected)
        self.profile_list.itemDoubleClicked.connect(self._edit_profile)
        list_layout.addWidget(self.profile_list)
        
        # Botões da lista
        list_btn_layout = QHBoxLayout()
        
        btn_new = QPushButton("+ Novo")
        btn_new.clicked.connect(self._create_profile)
        list_btn_layout.addWidget(btn_new)
        
        btn_edit = QPushButton("✏️ Editar")
        btn_edit.clicked.connect(self._edit_profile)
        list_btn_layout.addWidget(btn_edit)
        
        btn_delete = QPushButton("🗑️ Excluir")
        btn_delete.clicked.connect(self._delete_profile)
        list_btn_layout.addWidget(btn_delete)
        
        list_layout.addLayout(list_btn_layout)
        
        # Botões de importação/exportação
        import_export_layout = QHBoxLayout()
        
        btn_import = QPushButton("📥 Importar")
        btn_import.clicked.connect(self._import_profile)
        import_export_layout.addWidget(btn_import)
        
        btn_export = QPushButton("📤 Exportar")
        btn_export.clicked.connect(self._export_profile)
        import_export_layout.addWidget(btn_export)
        
        list_layout.addLayout(import_export_layout)
        
        splitter.addWidget(list_widget)
        
        # Detalhes do perfil
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 0, 0, 0)
        
        details_layout.addWidget(QLabel("<b>Detalhes do Perfil:</b>"))
        
        self.details_group = QGroupBox()
        details_inner = QVBoxLayout()
        
        self.detail_name = QLabel("Nome: -")
        self.detail_name.setFont(QFont("Arial", 12, QFont.Bold))
        details_inner.addWidget(self.detail_name)
        
        self.detail_desc = QLabel("Descrição: -")
        self.detail_desc.setWordWrap(True)
        details_inner.addWidget(self.detail_desc)
        
        self.detail_type = QLabel("Tipo: -")
        details_inner.addWidget(self.detail_type)
        
        details_inner.addWidget(QLabel("<b>Padrões de Captura:</b>"))
        self.detail_capture = QTextEdit()
        self.detail_capture.setReadOnly(True)
        self.detail_capture.setMaximumHeight(100)
        details_inner.addWidget(self.detail_capture)
        
        details_inner.addWidget(QLabel("<b>Padrões de Exclusão:</b>"))
        self.detail_exclude = QTextEdit()
        self.detail_exclude.setReadOnly(True)
        self.detail_exclude.setMaximumHeight(100)
        details_inner.addWidget(self.detail_exclude)
        
        details_inner.addStretch()
        
        self.details_group.setLayout(details_inner)
        details_layout.addWidget(self.details_group)
        
        splitter.addWidget(details_widget)
        
        splitter.setSizes([300, 500])
        layout.addWidget(splitter)
        
        # Botões principais
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)
        
        layout.addLayout(btn_layout)
    
    def _load_profiles(self):
        """Carrega perfis na lista"""
        self.profile_list.clear()
        
        for name in self.profile_manager.get_all_profile_names():
            item = QListWidgetItem(name)
            self.profile_list.addItem(item)
    
    def _on_profile_selected(self, current, previous):
        """Callback quando perfil é selecionado"""
        if not current:
            return
        
        profile = self.profile_manager.get_profile(current.text())
        if not profile:
            return
        
        self.detail_name.setText(f"Nome: {profile.name}")
        self.detail_desc.setText(f"Descrição: {profile.description or 'Sem descrição'}")
        self.detail_type.setText(f"Tipo de Arquivo: {profile.file_type.upper()}")
        
        self.detail_capture.setPlainText("\n".join(profile.capture_patterns))
        self.detail_exclude.setPlainText("\n".join(profile.exclude_patterns))
    
    def _create_profile(self):
        """Cria novo perfil"""
        dialog = ProfileEditorDialog(self)
        
        if dialog.exec() == QDialog.Accepted and dialog.result_profile:
            self.profile_manager.save_profile(dialog.result_profile)
            self._load_profiles()
            self.profile_changed.emit()
            QMessageBox.information(self, "Sucesso", f"Perfil '{dialog.result_profile.name}' criado!")
    
    def _edit_profile(self):
        """Edita perfil selecionado"""
        item = self.profile_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para editar")
            return
        
        profile = self.profile_manager.get_profile(item.text())
        if not profile:
            return
        
        dialog = ProfileEditorDialog(self, profile)
        
        if dialog.exec() == QDialog.Accepted and dialog.result_profile:
            # Remove perfil antigo se o nome mudou
            if profile.name != dialog.result_profile.name:
                self.profile_manager.delete_profile(profile.name)
            
            self.profile_manager.save_profile(dialog.result_profile)
            self._load_profiles()
            self.profile_changed.emit()
            QMessageBox.information(self, "Sucesso", f"Perfil '{dialog.result_profile.name}' atualizado!")
    
    def _delete_profile(self):
        """Exclui perfil selecionado"""
        item = self.profile_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para excluir")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir o perfil '{item.text()}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.profile_manager.delete_profile(item.text())
            self._load_profiles()
            self.profile_changed.emit()
    
    def _import_profile(self):
        """Importa perfil de arquivo externo"""
        from PySide6.QtWidgets import QFileDialog
        
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Importar Perfil",
            "",
            "Perfil de Regex (*.json)"
        )
        
        if filepath:
            profile = self.profile_manager.import_profile(filepath)
            if profile:
                self._load_profiles()
                self.profile_changed.emit()
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Perfil '{profile.name}' importado com sucesso!"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Falha ao importar perfil. Verifique se o arquivo é válido."
                )
    
    def _export_profile(self):
        """Exporta perfil selecionado para arquivo"""
        from PySide6.QtWidgets import QFileDialog
        
        item = self.profile_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para exportar")
            return
        
        profile_name = item.text()
        
        # Sugere nome de arquivo baseado no perfil
        try:
            from regex_profiles import slugify
        except ImportError:
            from src.regex_profiles import slugify
        
        suggested_name = slugify(profile_name) + ".json"
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Perfil",
            suggested_name,
            "Perfil de Regex (*.json)"
        )
        
        if filepath:
            if self.profile_manager.export_profile(profile_name, filepath):
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Perfil '{profile_name}' exportado com sucesso!"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Falha ao exportar perfil."
                )


class ImportTranslationDialog(QDialog):
    """Diálogo para importar traduções de arquivo existente"""
    
    def __init__(self, parent, current_entries: list, translation_memory):
        super().__init__(parent)
        
        self.current_entries = current_entries
        self.translation_memory = translation_memory
        self.imported_translations = {}
        
        self.setWindowTitle("Importar Traduções Existentes")
        self.setGeometry(200, 200, 800, 600)
        self.setModal(True)
        
        self._create_ui()
    
    def _create_ui(self):
        layout = QVBoxLayout(self)
        
        # Cabeçalho
        header = QLabel("<h2>📥 Importar Traduções de Arquivo Existente</h2>")
        layout.addWidget(header)
        
        info = QLabel(
            "Selecione um arquivo já traduzido para importar as traduções.\n"
            "O programa irá comparar os textos e aplicar as traduções correspondentes."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #888;")
        layout.addWidget(info)
        
        # Seleção de arquivo
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Arquivo traduzido:"))
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Selecione um arquivo JSON ou XML traduzido...")
        file_layout.addWidget(self.file_input)
        
        btn_browse = QPushButton("📁 Procurar")
        btn_browse.clicked.connect(self._browse_file)
        file_layout.addWidget(btn_browse)
        
        layout.addLayout(file_layout)
        
        # Botão analisar
        btn_analyze = QPushButton("🔍 Analisar Arquivo")
        btn_analyze.clicked.connect(self._analyze_file)
        layout.addWidget(btn_analyze)
        
        # Tabela de correspondências
        layout.addWidget(QLabel("<b>Correspondências Encontradas:</b>"))
        
        self.match_table = QTableWidget()
        self.match_table.setColumnCount(4)
        self.match_table.setHorizontalHeaderLabels([
            "✓", "Texto Original", "Tradução Encontrada", "Similaridade"
        ])
        header = self.match_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.match_table.setAlternatingRowColors(True)
        layout.addWidget(self.match_table)
        
        # Estatísticas
        self.stats_label = QLabel("Selecione um arquivo para analisar")
        self.stats_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.stats_label)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_select_all = QPushButton("✓ Selecionar Todos")
        btn_select_all.clicked.connect(self._select_all)
        btn_layout.addWidget(btn_select_all)
        
        btn_deselect_all = QPushButton("✗ Desmarcar Todos")
        btn_deselect_all.clicked.connect(self._deselect_all)
        btn_layout.addWidget(btn_deselect_all)
        
        btn_layout.addStretch()
        
        btn_import = QPushButton("📥 Importar Selecionados")
        btn_import.clicked.connect(self._import_selected)
        btn_layout.addWidget(btn_import)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        layout.addLayout(btn_layout)
    
    def _browse_file(self):
        """Seleciona arquivo para importar"""
        from PySide6.QtWidgets import QFileDialog
        
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo Traduzido",
            "",
            "Arquivos Suportados (*.json *.xml *.csv);;Arquivos JSON (*.json);;Arquivos XML (*.xml);;Arquivos CSV (*.csv)"
        )
        
        if filepath:
            self.file_input.setText(filepath)
    
    def _analyze_file(self):
        """Analisa arquivo e encontra correspondências"""
        import json
        import xml.etree.ElementTree as ET
        
        filepath = self.file_input.text().strip()
        if not filepath:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo primeiro")
            return
        
        try:
            # Lê arquivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrai textos do arquivo importado
            imported_texts = set()
            
            if filepath.endswith('.json'):
                self._extract_json_texts(json.loads(content), imported_texts)
            elif filepath.endswith('.xml'):
                root = ET.fromstring(content)
                self._extract_xml_texts(root, imported_texts)
            elif filepath.endswith('.csv'):
                self._extract_csv_texts(content, imported_texts)
            
            # Encontra correspondências
            self.match_table.setRowCount(0)
            matches = []
            
            for entry in self.current_entries:
                if entry.translated_text:
                    continue  # Já traduzido
                
                original = entry.original_text
                
                # Busca correspondência exata ou similar
                for imported in imported_texts:
                    similarity = self._calculate_similarity(original, imported)
                    if similarity > 0.8:  # 80% de similaridade
                        matches.append((original, imported, similarity))
                        break
            
            # Popula tabela
            self.match_table.setRowCount(len(matches))
            
            for i, (original, translation, similarity) in enumerate(matches):
                # Checkbox
                from PySide6.QtWidgets import QCheckBox
                checkbox = QCheckBox()
                checkbox.setChecked(True)
                self.match_table.setCellWidget(i, 0, checkbox)
                
                self.match_table.setItem(i, 1, QTableWidgetItem(original[:80]))
                self.match_table.setItem(i, 2, QTableWidgetItem(translation[:80]))
                self.match_table.setItem(i, 3, QTableWidgetItem(f"{similarity*100:.0f}%"))
            
            self.stats_label.setText(
                f"✅ {len(matches)} correspondências encontradas de {len(self.current_entries)} textos"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao analisar arquivo:\n{str(e)}")
    
    def _extract_json_texts(self, obj, texts: set, path=""):
        """Extrai textos de objeto JSON recursivamente"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                self._extract_json_texts(value, texts, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._extract_json_texts(item, texts, f"{path}[{i}]")
        elif isinstance(obj, str) and len(obj) > 1:
            texts.add(obj)
    
    def _extract_xml_texts(self, element, texts: set):
        """Extrai textos de elemento XML recursivamente"""
        if element.text and element.text.strip():
            texts.add(element.text.strip())
        
        for attr_value in element.attrib.values():
            if attr_value and len(attr_value) > 1:
                texts.add(attr_value)
        
        for child in element:
            self._extract_xml_texts(child, texts)
    
    def _extract_csv_texts(self, content: str, texts: set):
        """Extrai textos de arquivo CSV"""
        import csv
        from io import StringIO
        
        try:
            # Detecta delimitador
            delimiter = ';' if ';' in content.split('\n')[0] else ','
            
            csv_file = StringIO(content)
            reader = csv.reader(csv_file, delimiter=delimiter)
            
            # Pula cabeçalho
            try:
                next(reader)
            except StopIteration:
                return
            
            # Extrai todos os valores das células
            for row in reader:
                for cell in row:
                    if cell and cell.strip() and len(cell.strip()) > 1:
                        texts.add(cell.strip())
        except Exception as e:
            print(f"Erro ao extrair textos do CSV: {e}")
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """Calcula similaridade entre duas strings"""
        if s1 == s2:
            return 1.0
        
        # Similaridade simples baseada em caracteres comuns
        s1_lower = s1.lower()
        s2_lower = s2.lower()
        
        if s1_lower == s2_lower:
            return 0.95
        
        # Verifica se um contém o outro
        if s1_lower in s2_lower or s2_lower in s1_lower:
            return 0.85
        
        # Calcula Jaccard similarity
        set1 = set(s1_lower.split())
        set2 = set(s2_lower.split())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def _select_all(self):
        """Seleciona todas as correspondências"""
        for i in range(self.match_table.rowCount()):
            checkbox = self.match_table.cellWidget(i, 0)
            if checkbox:
                checkbox.setChecked(True)
    
    def _deselect_all(self):
        """Desmarca todas as correspondências"""
        for i in range(self.match_table.rowCount()):
            checkbox = self.match_table.cellWidget(i, 0)
            if checkbox:
                checkbox.setChecked(False)
    
    def _import_selected(self):
        """Importa traduções selecionadas"""
        count = 0
        
        for i in range(self.match_table.rowCount()):
            checkbox = self.match_table.cellWidget(i, 0)
            if checkbox and checkbox.isChecked():
                original = self.match_table.item(i, 1).text()
                translation = self.match_table.item(i, 2).text()
                self.imported_translations[original] = translation
                count += 1
        
        if count > 0:
            QMessageBox.information(
                self,
                "Sucesso",
                f"{count} traduções serão importadas!"
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Aviso", "Nenhuma tradução selecionada")
