"""
Módulo de Sugestões de Tradução Contextual
Busca traduções similares na memória para ajudar a manter consistência terminológica
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from difflib import SequenceMatcher

from database import TranslationMemory


@dataclass
class ContextualSuggestion:
    """Representa uma sugestão de tradução contextual"""
    original_text: str
    translated_text: str
    context_type: str  # 'exact', 'contains_term', 'similar', 'pattern'
    relevance_score: float  # 0.0 a 1.0
    matched_term: str  # Termo que foi encontrado em comum
    notes: str = ""


class ContextualSuggestionEngine:
    """
    Motor de sugestões contextuais para tradução.
    
    Busca na memória de tradução por textos que contenham termos similares
    ao texto sendo traduzido, ajudando o tradutor a manter consistência
    terminológica em todo o projeto.
    """
    
    # Palavras comuns a ignorar na busca (stop words)
    STOP_WORDS = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
        'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
        'and', 'but', 'if', 'or', 'because', 'until', 'while', 'this',
        'that', 'these', 'those', 'it', 'its', 'you', 'your', 'he', 'she',
        'his', 'her', 'they', 'them', 'their', 'we', 'our', 'i', 'me', 'my',
        # Português
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'da', 'do',
        'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'por', 'para', 'com',
        'sem', 'sob', 'sobre', 'entre', 'até', 'após', 'desde', 'durante',
        'e', 'ou', 'mas', 'porém', 'contudo', 'todavia', 'entretanto',
        'que', 'se', 'quando', 'como', 'onde', 'porque', 'pois', 'já',
        'ainda', 'também', 'só', 'apenas', 'mesmo', 'muito', 'pouco',
        'mais', 'menos', 'bem', 'mal', 'assim', 'então', 'logo', 'agora',
        'ele', 'ela', 'eles', 'elas', 'você', 'vocês', 'nós', 'eu', 'tu',
        'seu', 'sua', 'seus', 'suas', 'meu', 'minha', 'meus', 'minhas',
        'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas',
        'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'isso', 'aquilo',
    }
    
    def __init__(self, translation_memory: TranslationMemory):
        """
        Inicializa o motor de sugestões.
        
        Args:
            translation_memory: Instância da memória de tradução
        """
        self.memory = translation_memory
        self._term_cache: Dict[str, List[Tuple[str, str]]] = {}
        self._cache_valid = False
    
    def invalidate_cache(self):
        """Invalida o cache de termos"""
        self._cache_valid = False
        self._term_cache.clear()
    
    def _build_term_cache(self):
        """Constrói cache de termos para busca rápida"""
        if self._cache_valid:
            return
        
        self._term_cache.clear()
        
        # Obtém todas as traduções
        all_translations = self.memory.search_translations("", limit=10000)
        
        for original, translated in all_translations:
            # Extrai termos significativos
            terms = self._extract_terms(original)
            
            for term in terms:
                term_lower = term.lower()
                if term_lower not in self._term_cache:
                    self._term_cache[term_lower] = []
                self._term_cache[term_lower].append((original, translated))
        
        self._cache_valid = True
    
    def _extract_terms(self, text: str) -> Set[str]:
        """
        Extrai termos significativos de um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Conjunto de termos significativos
        """
        # Remove pontuação e divide em palavras
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
        
        # Filtra stop words e palavras muito curtas
        terms = {
            word for word in words
            if word not in self.STOP_WORDS and len(word) >= 3
        }
        
        return terms
    
    def get_suggestions(self, text: str, max_suggestions: int = 10) -> List[ContextualSuggestion]:
        """
        Obtém sugestões de tradução baseadas no contexto.
        
        Args:
            text: Texto a ser traduzido
            max_suggestions: Número máximo de sugestões
            
        Returns:
            Lista de sugestões ordenadas por relevância
        """
        if not self.memory.is_connected():
            return []
        
        suggestions = []
        
        # 1. Busca exata
        exact = self.memory.get_translation(text)
        if exact:
            suggestions.append(ContextualSuggestion(
                original_text=text,
                translated_text=exact,
                context_type='exact',
                relevance_score=1.0,
                matched_term=text,
                notes="Tradução exata encontrada na memória"
            ))
        
        # 2. Busca por termos
        self._build_term_cache()
        terms = self._extract_terms(text)
        
        seen_originals = {text}  # Evita duplicatas
        
        for term in terms:
            term_lower = term.lower()
            if term_lower in self._term_cache:
                for original, translated in self._term_cache[term_lower]:
                    if original not in seen_originals:
                        seen_originals.add(original)
                        
                        # Calcula relevância
                        relevance = self._calculate_relevance(text, original, term)
                        
                        suggestions.append(ContextualSuggestion(
                            original_text=original,
                            translated_text=translated,
                            context_type='contains_term',
                            relevance_score=relevance,
                            matched_term=term,
                            notes=f"Contém o termo '{term}'"
                        ))
        
        # 3. Busca por similaridade (para textos sem matches de termo)
        if len(suggestions) < max_suggestions:
            similar = self._find_similar_texts(text, seen_originals, max_suggestions - len(suggestions))
            suggestions.extend(similar)
        
        # Ordena por relevância e limita
        suggestions.sort(key=lambda s: s.relevance_score, reverse=True)
        return suggestions[:max_suggestions]
    
    def _calculate_relevance(self, query: str, candidate: str, matched_term: str) -> float:
        """
        Calcula a relevância de uma sugestão.
        
        Args:
            query: Texto sendo traduzido
            candidate: Texto candidato da memória
            matched_term: Termo que causou o match
            
        Returns:
            Score de relevância entre 0.0 e 1.0
        """
        # Similaridade de sequência
        seq_ratio = SequenceMatcher(None, query.lower(), candidate.lower()).ratio()
        
        # Proporção de termos em comum
        query_terms = self._extract_terms(query)
        candidate_terms = self._extract_terms(candidate)
        
        if query_terms and candidate_terms:
            common_terms = query_terms & candidate_terms
            term_ratio = len(common_terms) / max(len(query_terms), len(candidate_terms))
        else:
            term_ratio = 0.0
        
        # Penaliza textos muito diferentes em tamanho
        len_ratio = min(len(query), len(candidate)) / max(len(query), len(candidate))
        
        # Combina os scores
        relevance = (seq_ratio * 0.4) + (term_ratio * 0.4) + (len_ratio * 0.2)
        
        return min(1.0, relevance)
    
    def _find_similar_texts(self, text: str, exclude: Set[str], 
                           max_results: int) -> List[ContextualSuggestion]:
        """
        Encontra textos similares usando busca fuzzy.
        
        Args:
            text: Texto de referência
            exclude: Textos a excluir
            max_results: Número máximo de resultados
            
        Returns:
            Lista de sugestões similares
        """
        suggestions = []
        
        # Busca por substring
        search_results = self.memory.search_translations(text[:50], limit=100)
        
        for original, translated in search_results:
            if original in exclude:
                continue
            
            # Calcula similaridade
            similarity = SequenceMatcher(None, text.lower(), original.lower()).ratio()
            
            if similarity >= 0.3:  # Threshold mínimo
                suggestions.append(ContextualSuggestion(
                    original_text=original,
                    translated_text=translated,
                    context_type='similar',
                    relevance_score=similarity,
                    matched_term="",
                    notes=f"Similaridade: {similarity:.0%}"
                ))
        
        # Ordena e limita
        suggestions.sort(key=lambda s: s.relevance_score, reverse=True)
        return suggestions[:max_results]
    
    def get_term_translations(self, term: str) -> List[Tuple[str, str, str]]:
        """
        Obtém todas as traduções que contêm um termo específico.
        
        Útil para verificar como um termo foi traduzido em diferentes contextos.
        
        Args:
            term: Termo a buscar
            
        Returns:
            Lista de tuplas (original, tradução, contexto)
        """
        self._build_term_cache()
        
        term_lower = term.lower()
        results = []
        
        if term_lower in self._term_cache:
            for original, translated in self._term_cache[term_lower]:
                # Extrai contexto (texto ao redor do termo)
                context = self._extract_context(original, term)
                results.append((original, translated, context))
        
        return results
    
    def _extract_context(self, text: str, term: str, context_size: int = 30) -> str:
        """
        Extrai o contexto ao redor de um termo no texto.
        
        Args:
            text: Texto completo
            term: Termo a destacar
            context_size: Caracteres de contexto em cada lado
            
        Returns:
            Texto com contexto
        """
        match = re.search(re.escape(term), text, re.IGNORECASE)
        if not match:
            return text[:context_size * 2]
        
        start = max(0, match.start() - context_size)
        end = min(len(text), match.end() + context_size)
        
        context = text[start:end]
        
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
        
        return context
    
    def analyze_terminology(self, texts: List[str]) -> Dict[str, Dict]:
        """
        Analisa a terminologia de uma lista de textos.
        
        Args:
            texts: Lista de textos a analisar
            
        Returns:
            Dicionário com análise de termos
        """
        term_analysis = {}
        
        for text in texts:
            terms = self._extract_terms(text)
            
            for term in terms:
                if term not in term_analysis:
                    term_analysis[term] = {
                        'count': 0,
                        'translations': set(),
                        'contexts': []
                    }
                
                term_analysis[term]['count'] += 1
                
                # Busca traduções existentes
                translations = self.get_term_translations(term)
                for orig, trans, ctx in translations:
                    # Extrai como o termo foi traduzido
                    term_analysis[term]['translations'].add(trans)
                    term_analysis[term]['contexts'].append(ctx)
        
        # Converte sets para listas para serialização
        for term in term_analysis:
            term_analysis[term]['translations'] = list(term_analysis[term]['translations'])
        
        return term_analysis
    
    def suggest_consistent_translation(self, text: str, term: str) -> Optional[str]:
        """
        Sugere uma tradução consistente para um termo baseado no histórico.
        
        Args:
            text: Texto completo sendo traduzido
            term: Termo específico a traduzir
            
        Returns:
            Sugestão de tradução ou None
        """
        translations = self.get_term_translations(term)
        
        if not translations:
            return None
        
        # Conta frequência de cada tradução
        translation_counts = {}
        for orig, trans, ctx in translations:
            # Tenta extrair como o termo foi traduzido
            # (simplificado - idealmente usaria alinhamento de palavras)
            if trans not in translation_counts:
                translation_counts[trans] = 0
            translation_counts[trans] += 1
        
        # Retorna a tradução mais comum
        if translation_counts:
            most_common = max(translation_counts.items(), key=lambda x: x[1])
            return most_common[0]
        
        return None
