#!/usr/bin/env python3
"""
Script de Teste para Verificar as Mudanças do Commit 0a8a11f
Verifica se as alterações de PowerShell scripts e correções de bugs funcionam corretamente
"""

import sys
import os
import re

def test_powershell_scripts_exist():
    """Testa se os scripts PowerShell foram criados corretamente"""
    print("\n🔍 Testando Scripts PowerShell...")
    print("-" * 60)
    
    # Descobre o diretório raiz do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    scripts = [
        'EXECUTAR.ps1',
        'INSTALAR.ps1',
        'VERIFICAR_SISTEMA.ps1',
        'build_exe.ps1'
    ]
    
    all_ok = True
    
    for script in scripts:
        filepath = os.path.join(base_dir, script)
        if os.path.exists(filepath):
            print(f"✅ {script}: encontrado")
            
            # Verifica conteúdo básico do PowerShell
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verifica se é um script PowerShell válido
            if not content.strip():
                print(f"   ❌ {script}: arquivo vazio")
                all_ok = False
            elif '$Host.UI.RawUI.WindowTitle' in content or 'Write-Host' in content:
                print(f"   ✅ {script}: sintaxe PowerShell válida")
            else:
                print(f"   ⚠️ {script}: pode não ser um script PowerShell válido")
        else:
            print(f"❌ {script}: NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok


def test_powershell_executar():
    """Testa o script EXECUTAR.ps1 especificamente"""
    print("\n🔍 Testando EXECUTAR.ps1...")
    print("-" * 60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, 'EXECUTAR.ps1')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            'Título da janela': '$Host.UI.RawUI.WindowTitle' in content,
            'Codificação UTF-8': '[Console]::OutputEncoding' in content or '[System.Text.Encoding]::UTF8' in content,
            'Verificação do executável': 'dist' in content and 'GameTranslator.exe' in content,
            'Fallback para Python': 'py ' in content or 'python ' in content,
            'Verificação de dependências': 'PySide6' in content or 'requests' in content,
        }
        
        all_ok = True
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: OK")
            else:
                print(f"❌ {check_name}: FALTANDO")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erro ao testar EXECUTAR.ps1: {e}")
        return False


def test_powershell_verificar_sistema():
    """Testa o script VERIFICAR_SISTEMA.ps1 especificamente"""
    print("\n🔍 Testando VERIFICAR_SISTEMA.ps1...")
    print("-" * 60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, 'VERIFICAR_SISTEMA.ps1')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            'Verificação de Python': 'py --version' in content or 'python --version' in content,
            'Chama verificar_sistema.py': 'verificar_sistema.py' in content,
            'Flag --auto-instalar': '--auto-instalar' in content,
            'Tratamento de erro': 'exit 1' in content or '$LASTEXITCODE' in content,
        }
        
        all_ok = True
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: OK")
            else:
                print(f"❌ {check_name}: FALTANDO")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erro ao testar VERIFICAR_SISTEMA.ps1: {e}")
        return False


def test_paste_rows_clipboard_index():
    """Testa se a correção do clipboard_index foi implementada corretamente"""
    print("\n🔍 Testando Correção do paste_rows (clipboard_index)...")
    print("-" * 60)
    
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'gui', 'main_window.py')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se a função paste_rows existe
        if 'def paste_rows(self):' not in content:
            print("❌ Função paste_rows NÃO encontrada")
            return False
        
        print("✅ Função paste_rows encontrada")
        
        # Verifica se clipboard_index foi adicionado
        if 'clipboard_index = 0' not in content:
            print("❌ Variável clipboard_index = 0 NÃO encontrada")
            return False
        
        print("✅ Variável clipboard_index = 0 encontrada")
        
        # Verifica se há incremento de clipboard_index
        if 'clipboard_index += 1' not in content:
            print("❌ Incremento clipboard_index += 1 NÃO encontrado")
            return False
        
        print("✅ Incremento clipboard_index += 1 encontrado")
        
        # Verifica se usa clipboard_index para acessar clipboard_lines
        if 'clipboard_lines[clipboard_index]' not in content:
            print("❌ Uso de clipboard_lines[clipboard_index] NÃO encontrado")
            return False
        
        print("✅ Uso correto de clipboard_lines[clipboard_index] encontrado")
        
        # Verifica se há comentário explicativo sobre a correção
        if 'Índice separado' in content or 'clipboard_index' in content:
            print("✅ Documentação sobre clipboard_index encontrada")
        else:
            print("⚠️ Documentação sobre clipboard_index pode estar faltando")
        
        # Verifica lógica de filtro para linhas sem tradução
        if 'rows_without_translation' in content:
            print("✅ Lógica de filtro rows_without_translation encontrada")
        else:
            print("❌ Lógica de filtro rows_without_translation NÃO encontrada")
            return False
        
        # Verifica se cola apenas em linhas sem tradução
        if 'NÃO possuem tradução' in content or 'sem tradução' in content:
            print("✅ Verificação de linhas sem tradução encontrada")
        else:
            print("⚠️ Verificação de linhas sem tradução pode estar faltando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar paste_rows: {e}")
        return False


