#!/usr/bin/env python3
"""
Script de teste para validar o suporte a arquivos CSV
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from file_processor import FileProcessor
from regex_profiles import RegexProfileManager

def test_csv_default_extraction():
    """Testa extração padrão de CSV sem perfil"""
    print("=" * 60)
    print("TESTE 1: Extração padrão de CSV (sem perfil)")
    print("=" * 60)
    
    processor = FileProcessor()
    
    # Carrega o arquivo CSV de teste
    if not processor.load_file('test_data.csv'):
        print("❌ Erro ao carregar arquivo CSV")
        return False
    
    print(f"✓ Arquivo carregado com sucesso")
    print(f"  - Tipo: {processor.file_type}")
    print(f"  - Encoding: {processor.detected_encoding}")
    
    # Extrai textos
    entries = processor.extract_texts()
    
    print(f"\n✓ Extração concluída: {len(entries)} entradas encontradas\n")
    
    # Mostra as primeiras entradas
    for i, entry in enumerate(entries[:10], 1):
        print(f"{i}. Texto: '{entry.original_text}'")
        print(f"   Contexto: {entry.context}")
        print()
    
    return len(entries) > 0

def test_csv_with_profile():
    """Testa extração de CSV com perfil"""
    print("\n" + "=" * 60)
    print("TESTE 2: Extração de CSV com perfil genérico")
    print("=" * 60)
    
    # Carrega perfis
    profile_manager = RegexProfileManager('profiles')
    
    # Verifica se o perfil CSV foi criado
    if "CSV Genérico" not in profile_manager.profiles:
        print("❌ Perfil 'CSV Genérico' não encontrado")
        return False
    
    csv_profile = profile_manager.profiles["CSV Genérico"]
    print(f"✓ Perfil carregado: {csv_profile.name}")
    print(f"  - Descrição: {csv_profile.description}")
    print(f"  - Padrões de captura: {len(csv_profile.capture_patterns)}")
    print(f"  - Padrões de exclusão: {len(csv_profile.exclude_patterns)}")
    
    # Cria processador com perfil
    processor = FileProcessor(regex_profile=csv_profile)
    
    if not processor.load_file('test_data.csv'):
        print("❌ Erro ao carregar arquivo CSV")
        return False
    
    print(f"\n✓ Arquivo carregado com sucesso")
    
    # Extrai textos
    entries = processor.extract_texts()
    
    print(f"✓ Extração concluída: {len(entries)} entradas encontradas\n")
    
    # Mostra as primeiras entradas
    for i, entry in enumerate(entries[:10], 1):
        print(f"{i}. Texto: '{entry.original_text}'")
        print(f"   Contexto: {entry.context}")
        print()
    
    return len(entries) > 0

def test_profile_file_exists():
    """Verifica se o arquivo de perfil CSV foi criado"""
    print("\n" + "=" * 60)
    print("TESTE 3: Verificação do arquivo de perfil")
    print("=" * 60)
    
    profile_path = 'profiles/csv-generico.json'
    
    if not os.path.exists(profile_path):
        print(f"❌ Arquivo de perfil não encontrado: {profile_path}")
        return False
    
    print(f"✓ Arquivo de perfil encontrado: {profile_path}")
    
    # Lê e mostra o conteúdo
    import json
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = json.load(f)
    
    print(f"\nConteúdo do perfil:")
    print(json.dumps(profile_data, indent=2, ensure_ascii=False))
    
    return True

def main():
    """Executa todos os testes"""
    print("\n🧪 INICIANDO TESTES DE SUPORTE A CSV\n")
    
    results = []
    
    # Teste 1: Extração padrão
    try:
        results.append(("Extração padrão", test_csv_default_extraction()))
    except Exception as e:
        print(f"❌ Erro no teste 1: {e}")
        results.append(("Extração padrão", False))
    
    # Teste 2: Extração com perfil
    try:
        results.append(("Extração com perfil", test_csv_with_profile()))
    except Exception as e:
        print(f"❌ Erro no teste 2: {e}")
        results.append(("Extração com perfil", False))
    
    # Teste 3: Arquivo de perfil
    try:
        results.append(("Arquivo de perfil", test_profile_file_exists()))
    except Exception as e:
        print(f"❌ Erro no teste 3: {e}")
        results.append(("Arquivo de perfil", False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 Todos os testes passaram com sucesso!")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
