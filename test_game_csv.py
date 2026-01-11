#!/usr/bin/env python3
"""
Script de teste para validar o suporte a CSV com formato de jogo
(delimitado por ponto e vírgula com coluna BRASILIAN)
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from file_processor import FileProcessor
from regex_profiles import RegexProfileManager

def test_game_format_extraction():
    """Testa extração de CSV no formato do jogo"""
    print("=" * 70)
    print("TESTE: Extração de CSV no formato de jogo (delimitado por ;)")
    print("=" * 70)
    
    processor = FileProcessor()
    
    # Carrega o arquivo CSV de teste
    if not processor.load_file('test_game_format.csv'):
        print("❌ Erro ao carregar arquivo CSV")
        return False
    
    print(f"✓ Arquivo carregado com sucesso")
    print(f"  - Tipo: {processor.file_type}")
    print(f"  - Encoding: {processor.detected_encoding}")
    
    # Mostra o conteúdo original
    print(f"\n📄 Conteúdo do arquivo:")
    print("-" * 70)
    lines = processor.original_content.split('\n')
    for i, line in enumerate(lines[:7], 1):
        print(f"{i}. {line}")
    print("-" * 70)
    
    # Extrai textos
    entries = processor.extract_texts()
    
    print(f"\n✓ Extração concluída: {len(entries)} entradas encontradas")
    print(f"\n📝 Textos extraídos da coluna BRASILIAN:\n")
    
    # Mostra todas as entradas
    for i, entry in enumerate(entries, 1):
        print(f"{i}. Texto original: '{entry.original_text}'")
        print(f"   {entry.context}")
        print()
    
    # Validações
    expected_texts = [
        "Plano 1",
        "Plano 2", 
        "Construir",
        "Destruir",
        "Madeira",
        "Pedra"
    ]
    
    extracted_texts = [entry.original_text for entry in entries]
    
    print("=" * 70)
    print("VALIDAÇÃO:")
    print("=" * 70)
    
    all_found = True
    for expected in expected_texts:
        if expected in extracted_texts:
            print(f"✅ '{expected}' encontrado")
        else:
            print(f"❌ '{expected}' NÃO encontrado")
            all_found = False
    
    # Verifica se não extraiu textos de outras colunas
    other_language_texts = ["Template 1", "Template 2", "Build", "Destroy", "Wood", "Stone", 
                           "Шаблон 1", "Шаблон 2", "模板-1", "模板-2"]
    
    print(f"\n🔍 Verificando se NÃO extraiu textos de outras colunas:")
    no_other_langs = True
    for other_text in other_language_texts:
        if other_text in extracted_texts:
            print(f"❌ ERRO: '{other_text}' foi extraído (não deveria)")
            no_other_langs = False
    
    if no_other_langs:
        print(f"✅ Nenhum texto de outras colunas foi extraído")
    
    return all_found and no_other_langs

def test_translation_application():
    """Testa aplicação de traduções mantendo estrutura"""
    print("\n" + "=" * 70)
    print("TESTE: Aplicação de traduções mantendo estrutura do CSV")
    print("=" * 70)
    
    processor = FileProcessor()
    
    if not processor.load_file('test_game_format.csv'):
        print("❌ Erro ao carregar arquivo CSV")
        return False
    
    # Extrai textos
    entries = processor.extract_texts()
    
    # Simula traduções
    translations = {
        "Plano 1": "Modelo 1 [TRADUZIDO]",
        "Plano 2": "Modelo 2 [TRADUZIDO]",
        "Construir": "Edificar [TRADUZIDO]",
        "Destruir": "Demolir [TRADUZIDO]",
        "Madeira": "Lenha [TRADUZIDO]",
        "Pedra": "Rocha [TRADUZIDA]"
    }
    
    print(f"\n📝 Aplicando {len(translations)} traduções...\n")
    
    # Aplica traduções
    translated_content = processor.apply_translations(translations)
    
    print("📄 Conteúdo traduzido:")
    print("-" * 70)
    for i, line in enumerate(translated_content.split('\n')[:7], 1):
        print(f"{i}. {line}")
    print("-" * 70)
    
    # Valida que a estrutura foi mantida
    lines = translated_content.split('\n')
    
    # Verifica cabeçalho
    if lines[0].startswith(';ENGLISH;POLISH;RUSSIAN'):
        print("\n✅ Cabeçalho mantido corretamente")
    else:
        print("\n❌ Cabeçalho foi alterado")
        return False
    
    # Verifica se as traduções foram aplicadas
    all_applied = True
    for original, translated in translations.items():
        if translated in translated_content:
            print(f"✅ '{original}' → '{translated}'")
        else:
            print(f"❌ Tradução de '{original}' não foi aplicada")
            all_applied = False
    
    # Verifica se outras colunas não foram afetadas
    if "Template 1" in translated_content and "Шаблон 1" in translated_content:
        print(f"\n✅ Outras colunas (ENGLISH, RUSSIAN, etc.) mantidas intactas")
    else:
        print(f"\n❌ Outras colunas foram afetadas")
        return False
    
    return all_applied

def main():
    """Executa todos os testes"""
    print("\n🧪 TESTANDO SUPORTE A CSV NO FORMATO DE JOGOS\n")
    
    results = []
    
    # Teste 1: Extração
    try:
        results.append(("Extração de coluna BRASILIAN", test_game_format_extraction()))
    except Exception as e:
        print(f"❌ Erro no teste 1: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Extração de coluna BRASILIAN", False))
    
    # Teste 2: Aplicação de traduções
    try:
        results.append(("Aplicação de traduções", test_translation_application()))
    except Exception as e:
        print(f"❌ Erro no teste 2: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Aplicação de traduções", False))
    
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 Todos os testes passaram! O suporte a CSV está funcionando corretamente.")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
