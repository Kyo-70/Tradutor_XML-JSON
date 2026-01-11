#!/usr/bin/env python3
"""
Script de Teste para Validar Arquivos .BAT
Verifica sintaxe e padrões dos scripts batch
"""

import os
import re

def test_bat_file(filepath):
    """Testa um arquivo .bat"""
    print(f"\n🔍 Testando: {os.path.basename(filepath)}")
    print("-" * 60)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        warnings = []
        
        # Teste 1: Verifica encoding UTF-8
        if 'chcp 65001' in content:
            print("✅ Encoding UTF-8 configurado")
        else:
            issues.append("❌ Falta configuração de encoding UTF-8 (chcp 65001)")
        
        # Teste 2: Verifica cores ANSI
        if 'VirtualTerminalLevel' in content:
            print("✅ Suporte a cores ANSI habilitado")
        else:
            warnings.append("⚠️ Suporte a cores ANSI não configurado")
        
        # Teste 3: Verifica uso de 'py' ao invés de 'python' ou 'pip'
        # Ignora comentários (::) e strings de mensagens (echo)
        lines = content.split('\n')
        python_command_found = False
        for line in lines:
            # Remove comentários
            if '::' in line:
                line = line.split('::')[0]
            # Verifica se é um comando python (não echo)
            if re.search(r'^\s*python\s', line, re.IGNORECASE) and 'echo' not in line.lower():
                python_command_found = True
                break
        
        if python_command_found:
            issues.append("❌ Usa 'python' ao invés de 'py'")
        else:
            print("✅ Usa comando 'py' correto")
        
        # Teste 4: Verifica uso de 'py -m pip' ao invés de 'pip' direto
        if re.search(r'\bpip\s+install', content) and 'py -m pip' not in content:
            issues.append("❌ Usa 'pip install' direto ao invés de 'py -m pip install'")
        elif 'py -m pip' in content:
            print("✅ Usa 'py -m pip' correto")
        
        # Teste 5: Verifica se tem título
        if 'title ' in content:
            print("✅ Título da janela definido")
        else:
            warnings.append("⚠️ Título da janela não definido")
        
        # Teste 6: Verifica tratamento de erro básico
        if 'errorlevel' in content or 'if errorlevel' in content:
            print("✅ Tratamento de erros presente")
        else:
            warnings.append("⚠️ Sem tratamento de erros")
        
        # Teste 7: Para build_exe.bat, verifica comando PyInstaller completo
        if 'build_exe.bat' in filepath:
            required_params = [
                '--name=',
                '--onefile',
                '--windowed',
                '--hidden-import=PySide6',
                '--add-data'
            ]
            
            missing_params = []
            for param in required_params:
                if param not in content:
                    missing_params.append(param)
            
            if not missing_params:
                print("✅ Comando PyInstaller completo")
            else:
                issues.append(f"❌ Faltam parâmetros PyInstaller: {', '.join(missing_params)}")
        
        # Teste 8: Verifica se limpa builds anteriores (para scripts de build)
        if 'build' in filepath.lower() or 'instalar' in filepath.lower():
            if 'rmdir' in content and 'build' in content:
                print("✅ Limpa diretórios de build anteriores")
            else:
                warnings.append("⚠️ Não limpa builds anteriores")
        
        # Mostra resultados
        print()
        if issues:
            for issue in issues:
                print(issue)
        
        if warnings:
            for warning in warnings:
                print(warning)
        
        if not issues and not warnings:
            print("🎉 Nenhum problema encontrado!")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Erro ao testar arquivo: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DE ARQUIVOS .BAT - Game Translator")
    print("=" * 60)
    
    # Lista de arquivos .bat para testar
    bat_files = [
        'INSTALAR.bat',
        'EXECUTAR.bat',
        'ATUALIZAR.bat',
        'VERIFICAR_SISTEMA.bat',
        'build_exe.bat'
    ]
    
    results = {}
    
    for bat_file in bat_files:
        filepath = os.path.join(os.path.dirname(__file__), bat_file)
        if os.path.exists(filepath):
            results[bat_file] = test_bat_file(filepath)
        else:
            print(f"\n⚠️ Arquivo não encontrado: {bat_file}")
            results[bat_file] = False
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    all_passed = True
    for bat_file, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{bat_file}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
