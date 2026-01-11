#!/usr/bin/env python3
"""
Teste do novo comportamento CSV:
- Extrai textos da coluna ENGLISH
- Insere traduções na coluna BRASILIAN
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from file_processor import FileProcessor

def test_new_csv_behavior():
    """Testa o novo comportamento de extração e inserção"""
    print("=" * 70)
    print("TESTE: Novo Comportamento CSV")
    print("Extrai ENGLISH → Insere tradução em BRASILIAN")
    print("=" * 70)
    
    processor = FileProcessor()
    
    # Carrega o arquivo CSV de teste (com coluna BRASILIAN vazia)
    if not processor.load_file('test_empty_brasilian.csv'):
        print("❌ Erro ao carregar arquivo CSV")
        return False
    
    print(f"\n✓ Arquivo carregado com sucesso")
    print(f"  - Tipo: {processor.file_type}")
    
    # Mostra o conteúdo original
    print(f"\n📄 Conteúdo ORIGINAL:")
    print("-" * 70)
    lines = processor.original_content.split('\n')
    for i, line in enumerate(lines[:7], 1):
        print(f"{i}. {line}")
    print("-" * 70)
    
    # Extrai textos
    entries = processor.extract_texts()
    
    print(f"\n✓ Extração concluída: {len(entries)} entradas encontradas")
    print(f"\n📝 Textos extraídos (da coluna ENGLISH):\n")
    
    # Mostra todas as entradas
    for i, entry in enumerate(entries, 1):
        print(f"{i}. Original (ENGLISH): '{entry.original_text}'")
        print(f"   {entry.context}")
        if hasattr(entry, 'csv_info') and entry.csv_info:
            print(f"   Coluna BRASILIAN: posição {entry.csv_info['brasilian_column']}")
        print()
    
    # Validações
    expected_english_texts = [
        "Template 1",
        "Template 2",
        "Build",
        "Destroy",
        "Wood",
        "Stone"
    ]
    
    extracted_texts = [entry.original_text for entry in entries]
    
    print("=" * 70)
    print("VALIDAÇÃO 1: Textos extraídos da coluna ENGLISH")
    print("=" * 70)
    
    all_found = True
    for expected in expected_english_texts:
        if expected in extracted_texts:
            print(f"✅ '{expected}' encontrado")
        else:
            print(f"❌ '{expected}' NÃO encontrado")
            all_found = False
    
    if not all_found:
        return False
    
    # Teste de aplicação de traduções
    print("\n" + "=" * 70)
    print("TESTE 2: Aplicação de traduções na coluna BRASILIAN")
    print("=" * 70)
    
    # Simula traduções do inglês para português
    translations = {
        "Template 1": "Modelo 1 [TRADUZIDO]",
        "Template 2": "Modelo 2 [TRADUZIDO]",
        "Build": "Construir [TRADUZIDO]",
        "Destroy": "Destruir [TRADUZIDO]",
        "Wood": "Madeira [TRADUZIDA]",
        "Stone": "Pedra [TRADUZIDA]"
    }
    
    print(f"\n📝 Aplicando {len(translations)} traduções...\n")
    
    # Aplica traduções
    translated_content = processor.apply_translations(translations)
    
    print("📄 Conteúdo TRADUZIDO:")
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
    
    # Verifica se as traduções foram aplicadas NA COLUNA BRASILIAN
    print("\n" + "=" * 70)
    print("VALIDAÇÃO 2: Traduções inseridas na coluna BRASILIAN")
    print("=" * 70)
    
    all_applied = True
    for original_english, translated_portuguese in translations.items():
        if translated_portuguese in translated_content:
            print(f"✅ '{original_english}' → '{translated_portuguese}' (inserido em BRASILIAN)")
        else:
            print(f"❌ Tradução de '{original_english}' não foi aplicada")
            all_applied = False
    
    # Verifica se a coluna ENGLISH ainda tem os textos originais
    print("\n" + "=" * 70)
    print("VALIDAÇÃO 3: Coluna ENGLISH mantida intacta")
    print("=" * 70)
    
    english_intact = True
    for english_text in expected_english_texts:
        if english_text in translated_content:
            print(f"✅ '{english_text}' ainda presente na coluna ENGLISH")
        else:
            print(f"❌ '{english_text}' foi removido da coluna ENGLISH")
            english_intact = False
    
    # Verifica se outras colunas não foram afetadas
    if "Шаблон 1" in translated_content and "模板-1" in translated_content:
        print(f"\n✅ Outras colunas (RUSSIAN, CHINESE, etc.) mantidas intactas")
    else:
        print(f"\n❌ Outras colunas foram afetadas")
        return False
    
    # Teste específico: verifica se a linha 2 está correta
    print("\n" + "=" * 70)
    print("VALIDAÇÃO 4: Estrutura da linha traduzida")
    print("=" * 70)
    
    line2 = lines[1]
    print(f"\nLinha 2 traduzida:")
    print(f"  {line2}")
    
    # Deve ter: chave;Template 1;;Шаблон 1;;;;Modelo 1 [TRADUZIDO];模板-1;;
    cells = line2.split(';')
    
    checks = [
        ("Chave (col 0)", cells[0] == "ggui/hud/building_templates/template_01"),
        ("ENGLISH (col 1)", cells[1] == "Template 1"),
        ("BRASILIAN (col 7)", cells[7] == "Modelo 1 [TRADUZIDO]"),
        ("CHINESE (col 8)", cells[8] == "模板-1"),
    ]
    
    all_checks_passed = True
    for check_name, result in checks:
        if result:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_checks_passed = False
    
    return all_found and all_applied and english_intact and all_checks_passed

def main():
    """Executa o teste"""
    print("\n🧪 TESTANDO NOVO COMPORTAMENTO CSV\n")
    
    try:
        result = test_new_csv_behavior()
        
        print("\n" + "=" * 70)
        print("RESULTADO FINAL")
        print("=" * 70)
        
        if result:
            print("\n🎉 Todos os testes passaram!")
            print("\nComportamento confirmado:")
            print("  ✅ Extrai textos da coluna ENGLISH")
            print("  ✅ Insere traduções na coluna BRASILIAN")
            print("  ✅ Mantém coluna ENGLISH intacta")
            print("  ✅ Preserva todas as outras colunas")
            print("  ✅ Estrutura do CSV mantida perfeitamente")
            return 0
        else:
            print("\n⚠️  Alguns testes falharam")
            return 1
    
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
