"""
Módulo de Validação de Placeholders
Identifica e valida placeholders em textos de jogos para evitar erros de tradução
"""

import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PlaceholderMatch:
    """Representa um placeholder encontrado no texto"""
    placeholder: str
    pattern_type: str  # Tipo do padrão (ex: 'curly_braces', 'percent', 'dollar')
    start: int
    end: int


@dataclass
class PlaceholderValidationResult:
    """Resultado da validação de placeholders"""
    is_valid: bool
    original_placeholders: List[PlaceholderMatch]
    translation_placeholders: List[PlaceholderMatch]
    missing_placeholders: List[str]  # Placeholders que estão no original mas não na tradução
    extra_placeholders: List[str]  # Placeholders que estão na tradução mas não no original
    modified_placeholders: List[Tuple[str, str]]  # Placeholders que foram modificados
    warnings: List[str]


class PlaceholderValidator:
    """
    Validador de placeholders para textos de jogos.
    
    Identifica placeholders comuns em textos de jogos e valida se eles
    foram preservados corretamente na tradução.
    
    Padrões suportados:
    - {variable} - Chaves (Unity, Unreal, etc.)
    - %s, %d, %f, %1$s - Printf style
    - $variable, ${variable} - Shell/Template style
    - <tag>, </tag> - Tags HTML/XML
    - [variable] - Colchetes
    - {{variable}} - Duplas chaves (Jinja, etc.)
    - %variable% - Variáveis de ambiente style
    - @variable - At-sign style
    - #variable# - Hash style
    """
    
    # Padrões de placeholder organizados por tipo
    PATTERNS = {
        'curly_braces': r'\{[^{}]+\}',  # {variable}
        'double_curly': r'\{\{[^{}]+\}\}',  # {{variable}}
        'percent_format': r'%(?:\d+\$)?[+-]?(?:\d+)?(?:\.\d+)?[sdifFeEgGxXoubcpn%]',  # %s, %d, %1$s
        'dollar_simple': r'\$[a-zA-Z_][a-zA-Z0-9_]*',  # $variable
        'dollar_braces': r'\$\{[^{}]+\}',  # ${variable}
        'square_brackets': r'\[[^\[\]]+\]',  # [variable]
        'html_tags': r'</?[a-zA-Z][a-zA-Z0-9]*(?:\s+[^>]*)?>',  # <tag>, </tag>
        'percent_var': r'%[a-zA-Z_][a-zA-Z0-9_]*%',  # %variable%
        'at_sign': r'@[a-zA-Z_][a-zA-Z0-9_]*',  # @variable
        'hash_var': r'#[a-zA-Z_][a-zA-Z0-9_]*#',  # #variable#
        'angle_brackets': r'<<[^<>]+>>',  # <<variable>>
        'color_codes': r'\[/?[a-fA-F0-9]{6}\]|\[/?color[^\]]*\]',  # [FF0000], [color=red]
        'newline_codes': r'\\n|\\r|\\t|<br\s*/?>',  # \n, \r, \t, <br>
        'escape_sequences': r'\\[nrt"\'\\]',  # Sequências de escape
    }
    
    def __init__(self, custom_patterns: Dict[str, str] = None):
        """
        Inicializa o validador.
        
        Args:
            custom_patterns: Padrões adicionais personalizados {nome: regex}
        """
        self.patterns = self.PATTERNS.copy()
        if custom_patterns:
            self.patterns.update(custom_patterns)
        
        # Compila os padrões
        self._compiled_patterns = {
            name: re.compile(pattern)
            for name, pattern in self.patterns.items()
        }
    
    def find_placeholders(self, text: str) -> List[PlaceholderMatch]:
        """
        Encontra todos os placeholders em um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Lista de placeholders encontrados
        """
        if not text:
            return []
        
        matches = []
        seen_positions = set()  # Evita duplicatas de posição
        
        for pattern_type, compiled in self._compiled_patterns.items():
            for match in compiled.finditer(text):
                # Evita sobreposição de matches
                pos_key = (match.start(), match.end())
                if pos_key not in seen_positions:
                    seen_positions.add(pos_key)
                    matches.append(PlaceholderMatch(
                        placeholder=match.group(),
                        pattern_type=pattern_type,
                        start=match.start(),
                        end=match.end()
                    ))
        
        # Ordena por posição
        matches.sort(key=lambda m: m.start)
        return matches
    
    def get_placeholder_set(self, text: str) -> Set[str]:
        """
        Retorna conjunto de placeholders únicos em um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Conjunto de placeholders
        """
        matches = self.find_placeholders(text)
        return {m.placeholder for m in matches}
    
    def validate_translation(self, original: str, translation: str) -> PlaceholderValidationResult:
        """
        Valida se os placeholders foram preservados na tradução.
        
        Args:
            original: Texto original
            translation: Texto traduzido
            
        Returns:
            Resultado da validação
        """
        original_matches = self.find_placeholders(original)
        translation_matches = self.find_placeholders(translation)
        
        original_set = {m.placeholder for m in original_matches}
        translation_set = {m.placeholder for m in translation_matches}
        
        # Placeholders faltando na tradução
        missing = list(original_set - translation_set)
        
        # Placeholders extras na tradução
        extra = list(translation_set - original_set)
        
        # Verifica modificações (case sensitivity, espaços, etc.)
        modified = []
        for orig_ph in original_set:
            for trans_ph in translation_set:
                # Verifica se é uma versão modificada
                if self._is_modified_placeholder(orig_ph, trans_ph):
                    modified.append((orig_ph, trans_ph))
        
        # Gera warnings
        warnings = []
        
        if missing:
            warnings.append(f"Placeholders removidos: {', '.join(missing)}")
        
        if extra:
            warnings.append(f"Placeholders adicionados: {', '.join(extra)}")
        
        if modified:
            for orig, trans in modified:
                warnings.append(f"Placeholder modificado: '{orig}' → '{trans}'")
        
        # Verifica ordem dos placeholders (importante para %1$s, %2$s, etc.)
        if len(original_matches) > 1 and len(translation_matches) > 1:
            orig_order = [m.placeholder for m in original_matches]
            trans_order = [m.placeholder for m in translation_matches]
            
            # Filtra apenas os que existem em ambos
            common_orig = [p for p in orig_order if p in translation_set]
            common_trans = [p for p in trans_order if p in original_set]
            
            if common_orig != common_trans:
                warnings.append("Ordem dos placeholders alterada (pode causar problemas)")
        
        is_valid = len(missing) == 0 and len(extra) == 0 and len(modified) == 0
        
        return PlaceholderValidationResult(
            is_valid=is_valid,
            original_placeholders=original_matches,
            translation_placeholders=translation_matches,
            missing_placeholders=missing,
            extra_placeholders=extra,
            modified_placeholders=modified,
            warnings=warnings
        )
    
    def _is_modified_placeholder(self, original: str, translation: str) -> bool:
        """
        Verifica se um placeholder foi modificado (não é exatamente igual).
        
        Args:
            original: Placeholder original
            translation: Placeholder na tradução
            
        Returns:
            True se parece ser uma versão modificada
        """
        if original == translation:
            return False
        
        # Normaliza para comparação
        orig_normalized = original.lower().replace(' ', '').replace('_', '')
        trans_normalized = translation.lower().replace(' ', '').replace('_', '')
        
        # Se são muito similares, provavelmente é uma modificação
        if orig_normalized == trans_normalized:
            return True
        
        # Verifica se um contém o outro (ex: {name} vs {player_name})
        orig_inner = re.sub(r'[{}\[\]<>$%@#]', '', original)
        trans_inner = re.sub(r'[{}\[\]<>$%@#]', '', translation)
        
        if orig_inner and trans_inner:
            if orig_inner in trans_inner or trans_inner in orig_inner:
                return True
        
        return False
    
    def highlight_placeholders(self, text: str, 
                               highlight_format: str = "**{placeholder}**") -> str:
        """
        Destaca placeholders no texto para visualização.
        
        Args:
            text: Texto com placeholders
            highlight_format: Formato de destaque (usa {placeholder})
            
        Returns:
            Texto com placeholders destacados
        """
        matches = self.find_placeholders(text)
        
        if not matches:
            return text
        
        # Processa de trás para frente para não afetar posições
        result = text
        for match in reversed(matches):
            highlighted = highlight_format.format(placeholder=match.placeholder)
            result = result[:match.start] + highlighted + result[match.end:]
        
        return result
    
    def get_placeholder_summary(self, text: str) -> Dict:
        """
        Retorna um resumo dos placeholders encontrados.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Dicionário com resumo
        """
        matches = self.find_placeholders(text)
        
        by_type = {}
        for match in matches:
            if match.pattern_type not in by_type:
                by_type[match.pattern_type] = []
            by_type[match.pattern_type].append(match.placeholder)
        
        return {
            'total': len(matches),
            'unique': len(set(m.placeholder for m in matches)),
            'by_type': by_type,
            'placeholders': [m.placeholder for m in matches]
        }
    
    def suggest_fix(self, original: str, translation: str) -> Optional[str]:
        """
        Sugere uma correção para a tradução baseada nos placeholders originais.
        
        Args:
            original: Texto original
            translation: Tradução com possíveis erros
            
        Returns:
            Tradução corrigida ou None se não puder corrigir
        """
        validation = self.validate_translation(original, translation)
        
        if validation.is_valid:
            return None  # Não precisa de correção
        
        fixed = translation
        
        # Tenta restaurar placeholders faltando
        for missing in validation.missing_placeholders:
            # Procura por versões modificadas
            for orig, trans in validation.modified_placeholders:
                if orig == missing:
                    # Substitui a versão modificada pela original
                    fixed = fixed.replace(trans, orig)
                    break
        
        # Verifica se a correção resolveu
        new_validation = self.validate_translation(original, fixed)
        
        if new_validation.is_valid or len(new_validation.warnings) < len(validation.warnings):
            return fixed
        
        return None


# Instância global para uso conveniente
default_validator = PlaceholderValidator()


def validate_placeholders(original: str, translation: str) -> PlaceholderValidationResult:
    """
    Função de conveniência para validar placeholders.
    
    Args:
        original: Texto original
        translation: Texto traduzido
        
    Returns:
        Resultado da validação
    """
    return default_validator.validate_translation(original, translation)


def find_placeholders(text: str) -> List[PlaceholderMatch]:
    """
    Função de conveniência para encontrar placeholders.
    
    Args:
        text: Texto a ser analisado
        
    Returns:
        Lista de placeholders encontrados
    """
    return default_validator.find_placeholders(text)
