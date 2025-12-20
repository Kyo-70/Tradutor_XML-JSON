#!/usr/bin/env python3
"""
Script de Teste para Validar as Correções
Testa a sintaxe e imports do código modificado
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from gui.main_window import MainWindow, DatabaseViewerDialog
        print("✅ Imports da MainWindow: OK")
    except ImportError as e:
        print(f"❌ Erro ao importar MainWindow: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def test_paste_rows_logic():
    """Testa a lógica da função paste_rows (análise estática)"""
    print("\n🔍 Testando lógica da função paste_rows...")
    
    try:
        # Lê o arquivo e verifica se a correção está presente
        with open('src/gui/main_window.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se a variável clipboard_index foi adicionada
        if 'clipboard_index = 0' in content:
            print("✅ Variável clipboard_index encontrada")
        else:
            print("❌ Variável clipboard_index NÃO encontrada")
            return False
        
        # Verifica se há incremento do clipboard_index
        if 'clipboard_index += 1' in content:
            print("✅ Incremento de clipboard_index encontrado")
        else:
            print("❌ Incremento de clipboard_index NÃO encontrado")
            return False
        
        # Verifica se usa clipboard_index ao invés de enumerate
        if 'clipboard_lines[clipboard_index]' in content:
            print("✅ Uso correto de clipboard_index encontrado")
        else:
            print("❌ Uso correto de clipboard_index NÃO encontrado")
            return False
        
        print("✅ Lógica da função paste_rows: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar paste_rows: {e}")
        return False

def test_window_geometry_save():
    """Testa se as funções de salvamento de geometria foram adicionadas"""
    print("\n🔍 Testando funções de salvamento de geometria...")
    
    try:
        # Lê o arquivo e verifica se as funções foram adicionadas
        with open('src/gui/main_window.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica função _restore_window_geometry no DatabaseViewerDialog
        if 'def _restore_window_geometry(self):' in content:
            print("✅ Função _restore_window_geometry encontrada")
        else:
            print("❌ Função _restore_window_geometry NÃO encontrada")
            return False
        
        # Verifica função _save_window_geometry no DatabaseViewerDialog
        if 'def _save_window_geometry(self):' in content:
            print("✅ Função _save_window_geometry encontrada")
        else:
            print("❌ Função _save_window_geometry NÃO encontrada")
            return False
        
        # Verifica se closeEvent foi adicionado ao DatabaseViewerDialog
        if 'def closeEvent(self, event):' in content and 'self._save_window_geometry()' in content:
            print("✅ closeEvent com salvamento de geometria encontrado")
        else:
            print("❌ closeEvent com salvamento NÃO encontrado corretamente")
            return False
        
        # Verifica se db_viewer_geometry é usado
        if 'db_viewer_geometry' in content:
            print("✅ Chave de configuração db_viewer_geometry encontrada")
        else:
            print("❌ Chave de configuração db_viewer_geometry NÃO encontrada")
            return False
        
        print("✅ Funções de salvamento de geometria: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar salvamento de geometria: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 TESTE DE CORREÇÕES - Tradutor XML-JSON")
    print("=" * 60)
    
    results = []
    
    # Teste 1: Imports
    results.append(("Imports", test_imports()))
    
    # Teste 2: Lógica paste_rows
    results.append(("Lógica paste_rows", test_paste_rows_logic()))
    
    # Teste 3: Salvamento de geometria
    results.append(("Salvamento de geometria", test_window_geometry_save()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    sys.exit(main())
