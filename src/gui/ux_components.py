"""
Módulo de Componentes de UX/UI
Componentes reutilizáveis para melhorar a experiência do usuário

Componentes incluídos:
- ToastNotification: Notificações temporárias estilo toast
- ThemeManager: Gerenciador de temas (claro/escuro)
- KeyboardShortcuts: Gerenciador de atalhos de teclado
- DragDropMixin: Mixin para suporte a arrastar e soltar
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsOpacityEffect, QApplication, QMainWindow
)
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    Signal, QPoint, QMimeData
)
from PySide6.QtGui import (
    QColor, QPalette, QFont, QKeySequence, QShortcut,
    QDragEnterEvent, QDropEvent
)
from typing import Optional, Callable, Dict, List
from enum import Enum


# ============================================================================
# TOAST NOTIFICATIONS
# ============================================================================

class ToastType(Enum):
    """Tipos de notificação toast"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class ToastNotification(QWidget):
    """
    Widget de notificação temporária estilo toast.

    Aparece no canto da tela e desaparece automaticamente.
    """

    # Cores para cada tipo de toast
    COLORS = {
        ToastType.INFO: {"bg": "#2196F3", "text": "#FFFFFF"},
        ToastType.SUCCESS: {"bg": "#4CAF50", "text": "#FFFFFF"},
        ToastType.WARNING: {"bg": "#FF9800", "text": "#000000"},
        ToastType.ERROR: {"bg": "#F44336", "text": "#FFFFFF"},
    }

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self._setup_ui()
        self._animation = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._fade_out)

    def _setup_ui(self):
        """Configura a interface do toast"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(24, 24)
        layout.addWidget(self._icon_label)

        self._message_label = QLabel()
        self._message_label.setWordWrap(True)
        self._message_label.setMaximumWidth(350)
        font = QFont()
        font.setPointSize(10)
        self._message_label.setFont(font)
        layout.addWidget(self._message_label)

        self._close_btn = QPushButton("×")
        self._close_btn.setFixedSize(24, 24)
        self._close_btn.setFlat(True)
        self._close_btn.clicked.connect(self.hide)
        self._close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 12px;
            }
        """)
        layout.addWidget(self._close_btn)

    def show_toast(self, message: str, toast_type: ToastType = ToastType.INFO,
                   duration: int = 3000):
        """
        Mostra uma notificação toast.

        Args:
            message: Mensagem a ser exibida
            toast_type: Tipo de notificação (INFO, SUCCESS, WARNING, ERROR)
            duration: Duração em milissegundos (0 = permanente)
        """
        colors = self.COLORS.get(toast_type, self.COLORS[ToastType.INFO])

        # Ícones para cada tipo
        icons = {
            ToastType.INFO: "ℹ️",
            ToastType.SUCCESS: "✅",
            ToastType.WARNING: "⚠️",
            ToastType.ERROR: "❌",
        }

        self._icon_label.setText(icons.get(toast_type, "ℹ️"))
        self._message_label.setText(message)

        # Aplica estilo
        self.setStyleSheet(f"""
            ToastNotification {{
                background-color: {colors['bg']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {colors['text']};
            }}
            QPushButton {{
                color: {colors['text']};
            }}
        """)

        # Posiciona no canto inferior direito
        self._position_toast()

        # Mostra com animação de fade in
        self.setWindowOpacity(0)
        self.show()
        self._fade_in()

        # Configura timer para esconder
        if duration > 0:
            self._timer.start(duration)

    def _position_toast(self):
        """Posiciona o toast no canto inferior direito da tela"""
        self.adjustSize()

        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.right() - self.width() - 20
            y = parent_rect.bottom() - self.height() - 20
            self.move(self.parent().mapToGlobal(QPoint(
                parent_rect.width() - self.width() - 20,
                parent_rect.height() - self.height() - 20
            )))
        else:
            screen = QApplication.primaryScreen().geometry()
            x = screen.right() - self.width() - 20
            y = screen.bottom() - self.height() - 60
            self.move(x, y)

    def _fade_in(self):
        """Animação de fade in"""
        self._animation = QPropertyAnimation(self, b"windowOpacity")
        self._animation.setDuration(200)
        self._animation.setStartValue(0)
        self._animation.setEndValue(1)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.start()

    def _fade_out(self):
        """Animação de fade out"""
        self._timer.stop()
        self._animation = QPropertyAnimation(self, b"windowOpacity")
        self._animation.setDuration(200)
        self._animation.setStartValue(1)
        self._animation.setEndValue(0)
        self._animation.setEasingCurve(QEasingCurve.InCubic)
        self._animation.finished.connect(self.hide)
        self._animation.start()


