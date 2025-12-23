"""
Plugin de API DeepL para o Sistema de Tradução
Implementa a integração com a API DeepL Free e Pro
"""

import requests
import time
from typing import Dict, List, Optional, Tuple

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_plugin_base import APIPluginBase, PluginInfo


class DeepLPlugin(APIPluginBase):
    """
    Plugin para tradução usando a API DeepL.
    
    Suporta tanto a API Free quanto a Pro.
    """
    
    # URLs das APIs
    API_URL_FREE = "https://api-free.deepl.com/v2/translate"
    API_URL_PRO = "https://api.deepl.com/v2/translate"
    
    def __init__(self):
        super().__init__()
        self._use_pro = False
        self._last_request_time = 0
        self._rate_limit = 5.0  # Requisições por segundo
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="deepl",
            display_name="DeepL Translator",
            description="Tradução de alta qualidade usando a API DeepL. "
                       "Suporta planos Free (500k chars/mês) e Pro.",
            version="1.0.0",
            author="Game Translator",
            requires_api_key=True,
            free_tier_limit=500000,
            rate_limit=5.0
        )
    
    def _get_api_url(self) -> str:
        """Retorna a URL da API baseado no tipo de conta"""
        return self.API_URL_PRO if self._use_pro else self.API_URL_FREE
    
    def _wait_rate_limit(self):
        """Aguarda para respeitar o rate limit"""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self._rate_limit
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self._last_request_time = time.time()
    
    def _map_language_code(self, lang: str) -> str:
        """Mapeia códigos de idioma para o formato DeepL"""
        mapping = {
            'pt': 'PT-BR',
            'pt-br': 'PT-BR',
            'pt-pt': 'PT-PT',
            'en': 'EN',
            'en-us': 'EN-US',
            'en-gb': 'EN-GB',
            'es': 'ES',
            'fr': 'FR',
            'de': 'DE',
            'it': 'IT',
            'ja': 'JA',
            'ko': 'KO',
            'zh': 'ZH',
            'ru': 'RU',
            'pl': 'PL',
            'nl': 'NL',
        }
        return mapping.get(lang.lower(), lang.upper())
    
    def translate(self, text: str, source_lang: str = 'en',
                  target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando a API DeepL"""
        if not self._api_key:
            return None
        
        if not text or not text.strip():
            return text
        
        try:
            self._wait_rate_limit()
            
            headers = {
                'Authorization': f'DeepL-Auth-Key {self._api_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'text': text,
                'source_lang': self._map_language_code(source_lang),
                'target_lang': self._map_language_code(target_lang),
            }
            
            response = requests.post(
                self._get_api_url(),
                headers=headers,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                translations = result.get('translations', [])
                if translations:
                    return translations[0].get('text', '')
            
            elif response.status_code == 403:
                # Chave inválida ou limite excedido
                print(f"DeepL: Erro de autenticação (403)")
            
            elif response.status_code == 456:
                # Quota excedida
                print(f"DeepL: Quota excedida (456)")
            
            return None
            
        except requests.exceptions.Timeout:
            print("DeepL: Timeout na requisição")
            return None
        except Exception as e:
            print(f"DeepL: Erro na tradução: {e}")
            return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                        target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos de uma vez"""
        results = {}
        
        if not self._api_key or not texts:
            return results
        
        try:
            self._wait_rate_limit()
            
            headers = {
                'Authorization': f'DeepL-Auth-Key {self._api_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # DeepL aceita múltiplos textos na mesma requisição
            data = {
                'text': texts,
                'source_lang': self._map_language_code(source_lang),
                'target_lang': self._map_language_code(target_lang),
            }
            
            response = requests.post(
                self._get_api_url(),
                headers=headers,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                translations = result.get('translations', [])
                
                for i, trans in enumerate(translations):
                    if i < len(texts):
                        results[texts[i]] = trans.get('text', '')
            
            return results
            
        except Exception as e:
            print(f"DeepL: Erro na tradução em lote: {e}")
            return results
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testa a conexão com a API DeepL"""
        if not self._api_key:
            return False, "Chave de API não configurada"
        
        try:
            # Usa endpoint de usage para testar
            url = self._get_api_url().replace('/translate', '/usage')
            
            headers = {
                'Authorization': f'DeepL-Auth-Key {self._api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                usage = response.json()
                char_count = usage.get('character_count', 0)
                char_limit = usage.get('character_limit', 0)
                remaining = char_limit - char_count
                
                return True, f"Conexão OK. Caracteres restantes: {remaining:,}"
            
            elif response.status_code == 403:
                return False, "Chave de API inválida"
            
            else:
                return False, f"Erro HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Timeout na conexão"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """Retorna idiomas suportados pelo DeepL"""
        return [
            ('en', 'English'),
            ('pt-br', 'Portuguese (Brazil)'),
            ('pt-pt', 'Portuguese (Portugal)'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('it', 'Italian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('zh', 'Chinese'),
            ('ru', 'Russian'),
            ('pl', 'Polish'),
            ('nl', 'Dutch'),
            ('sv', 'Swedish'),
            ('da', 'Danish'),
            ('fi', 'Finnish'),
            ('el', 'Greek'),
            ('cs', 'Czech'),
            ('ro', 'Romanian'),
            ('hu', 'Hungarian'),
            ('sk', 'Slovak'),
            ('bg', 'Bulgarian'),
            ('sl', 'Slovenian'),
            ('lt', 'Lithuanian'),
            ('lv', 'Latvian'),
            ('et', 'Estonian'),
            ('id', 'Indonesian'),
            ('tr', 'Turkish'),
            ('uk', 'Ukrainian'),
        ]
    
    def set_use_pro(self, use_pro: bool):
        """Define se deve usar a API Pro"""
        self._use_pro = use_pro
    
    def is_using_pro(self) -> bool:
        """Verifica se está usando a API Pro"""
        return self._use_pro
