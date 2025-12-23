"""
Plugin de API Google Translate para o Sistema de Tradução
Implementa a integração com a API Google Cloud Translation
"""

import requests
import time
from typing import Dict, List, Optional, Tuple

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_plugin_base import APIPluginBase, PluginInfo


class GoogleTranslatePlugin(APIPluginBase):
    """
    Plugin para tradução usando a API Google Cloud Translation.
    
    Requer uma chave de API do Google Cloud.
    """
    
    API_URL = "https://translation.googleapis.com/language/translate/v2"
    
    def __init__(self):
        super().__init__()
        self._last_request_time = 0
        self._rate_limit = 10.0  # Requisições por segundo
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="google",
            display_name="Google Translate",
            description="Tradução usando a API Google Cloud Translation. "
                       "Suporta mais de 100 idiomas. Plano gratuito: 500k chars/mês.",
            version="1.0.0",
            author="Game Translator",
            requires_api_key=True,
            free_tier_limit=500000,
            rate_limit=10.0
        )
    
    def _wait_rate_limit(self):
        """Aguarda para respeitar o rate limit"""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self._rate_limit
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self._last_request_time = time.time()
    
    def translate(self, text: str, source_lang: str = 'en',
                  target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando a API Google Translate"""
        if not self._api_key:
            return None
        
        if not text or not text.strip():
            return text
        
        try:
            self._wait_rate_limit()
            
            params = {
                'key': self._api_key,
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            response = requests.post(
                self.API_URL,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                translations = result.get('data', {}).get('translations', [])
                if translations:
                    return translations[0].get('translatedText', '')
            
            elif response.status_code == 403:
                print("Google Translate: Erro de autenticação (403)")
            
            elif response.status_code == 429:
                print("Google Translate: Rate limit excedido (429)")
            
            return None
            
        except requests.exceptions.Timeout:
            print("Google Translate: Timeout na requisição")
            return None
        except Exception as e:
            print(f"Google Translate: Erro na tradução: {e}")
            return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                        target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos de uma vez"""
        results = {}
        
        if not self._api_key or not texts:
            return results
        
        try:
            self._wait_rate_limit()
            
            # Google aceita múltiplos textos via parâmetro 'q' repetido
            params = {
                'key': self._api_key,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            # Adiciona cada texto como parâmetro 'q'
            data = [('q', text) for text in texts]
            
            response = requests.post(
                self.API_URL,
                params=params,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                translations = result.get('data', {}).get('translations', [])
                
                for i, trans in enumerate(translations):
                    if i < len(texts):
                        results[texts[i]] = trans.get('translatedText', '')
            
            return results
            
        except Exception as e:
            print(f"Google Translate: Erro na tradução em lote: {e}")
            return results
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testa a conexão com a API Google Translate"""
        if not self._api_key:
            return False, "Chave de API não configurada"
        
        try:
            # Testa com uma tradução simples
            params = {
                'key': self._api_key,
                'q': 'test',
                'source': 'en',
                'target': 'pt',
                'format': 'text'
            }
            
            response = requests.post(
                self.API_URL,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Conexão OK"
            
            elif response.status_code == 403:
                return False, "Chave de API inválida ou sem permissão"
            
            elif response.status_code == 400:
                error = response.json().get('error', {})
                message = error.get('message', 'Erro desconhecido')
                return False, f"Erro: {message}"
            
            else:
                return False, f"Erro HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Timeout na conexão"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """Retorna idiomas suportados pelo Google Translate"""
        return [
            ('en', 'English'),
            ('pt', 'Portuguese'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('it', 'Italian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('zh', 'Chinese (Simplified)'),
            ('zh-TW', 'Chinese (Traditional)'),
            ('ru', 'Russian'),
            ('ar', 'Arabic'),
            ('hi', 'Hindi'),
            ('th', 'Thai'),
            ('vi', 'Vietnamese'),
            ('id', 'Indonesian'),
            ('ms', 'Malay'),
            ('tr', 'Turkish'),
            ('pl', 'Polish'),
            ('nl', 'Dutch'),
            ('sv', 'Swedish'),
            ('da', 'Danish'),
            ('fi', 'Finnish'),
            ('no', 'Norwegian'),
            ('cs', 'Czech'),
            ('el', 'Greek'),
            ('he', 'Hebrew'),
            ('hu', 'Hungarian'),
            ('ro', 'Romanian'),
            ('uk', 'Ukrainian'),
        ]