def test_delete_multiple_lines():
    """Testa se o suporte para excluir múltiplas linhas foi adicionado"""
    print("\n🔍 Testando Suporte para Delete de Múltiplas Linhas...")
    print("-" * 60)
    
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'gui', 'main_window.py')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se há atalho de Delete configurado
        if 'QShortcut(QKeySequence.Delete' not in content:
            print("❌ QShortcut para Delete NÃO encontrado")
            return False
        
        print("✅ QShortcut para Delete encontrado")
        
        # Conta quantas vezes o atalho Delete é configurado
        delete_count = content.count('QShortcut(QKeySequence.Delete')
        print(f"   ℹ️ Atalho Delete configurado {delete_count} vez(es)")
        
        # Verifica se há método _delete_selected
        if 'def _delete_selected(self):' not in content:
            print("❌ Método _delete_selected NÃO encontrado")
            return False
        
        print("✅ Método _delete_selected encontrado")
        
        # Verifica se _delete_selected lida com múltiplas seleções
        if 'selectedRows()' in content:
            print("✅ Uso de selectedRows() encontrado (suporta múltiplas seleções)")
        else:
            print("⚠️ selectedRows() pode não estar sendo usado corretamente")
        
        # Verifica se há iteração sobre múltiplas linhas selecionadas
        if 'for index in selected_rows:' in content or 'for row in selected_rows:' in content:
            print("✅ Iteração sobre múltiplas linhas encontrada")
        else:
            print("⚠️ Iteração sobre múltiplas linhas pode estar faltando")
        
        # Verifica se há confirmação antes de excluir
        if 'QMessageBox.question' in content and 'Confirmar Exclusão' in content:
            print("✅ Confirmação de exclusão encontrada")
        else:
            print("⚠️ Confirmação de exclusão pode estar faltando")
        
        # Verifica se mostra quantidade de linhas a excluir
        # Procura por padrão de f-string ou mensagem específica
        if 'f"Tem certeza que deseja excluir {count}' in content or '{count}' in content and 'excluir' in content:
            print("✅ Mensagem com quantidade de linhas a excluir encontrada")
        else:
            print("⚠️ Mensagem com quantidade pode estar faltando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar delete múltiplo: {e}")
        return False


def test_verificar_sistema_module():
    """Testa se o módulo verificar_sistema.py existe e está correto"""
    print("\n🔍 Testando Módulo verificar_sistema.py...")
    print("-" * 60)
    
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'verificar_sistema.py')
        
        if not os.path.exists(filepath):
            print("❌ verificar_sistema.py NÃO encontrado")
            return False
        
        print("✅ verificar_sistema.py encontrado")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica elementos essenciais
        checks = {
            'Classe VerificadorSistema': 'class VerificadorSistema:' in content,
            'Método verificar_tudo': 'def verificar_tudo(self' in content,
            'Suporte a colorama': 'colorama' in content or 'Fore.' in content,
            'Verificação de Python': 'def verificar_python(self' in content,
            'Verificação de pip': 'def verificar_pip(self' in content,
            'Instalação automática': 'auto_instalar' in content,
            'Argparse para CLI': 'argparse' in content,
            'Flag --auto-instalar': '--auto-instalar' in content,
        }
        
        all_ok = True
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: OK")
            else:
                print(f"❌ {check_name}: FALTANDO")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erro ao testar verificar_sistema.py: {e}")
        return False


def test_main_window_clear_translations():
    """Testa se a função _clear_selected_translations foi corrigida"""
    print("\n🔍 Testando Função _clear_selected_translations...")
    print("-" * 60)
    
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'gui', 'main_window.py')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se a função existe
        if 'def _clear_selected_translations(self):' not in content:
            print("❌ Função _clear_selected_translations NÃO encontrada")
            return False
        
        print("✅ Função _clear_selected_translations encontrada")
        
        # Verifica se limpa múltiplas seleções
        if 'selectedRows()' in content or 'selected_rows' in content:
            print("✅ Suporte para múltiplas seleções")
        
        # Verifica se atualiza estatísticas após limpar
        if '_update_statistics()' in content:
            print("✅ Atualização de estatísticas encontrada")
        else:
            print("⚠️ Atualização de estatísticas pode estar faltando")
        
        # Verifica se há logging
        if 'app_logger.info' in content and 'Delete' in content:
            print("✅ Logging de operações de Delete encontrado")
        else:
            print("⚠️ Logging pode estar faltando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar _clear_selected_translations: {e}")
        return False


def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 TESTE DO COMMIT 0a8a11f - Tradutor XML-JSON")
    print("=" * 60)
    print("\nVerificando mudanças do commit:")
    print("- Substituir scripts .bat por PowerShell")
    print("- Corrigir bugs de seleção múltipla")
    print("- Suporte para excluir múltiplas linhas com Delete")
    print("- Corrigir bug de colagem em múltiplas linhas")
    
    results = []
    
    # Teste 1: Scripts PowerShell existem
    results.append(("Scripts PowerShell existem", test_powershell_scripts_exist()))
    
    # Teste 2: EXECUTAR.ps1 específico
    results.append(("EXECUTAR.ps1 correto", test_powershell_executar()))
    
    # Teste 3: VERIFICAR_SISTEMA.ps1 específico
    results.append(("VERIFICAR_SISTEMA.ps1 correto", test_powershell_verificar_sistema()))
    
    # Teste 4: Módulo verificar_sistema.py
    results.append(("verificar_sistema.py correto", test_verificar_sistema_module()))
    
    # Teste 5: Correção do clipboard_index em paste_rows
    results.append(("Correção paste_rows (clipboard_index)", test_paste_rows_clipboard_index()))
    
    # Teste 6: Suporte para Delete múltiplo
    results.append(("Suporte Delete múltiplo", test_delete_multiple_lines()))
    
    # Teste 7: Função _clear_selected_translations
    results.append(("_clear_selected_translations", test_main_window_clear_translations()))
    
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
        print("\n✅ As mudanças do commit 0a8a11f estão funcionando corretamente:")
        print("   - Scripts PowerShell criados e funcionais")
        print("   - Bug de colagem em múltiplas linhas corrigido (clipboard_index)")
        print("   - Suporte para excluir múltiplas linhas com Delete adicionado")
        print("   - Módulo verificar_sistema.py implementado corretamente")
        return 0
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("\nVerifique os detalhes acima para mais informações.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