class ToastManager:
    """
    Gerenciador de toasts para a aplicação.

    Uso:
        toast = ToastManager(main_window)
        toast.info("Arquivo carregado com sucesso")
        toast.success("Tradução concluída!")
        toast.warning("Limite de API próximo")
        toast.error("Erro ao salvar arquivo")
    """

    def __init__(self, parent: QWidget):
        self._parent = parent
        self._toast = ToastNotification(parent)

    def info(self, message: str, duration: int = 3000):
        """Mostra toast informativo"""
        self._toast.show_toast(message, ToastType.INFO, duration)

    def success(self, message: str, duration: int = 3000):
        """Mostra toast de sucesso"""
        self._toast.show_toast(message, ToastType.SUCCESS, duration)

    def warning(self, message: str, duration: int = 4000):
        """Mostra toast de aviso"""
        self._toast.show_toast(message, ToastType.WARNING, duration)

    def error(self, message: str, duration: int = 5000):
        """Mostra toast de erro"""
        self._toast.show_toast(message, ToastType.ERROR, duration)


# ============================================================================
# THEME MANAGER
# ============================================================================

class ThemeType(Enum):
    """Tipos de tema disponíveis"""
    DARK = "dark"
    LIGHT = "light"


class ThemeManager:
    """
    Gerenciador de temas para a aplicação.

    Suporta tema claro e escuro com troca dinâmica.
    Estilo Bannerlord - tema escuro com acentos laranja/dourado.
    """

    # Paleta de cores para tema escuro (Bannerlord Style)
    DARK_THEME = {
        "window": "#0d0d0d",
        "window_text": "#e8a624",
        "base": "#141414",
        "alternate_base": "#1a1a1a",
        "text": "#e8a624",
        "button": "#1a1a1a",
        "button_text": "#e8a624",
        "highlight": "#e8a624",
        "highlight_text": "#0d0d0d",
        "link": "#ffc947",
        "placeholder": "#666666",
        "accent": "#e8a624",
        "accent_hover": "#ffc947",
        "border": "#3a3a3a",
        "success": "#4ecdc4",
        "warning": "#ffa500",
        "error": "#ff6b6b",
    }

    # Paleta de cores para tema claro
    LIGHT_THEME = {
        "window": "#f0f0f0",
        "window_text": "#000000",
        "base": "#ffffff",
        "alternate_base": "#f5f5f5",
        "text": "#000000",
        "button": "#e1e1e1",
        "button_text": "#000000",
        "highlight": "#e8a624",
        "highlight_text": "#ffffff",
        "link": "#b8860b",
        "placeholder": "#808080",
        "accent": "#e8a624",
        "accent_hover": "#ffc947",
        "border": "#cccccc",
        "success": "#4ecdc4",
        "warning": "#ffa500",
        "error": "#ff6b6b",
    }

    def __init__(self, app: QApplication):
        self._app = app
        self._current_theme = ThemeType.DARK

    def get_current_theme(self) -> ThemeType:
        """Retorna o tema atual"""
        return self._current_theme

    def set_theme(self, theme: ThemeType):
        """
        Define o tema da aplicação.

        Args:
            theme: Tema a ser aplicado (DARK ou LIGHT)
        """
        self._current_theme = theme
        colors = self.DARK_THEME if theme == ThemeType.DARK else self.LIGHT_THEME

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(colors["window"]))
        palette.setColor(QPalette.WindowText, QColor(colors["window_text"]))
        palette.setColor(QPalette.Base, QColor(colors["base"]))
        palette.setColor(QPalette.AlternateBase, QColor(colors["alternate_base"]))
        palette.setColor(QPalette.Text, QColor(colors["text"]))
        palette.setColor(QPalette.Button, QColor(colors["button"]))
        palette.setColor(QPalette.ButtonText, QColor(colors["button_text"]))
        palette.setColor(QPalette.Highlight, QColor(colors["highlight"]))
        palette.setColor(QPalette.HighlightedText, QColor(colors["highlight_text"]))
        palette.setColor(QPalette.Link, QColor(colors["link"]))
        palette.setColor(QPalette.PlaceholderText, QColor(colors["placeholder"]))

        # Cores para estados desabilitados
        disabled_text = QColor(colors["placeholder"])
        palette.setColor(QPalette.Disabled, QPalette.Text, disabled_text)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, disabled_text)

        self._app.setPalette(palette)

        # Estilos adicionais baseados no tema
        if theme == ThemeType.DARK:
            self._app.setStyleSheet(self._get_dark_stylesheet())
        else:
            self._app.setStyleSheet(self._get_light_stylesheet())

    def toggle_theme(self) -> ThemeType:
        """
        Alterna entre tema claro e escuro.

        Returns:
            Novo tema aplicado
        """
        new_theme = ThemeType.LIGHT if self._current_theme == ThemeType.DARK else ThemeType.DARK
        self.set_theme(new_theme)
        return new_theme

    def _get_dark_stylesheet(self) -> str:
        """Retorna stylesheet para tema escuro (Bannerlord Style)"""
        return """
            QToolTip {
                background-color: #1a1a1a;
                color: #e8a624;
                border: 1px solid #e8a624;
                padding: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QScrollBar:vertical {
                background-color: #0d0d0d;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #3a3a3a;
                min-height: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #e8a624;
            }
            QScrollBar:horizontal {
                background-color: #0d0d0d;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #3a3a3a;
                min-width: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #e8a624;
            }
            QTableWidget {
                gridline-color: #2a2a2a;
                background-color: #141414;
                alternate-background-color: #1a1a1a;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #e8a624;
                padding: 8px;
                border: none;
                border-right: 1px solid #2a2a2a;
                border-bottom: 1px solid #2a2a2a;
                font-weight: bold;
            }
            QGroupBox {
                border: 1px solid #e8a624;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 12px;
                color: #e8a624;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                color: #e8a624;
            }
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 6px;
                background-color: #1a1a1a;
                color: #e8a624;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border-color: #e8a624;
            }
            QPushButton {
                background-color: transparent;
                color: #e8a624;
                border: 1px solid #e8a624;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 80px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e8a624;
                color: #0d0d0d;
            }
            QPushButton:pressed {
                background-color: #ffc947;
                color: #0d0d0d;
            }
            QPushButton:disabled {
                background-color: transparent;
                border-color: #3a3a3a;
                color: #666666;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #1a1a1a;
                color: #e8a624;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #3a3a3a;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #e8a624;
                color: #0d0d0d;
            }
            QTabBar::tab:hover:!selected {
                background-color: #2a2a2a;
            }
        """

    def _get_light_stylesheet(self) -> str:
        """Retorna stylesheet para tema claro"""
        return """
            QToolTip {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 4px;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                min-height: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar:horizontal {
                background-color: #f0f0f0;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #c0c0c0;
                min-width: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
            }
            QHeaderView::section {
                background-color: #e8e8e8;
                padding: 6px;
                border: none;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QGroupBox {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 4px;
                background-color: #ffffff;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border-color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #888888;
            }
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e8e8e8;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #d8d8d8;
            }
        """


