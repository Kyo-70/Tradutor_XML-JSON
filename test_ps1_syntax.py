#!/usr/bin/env python3
"""
Script de teste para validar a sintaxe dos arquivos PowerShell (.ps1)
Verifica:
1. Caracteres problematicos (emojis, caracteres especiais)
2. Encoding correto (UTF-8 sem BOM ou ASCII)
3. Estrutura basica do PowerShell
"""

import os
import re
import sys

class PowerShellValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_file(self, filepath):
        """Valida um arquivo PowerShell"""
        self.errors = []
        self.warnings = []
        
        print(f"\n{'='*60}")
        print(f"Validando: {os.path.basename(filepath)}")
        print(f"{'='*60}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            self.errors.append(f"Erro ao ler arquivo: {e}")
            return False
        
        # Teste 1: Verificar caracteres problematicos (emojis)
        self._check_problematic_chars(lines)
        
        # Teste 2: Verificar estrutura de funcoes
        self._check_function_structure(lines)
        
        # Teste 3: Verificar encoding
        self._check_encoding(filepath)
        
        # Exibir resultados
        self._print_results()
        
        return len(self.errors) == 0
    
    def _check_problematic_chars(self, lines):
        """Verifica caracteres que podem causar problemas no Windows"""
        # Emojis e simbolos especiais que causam problemas
        problematic_ranges = [
            (0x1F300, 0x1F9FF),  # Emojis
            (0x2600, 0x26FF),    # Simbolos diversos (inclui checkmarks, etc)
            (0x2700, 0x27BF),    # Dingbats
            (0x2800, 0x28FF),    # Braille patterns (spinners)
        ]
        
        for line_num, line in enumerate(lines, 1):
            for char in line:
                code = ord(char)
                for start, end in problematic_ranges:
                    if start <= code <= end:
                        self.errors.append(
                            f"Linha {line_num}: Caractere problematico: '{char}' (U+{code:04X})"
                        )
                        break
    
    def _check_function_structure(self, lines):
        """Verifica estrutura basica de funcoes"""
        for line_num, line in enumerate(lines, 1):
            # Verificar se a funcao tem nome valido
            if re.match(r'^\s*function\s+', line, re.IGNORECASE):
                match = re.match(r'^\s*function\s+([\w-]+)', line, re.IGNORECASE)
                if not match:
                    self.errors.append(f"Linha {line_num}: Definicao de funcao invalida")
    
    def _check_encoding(self, filepath):
        """Verifica se o arquivo tem encoding correto"""
        try:
            with open(filepath, 'rb') as f:
                raw = f.read(3)
                # Verificar BOM UTF-8
                if raw.startswith(b'\xef\xbb\xbf'):
                    self.warnings.append("Arquivo tem BOM UTF-8 (pode causar problemas)")
        except Exception as e:
            self.warnings.append(f"Nao foi possivel verificar encoding: {e}")
    
    def _print_results(self):
        """Exibe os resultados da validacao"""
        if self.errors:
            print(f"\n[X] ERROS ENCONTRADOS ({len(self.errors)}):")
            for error in self.errors:
                print(f"    - {error}")
        
        if self.warnings:
            print(f"\n[!] AVISOS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"    - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n[+] Nenhum problema encontrado!")
        elif not self.errors:
            print("\n[+] Nenhum erro critico encontrado (apenas avisos)")
        
        return len(self.errors) == 0


def count_brackets(filepath):
    """Conta chaves e parenteses no arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    open_braces = content.count('{')
    close_braces = content.count('}')
    open_parens = content.count('(')
    close_parens = content.count(')')
    
    print(f"\n  Contagem de brackets:")
    print(f"    Chaves:     {{ = {open_braces}, }} = {close_braces} ", end="")
    if open_braces == close_braces:
        print("[OK]")
    else:
        print(f"[ERRO: diferenca de {abs(open_braces - close_braces)}]")
    
    print(f"    Parenteses: ( = {open_parens}, ) = {close_parens} ", end="")
    if open_parens == close_parens:
        print("[OK]")
    else:
        print(f"[ERRO: diferenca de {abs(open_parens - close_parens)}]")
    
    return open_braces == close_braces and open_parens == close_parens


def main():
    """Funcao principal"""
    print("="*60)
    print("   VALIDADOR DE SINTAXE POWERSHELL v2.0")
    print("="*60)
    
    # Diretorio do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Encontrar todos os arquivos .ps1
    ps1_files = []
    for file in os.listdir(script_dir):
        if file.endswith('.ps1'):
            ps1_files.append(os.path.join(script_dir, file))
    
    if not ps1_files:
        print("\n[!] Nenhum arquivo .ps1 encontrado!")
        return 1
    
    print(f"\nArquivos encontrados: {len(ps1_files)}")
    
    validator = PowerShellValidator()
    all_valid = True
    
    for filepath in ps1_files:
        if not validator.validate_file(filepath):
            all_valid = False
        
        # Verificar balanceamento de brackets
        if not count_brackets(filepath):
            all_valid = False
    
    print("\n" + "="*60)
    if all_valid:
        print("[+] TODOS OS ARQUIVOS PASSARAM NA VALIDACAO!")
        print("="*60)
        return 0
    else:
        print("[X] ALGUNS ARQUIVOS TEM PROBLEMAS!")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
