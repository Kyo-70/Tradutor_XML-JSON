"""
Game Translator - Sistema de Tradução para Jogos e Mods
Autor: Manus AI
Versão: 1.0.3
Descrição: Ferramenta completa para tradução de arquivos JSON/XML preservando estrutura original
"""

import sys
import os

# Adiciona o diretório src ao path para imports funcionarem no executável
if getattr(sys, 'frozen', False):
    # Executando como executável PyInstaller
    BASE_DIR = os.path.dirname(sys.executable)
    SRC_DIR = os.path.join(BASE_DIR, '_internal')
    if os.path.exists(SRC_DIR):
        sys.path.insert(0, SRC_DIR)
    sys.path.insert(0, BASE_DIR)
else:
    # Executando como script Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)

from PySide6.QtWidgets import QApplication

# Import relativo para funcionar tanto como script quanto como executável
try:
    from gui.main_window import MainWindow
except ImportError:
    from main_window import MainWindow

def main():
    """Função principal do aplicativo"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