# ============================================================================
# KEYBOARD SHORTCUTS MANAGER
# ============================================================================

class KeyboardShortcutsManager:
    """
    Gerenciador de atalhos de teclado.

    Centraliza a definição e gerenciamento de todos os atalhos.
    """

    # Atalhos padrão
    DEFAULT_SHORTCUTS = {
        "open_file": "Ctrl+O",
        "save_file": "Ctrl+S",
        "translate_selected": "Ctrl+T",
        "translate_all": "Ctrl+Shift+T",
        "search": "Ctrl+F",
        "refresh": "F5",
        "undo": "Ctrl+Z",
        "redo": "Ctrl+Y",
        "copy": "Ctrl+C",
        "paste": "Ctrl+V",
        "select_all": "Ctrl+A",
        "toggle_theme": "Ctrl+Shift+D",
        "open_database": "Ctrl+D",
        "export": "Ctrl+E",
        "import": "Ctrl+I",
        "settings": "Ctrl+,",
        "help": "F1",
        "quit": "Ctrl+Q",
    }

    def __init__(self, parent: QWidget):
        self._parent = parent
        self._shortcuts: Dict[str, QShortcut] = {}
        self._callbacks: Dict[str, Callable] = {}

    def register(self, name: str, callback: Callable, key_sequence: str = None):
        """
        Registra um atalho de teclado.

        Args:
            name: Nome do atalho (ex: "save_file")
            callback: Função a ser chamada quando o atalho é ativado
            key_sequence: Sequência de teclas (None = usa padrão)
        """
        if key_sequence is None:
            key_sequence = self.DEFAULT_SHORTCUTS.get(name)

        if not key_sequence:
            return

        # Remove atalho anterior se existir
        if name in self._shortcuts:
            self._shortcuts[name].deleteLater()

        shortcut = QShortcut(QKeySequence(key_sequence), self._parent)
        shortcut.activated.connect(callback)
        self._shortcuts[name] = shortcut
        self._callbacks[name] = callback

    def unregister(self, name: str):
        """Remove um atalho de teclado"""
        if name in self._shortcuts:
            self._shortcuts[name].deleteLater()
            del self._shortcuts[name]
            del self._callbacks[name]

    def get_shortcut_text(self, name: str) -> str:
        """Retorna o texto do atalho para exibição"""
        if name in self._shortcuts:
            return self._shortcuts[name].key().toString()
        return self.DEFAULT_SHORTCUTS.get(name, "")

    def get_all_shortcuts(self) -> Dict[str, str]:
        """Retorna todos os atalhos registrados"""
        return {name: shortcut.key().toString()
                for name, shortcut in self._shortcuts.items()}


