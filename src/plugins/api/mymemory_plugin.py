"""
Plugin de API MyMemory para o Sistema de Tradução
Implementa a integração com a API MyMemory (gratuita)
"""

import requests
import time
from typing import Dict, List, Optional, Tuple

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_plugin_base import APIPluginBase, PluginInfo


class MyMemoryPlugin(APIPluginBase):
    """
    Plugin para tradução usando a API MyMemory.
    
    API gratuita com limite de 1000 palavras/dia sem chave,
    ou 10000 palavras/dia com email registrado.
    """
    
    API_URL = "https://api.mymemory.translated.net/get"
    
    def __init__(self):
        super().__init__()
        self._email: Optional[str] = None
        self._last_request_time = 0
        self._rate_limit = 1.0  # Requisições por segundo (mais conservador)
    
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="mymemory",
            display_name="MyMemory",
            description="API de tradução gratuita baseada em memória de tradução. "
                       "Limite: 1000 palavras/dia (sem email) ou 10000/dia (com email).",
            version="1.0.0",
            author="Game Translator",
            requires_api_key=False,  # Email é opcional
            free_tier_limit=5000,  # Aproximado em caracteres
            rate_limit=1.0
        )
    
    def _wait_rate_limit(self):
        """Aguarda para respeitar o rate limit"""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self._rate_limit
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self._last_request_time = time.time()
    
    def set_email(self, email: str):
        """Define o email para aumentar o limite diário"""
        self._email = email
    
    def translate(self, text: str, source_lang: str = 'en',
                  target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando a API MyMemory"""
        if not text or not text.strip():
            return text
        
        try:
            self._wait_rate_limit()
            
            params = {
                'q': text,
                'langpair': f'{source_lang}|{target_lang}'
            }
            
            # Adiciona email se configurado (aumenta limite)
            if self._email:
                params['de'] = self._email
            
            # Adiciona chave de API se configurada
            if self._api_key:
                params['key'] = self._api_key
            
            response = requests.get(
                self.API_URL,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verifica se houve erro
                if result.get('responseStatus') == 200:
                    match = result.get('responseData', {})
                    translation = match.get('translatedText', '')
                    
                    # MyMemory pode retornar texto em maiúsculas quando não encontra
                    if translation and translation != text.upper():
                        return translation
                
                elif result.get('responseStatus') == 429:
                    print("MyMemory: Limite diário excedido")
                
                elif result.get('responseStatus') == 403:
                    print("MyMemory: Acesso negado")
            
            return None
            
        except requests.exceptions.Timeout:
            print("MyMemory: Timeout na requisição")
            return None
        except Exception as e:
            print(f"MyMemory: Erro na tradução: {e}")
            return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                        target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos (um por vez, pois API não suporta batch)"""
        results = {}
        
        for text in texts:
            translation = self.translate(text, source_lang, target_lang)
            if translation:
                results[text] = translation
        
        return results
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testa a conexão com a API MyMemory"""
        try:
            params = {
                'q': 'Hello',
                'langpair': 'en|pt'
            }
            
            if self._email:
                params['de'] = self._email
            
            response = requests.get(
                self.API_URL,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('responseStatus') == 200:
                    return True, "Conexão OK"
                
                elif result.get('responseStatus') == 429:
                    return False, "Limite diário excedido"
                
                else:
                    return False, f"Erro: {result.get('responseDetails', 'Desconhecido')}"
            
            else:
                return False, f"Erro HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Timeout na conexão"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """Retorna idiomas suportados pelo MyMemory"""
        return [
            ('en', 'English'),
            ('pt', 'Portuguese'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('it', 'Italian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('zh', 'Chinese'),
            ('ru', 'Russian'),
            ('ar', 'Arabic'),
            ('hi', 'Hindi'),
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
            ('th', 'Thai'),
            ('vi', 'Vietnamese'),
            ('id', 'Indonesian'),
        ]