# ============================================================================
# DRAG AND DROP SUPPORT
# ============================================================================

class DragDropHandler:
    """
    Handler para suporte a arrastar e soltar arquivos.

    Uso:
        handler = DragDropHandler(widget)
        handler.file_dropped.connect(self.on_file_dropped)
        handler.enable()
    """

    def __init__(self, widget: QWidget):
        self._widget = widget
        self._enabled = False
        self._accepted_extensions: List[str] = ['.json', '.xml', '.db', '.csv']
        self._file_dropped_callback: Optional[Callable] = None

    def set_accepted_extensions(self, extensions: List[str]):
        """Define as extensões de arquivo aceitas"""
        self._accepted_extensions = [ext.lower() for ext in extensions]

    def set_callback(self, callback: Callable[[str], None]):
        """Define o callback para quando um arquivo é solto"""
        self._file_dropped_callback = callback

    def enable(self):
        """Habilita drag and drop no widget"""
        self._widget.setAcceptDrops(True)
        self._enabled = True

    def disable(self):
        """Desabilita drag and drop no widget"""
        self._widget.setAcceptDrops(False)
        self._enabled = False

    def handle_drag_enter(self, event: QDragEnterEvent) -> bool:
        """
        Processa evento de entrada de drag.

        Retorna True se o evento foi aceito.
        """
        if not self._enabled:
            return False

        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
                ext = '.' + filepath.split('.')[-1].lower() if '.' in filepath else ''
                if ext in self._accepted_extensions:
                    event.acceptProposedAction()
                    return True

        return False

    def handle_drop(self, event: QDropEvent) -> Optional[str]:
        """
        Processa evento de drop.

        Retorna o caminho do arquivo solto ou None.
        """
        if not self._enabled:
            return None

        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
                ext = '.' + filepath.split('.')[-1].lower() if '.' in filepath else ''
                if ext in self._accepted_extensions:
                    event.acceptProposedAction()
                    if self._file_dropped_callback:
                        self._file_dropped_callback(filepath)
                    return filepath

        return None
