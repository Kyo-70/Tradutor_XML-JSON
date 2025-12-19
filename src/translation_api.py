"""
Módulo de API de Tradução
Suporte para tradução automática via DeepL, Google Translate e LibreTranslate
OTIMIZADO PARA PLANOS GRATUITOS - Minimiza uso de caracteres e requisições
"""

import requests
from typing import List, Optional, Dict, Tuple
import time
import json
import os
from datetime import datetime, timedelta
from collections import OrderedDict

# ============================================================================
# CONFIGURAÇÕES DE LIMITES DOS PLANOS GRATUITOS
# ============================================================================

class APILimits:
    """Limites dos planos gratuitos das APIs"""
    
    # DeepL Free: 500.000 caracteres/mês
    DEEPL_FREE_MONTHLY_CHARS = 500000
    DEEPL_FREE_REQUESTS_PER_SECOND = 5
    
    # Google Cloud Free: 500.000 caracteres/mês
    GOOGLE_FREE_MONTHLY_CHARS = 500000
    GOOGLE_FREE_REQUESTS_PER_SECOND = 10
    
    # LibreTranslate: Sem limites (self-hosted) ou variável (público)
    LIBRE_REQUESTS_PER_SECOND = 2
    
    # MyMemory Free: 1000 palavras/dia sem chave, 10000 com chave
    MYMEMORY_FREE_DAILY_CHARS = 5000
    MYMEMORY_REQUESTS_PER_SECOND = 1

# ============================================================================
# CACHE DE TRADUÇÕES (EVITA REQUISIÇÕES DUPLICADAS)
# ============================================================================

class TranslationCache:
    """Cache em memória para evitar requisições duplicadas à API"""
    
    def __init__(self, max_size: int = 10000):
        """
        Inicializa o cache
        
        Args:
            max_size: Número máximo de entradas no cache
        """
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
    
    def get(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Busca tradução no cache"""
        key = f"{source_lang}:{target_lang}:{text}"
        
        if key in self.cache:
            # Move para o final (LRU)
            self.cache.move_to_end(key)
            return self.cache[key]
        
        return None
    
    def set(self, text: str, translation: str, source_lang: str, target_lang: str):
        """Armazena tradução no cache"""
        key = f"{source_lang}:{target_lang}:{text}"
        
        # Remove item mais antigo se necessário
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        self.cache[key] = translation
    
    def clear(self):
        """Limpa o cache"""
        self.cache.clear()

# ============================================================================
# CONTADOR DE USO (MONITORA LIMITES)
# ============================================================================

class UsageTracker:
    """Rastreia uso de caracteres e requisições das APIs"""
    
    def __init__(self, storage_path: str = "api_usage.json"):
        """
        Inicializa o rastreador
        
        Args:
            storage_path: Caminho para arquivo de persistência
        """
        self.storage_path = storage_path
        self.usage = self._load_usage()
    
    def _load_usage(self) -> dict:
        """Carrega dados de uso do arquivo"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    
                    # Reseta se for novo mês
                    if data.get('month') != datetime.now().strftime('%Y-%m'):
                        return self._create_empty_usage()
                    
                    return data
            except:
                pass
        
        return self._create_empty_usage()
    
    def _create_empty_usage(self) -> dict:
        """Cria estrutura de uso vazia"""
        return {
            'month': datetime.now().strftime('%Y-%m'),
            'day': datetime.now().strftime('%Y-%m-%d'),
            'deepl': {'chars': 0, 'requests': 0},
            'google': {'chars': 0, 'requests': 0},
            'libre': {'chars': 0, 'requests': 0},
            'mymemory': {'chars_today': 0, 'requests': 0}
        }
    
    def _save_usage(self):
        """Salva dados de uso no arquivo"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.usage, f, indent=2)
        except:
            pass
    
    def add_usage(self, api: str, chars: int):
        """
        Registra uso de caracteres
        
        Args:
            api: Nome da API (deepl, google, libre, mymemory)
            chars: Número de caracteres usados
        """
        # Reseta se for novo mês
        if self.usage.get('month') != datetime.now().strftime('%Y-%m'):
            self.usage = self._create_empty_usage()
        
        # Reseta MyMemory se for novo dia
        if self.usage.get('day') != datetime.now().strftime('%Y-%m-%d'):
            self.usage['day'] = datetime.now().strftime('%Y-%m-%d')
            self.usage['mymemory']['chars_today'] = 0
        
        if api in self.usage:
            if api == 'mymemory':
                self.usage[api]['chars_today'] += chars
            else:
                self.usage[api]['chars'] += chars
            self.usage[api]['requests'] += 1
        
        self._save_usage()
    
    def get_remaining(self, api: str) -> int:
        """
        Retorna caracteres restantes para a API
        
        Args:
            api: Nome da API
            
        Returns:
            Caracteres restantes
        """
        limits = {
            'deepl': APILimits.DEEPL_FREE_MONTHLY_CHARS,
            'google': APILimits.GOOGLE_FREE_MONTHLY_CHARS,
            'mymemory': APILimits.MYMEMORY_FREE_DAILY_CHARS
        }
        
        if api == 'mymemory':
            used = self.usage.get(api, {}).get('chars_today', 0)
        else:
            used = self.usage.get(api, {}).get('chars', 0)
        
        limit = limits.get(api, float('inf'))
        return max(0, limit - used)
    
    def can_use(self, api: str, chars: int) -> bool:
        """
        Verifica se pode usar a API
        
        Args:
            api: Nome da API
            chars: Caracteres a serem usados
            
        Returns:
            True se pode usar
        """
        return self.get_remaining(api) >= chars
    
    def get_stats(self) -> dict:
        """Retorna estatísticas de uso"""
        return {
            'deepl': {
                'used': self.usage.get('deepl', {}).get('chars', 0),
                'remaining': self.get_remaining('deepl'),
                'limit': APILimits.DEEPL_FREE_MONTHLY_CHARS,
                'requests': self.usage.get('deepl', {}).get('requests', 0)
            },
            'google': {
                'used': self.usage.get('google', {}).get('chars', 0),
                'remaining': self.get_remaining('google'),
                'limit': APILimits.GOOGLE_FREE_MONTHLY_CHARS,
                'requests': self.usage.get('google', {}).get('requests', 0)
            },
            'mymemory': {
                'used_today': self.usage.get('mymemory', {}).get('chars_today', 0),
                'remaining_today': self.get_remaining('mymemory'),
                'daily_limit': APILimits.MYMEMORY_FREE_DAILY_CHARS,
                'requests': self.usage.get('mymemory', {}).get('requests', 0)
            }
        }

# ============================================================================
# RATE LIMITER (RESPEITA LIMITES DE REQUISIÇÕES)
# ============================================================================

class RateLimiter:
    """Controla taxa de requisições para respeitar limites das APIs"""
    
    def __init__(self):
        self.last_request: Dict[str, float] = {}
        self.limits = {
            'deepl': 1.0 / APILimits.DEEPL_FREE_REQUESTS_PER_SECOND,
            'google': 1.0 / APILimits.GOOGLE_FREE_REQUESTS_PER_SECOND,
            'libre': 1.0 / APILimits.LIBRE_REQUESTS_PER_SECOND,
            'mymemory': 1.0 / APILimits.MYMEMORY_REQUESTS_PER_SECOND
        }
    
    def wait_if_needed(self, api: str):
        """
        Aguarda se necessário para respeitar rate limit
        
        Args:
            api: Nome da API
        """
        if api not in self.last_request:
            self.last_request[api] = 0
        
        min_interval = self.limits.get(api, 0.5)
        elapsed = time.time() - self.last_request[api]
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_request[api] = time.time()

# ============================================================================
# CLASSES DE TRADUTORES
# ============================================================================

class TranslationAPI:
    """Classe base para APIs de tradução"""
    
    def __init__(self):
        self.cache = TranslationCache()
        self.usage_tracker = UsageTracker()
        self.rate_limiter = RateLimiter()
    
    def translate(self, text: str, source_lang: str = 'en', 
                 target_lang: str = 'pt') -> Optional[str]:
        raise NotImplementedError
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                       target_lang: str = 'pt') -> Dict[str, str]:
        raise NotImplementedError
    
    def get_name(self) -> str:
        raise NotImplementedError

class DeepLTranslator(TranslationAPI):
    """Tradutor usando API do DeepL (Otimizado para plano gratuito)"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        
        # Detecta se é chave gratuita ou paga
        if ':fx' in api_key:
            self.base_url = "https://api-free.deepl.com/v2/translate"
        else:
            self.base_url = "https://api.deepl.com/v2/translate"
        
        self.lang_map = {
            'en': 'EN',
            'pt': 'PT-BR',
            'es': 'ES',
            'fr': 'FR',
            'de': 'DE',
            'it': 'IT',
            'ja': 'JA',
            'zh': 'ZH',
            'ko': 'KO',
            'ru': 'RU'
        }
    
    def get_name(self) -> str:
        return "DeepL"
    
    def translate(self, text: str, source_lang: str = 'en',
                 target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando DeepL"""
        if not text or not text.strip():
            return text
        
        # Verifica cache primeiro
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
        
        # Verifica limite de uso
        char_count = len(text)
        if not self.usage_tracker.can_use('deepl', char_count):
            print(f"⚠️ Limite mensal do DeepL atingido!")
            return None
        
        try:
            # Respeita rate limit
            self.rate_limiter.wait_if_needed('deepl')
            
            target = self.lang_map.get(target_lang, target_lang.upper())
            
            params = {
                'auth_key': self.api_key,
                'text': text,
                'target_lang': target
            }
            
            response = requests.post(self.base_url, data=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'translations' in data and len(data['translations']) > 0:
                    translation = data['translations'][0]['text']
                    
                    # Armazena no cache
                    self.cache.set(text, translation, source_lang, target_lang)
                    
                    # Registra uso
                    self.usage_tracker.add_usage('deepl', char_count)
                    
                    return translation
            elif response.status_code == 456:
                print("⚠️ Cota do DeepL excedida!")
            else:
                print(f"Erro DeepL: {response.status_code}")
            
            return None
            
        except Exception as e:
            print(f"Erro ao traduzir com DeepL: {e}")
            return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                       target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos com DeepL (otimizado)"""
        results = {}
        
        # Filtra textos já em cache
        texts_to_translate = []
        for text in texts:
            if not text or not text.strip():
                continue
            
            cached = self.cache.get(text, source_lang, target_lang)
            if cached:
                results[text] = cached
            else:
                texts_to_translate.append(text)
        
        # Traduz apenas textos não cacheados
        for text in texts_to_translate:
            translation = self.translate(text, source_lang, target_lang)
            if translation:
                results[text] = translation
        
        return results

class GoogleTranslator(TranslationAPI):
    """Tradutor usando API do Google Translate (Otimizado para plano gratuito)"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
    
    def get_name(self) -> str:
        return "Google"
    
    def translate(self, text: str, source_lang: str = 'en',
                 target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando Google Translate"""
        if not text or not text.strip():
            return text
        
        # Verifica cache primeiro
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
        
        # Verifica limite de uso
        char_count = len(text)
        if not self.usage_tracker.can_use('google', char_count):
            print(f"⚠️ Limite mensal do Google atingido!")
            return None
        
        try:
            # Respeita rate limit
            self.rate_limiter.wait_if_needed('google')
            
            params = {
                'key': self.api_key,
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            response = requests.post(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'translations' in data['data']:
                    translations = data['data']['translations']
                    if len(translations) > 0:
                        translation = translations[0]['translatedText']
                        
                        # Armazena no cache
                        self.cache.set(text, translation, source_lang, target_lang)
                        
                        # Registra uso
                        self.usage_tracker.add_usage('google', char_count)
                        
                        return translation
            else:
                print(f"Erro Google: {response.status_code}")
            
            return None
            
        except Exception as e:
            print(f"Erro ao traduzir com Google: {e}")
            return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                       target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos com Google (otimizado com batching)"""
        results = {}
        
        # Filtra textos já em cache
        texts_to_translate = []
        for text in texts:
            if not text or not text.strip():
                continue
            
            cached = self.cache.get(text, source_lang, target_lang)
            if cached:
                results[text] = cached
            else:
                texts_to_translate.append(text)
        
        if not texts_to_translate:
            return results
        
        # Verifica limite total
        total_chars = sum(len(t) for t in texts_to_translate)
        if not self.usage_tracker.can_use('google', total_chars):
            print(f"⚠️ Limite mensal do Google seria excedido!")
            # Traduz apenas o que couber
            remaining = self.usage_tracker.get_remaining('google')
            char_count = 0
            limited_texts = []
            for text in texts_to_translate:
                if char_count + len(text) <= remaining:
                    limited_texts.append(text)
                    char_count += len(text)
            texts_to_translate = limited_texts
        
        # Google suporta batch nativo - agrupa em lotes de 100
        batch_size = 100
        for i in range(0, len(texts_to_translate), batch_size):
            batch = texts_to_translate[i:i + batch_size]
            
            try:
                self.rate_limiter.wait_if_needed('google')
                
                params = {
                    'key': self.api_key,
                    'q': batch,
                    'source': source_lang,
                    'target': target_lang,
                    'format': 'text'
                }
                
                response = requests.post(self.base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and 'translations' in data['data']:
                        translations = data['data']['translations']
                        
                        for j, trans in enumerate(translations):
                            if j < len(batch):
                                original = batch[j]
                                translated = trans['translatedText']
                                
                                results[original] = translated
                                self.cache.set(original, translated, source_lang, target_lang)
                        
                        # Registra uso
                        batch_chars = sum(len(t) for t in batch)
                        self.usage_tracker.add_usage('google', batch_chars)
                        
            except Exception as e:
                print(f"Erro ao traduzir batch com Google: {e}")
        
        return results

class MyMemoryTranslator(TranslationAPI):
    """
    Tradutor usando MyMemory API (GRATUITO)
    - Sem chave: 1000 palavras/dia
    - Com email: 10000 palavras/dia
    """
    
    def __init__(self, email: str = None):
        super().__init__()
        self.email = email
        self.base_url = "https://api.mymemory.translated.net/get"
    
    def get_name(self) -> str:
        return "MyMemory"
    
    def translate(self, text: str, source_lang: str = 'en',
                 target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando MyMemory (gratuito)"""
        if not text or not text.strip():
            return text
        
        # Verifica cache primeiro
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
        
        # Verifica limite diário
        char_count = len(text)
        if not self.usage_tracker.can_use('mymemory', char_count):
            print(f"⚠️ Limite diário do MyMemory atingido!")
            return None
        
        try:
            # Respeita rate limit (MyMemory é mais lento)
            self.rate_limiter.wait_if_needed('mymemory')
            
            params = {
                'q': text,
                'langpair': f'{source_lang}|{target_lang}'
            }
            
            if self.email:
                params['de'] = self.email
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('responseStatus') == 200:
                    translation = data.get('responseData', {}).get('translatedText')
                    
                    if translation:
                        # Armazena no cache
                        self.cache.set(text, translation, source_lang, target_lang)
                        
                        # Registra uso
                        self.usage_tracker.add_usage('mymemory', char_count)
                        
                        return translation
            
            return None
            
        except Exception as e:
            print(f"Erro ao traduzir com MyMemory: {e}")
            return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                       target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos com MyMemory"""
        results = {}
        
        for text in texts:
            if not text or not text.strip():
                continue
            
            translation = self.translate(text, source_lang, target_lang)
            if translation:
                results[text] = translation
        
        return results

class LibreTranslator(TranslationAPI):
    """
    Tradutor usando LibreTranslate (GRATUITO E SEM LIMITES)
    Pode usar servidor público ou self-hosted
    """
    
    # Servidores públicos gratuitos
    PUBLIC_SERVERS = [
        "https://libretranslate.com",
        "https://translate.argosopentech.com",
        "https://translate.terraprint.co"
    ]
    
    def __init__(self, server_url: str = None, api_key: str = None):
        super().__init__()
        self.server_url = server_url or self.PUBLIC_SERVERS[0]
        self.api_key = api_key
        self.current_server_index = 0
    
    def get_name(self) -> str:
        return "LibreTranslate"
    
    def _try_next_server(self):
        """Tenta próximo servidor público"""
        self.current_server_index = (self.current_server_index + 1) % len(self.PUBLIC_SERVERS)
        self.server_url = self.PUBLIC_SERVERS[self.current_server_index]
    
    def translate(self, text: str, source_lang: str = 'en',
                 target_lang: str = 'pt') -> Optional[str]:
        """Traduz um texto usando LibreTranslate"""
        if not text or not text.strip():
            return text
        
        # Verifica cache primeiro
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
        
        # Tenta até 3 servidores diferentes
        for attempt in range(3):
            try:
                # Respeita rate limit
                self.rate_limiter.wait_if_needed('libre')
                
                url = f"{self.server_url}/translate"
                
                payload = {
                    'q': text,
                    'source': source_lang,
                    'target': target_lang,
                    'format': 'text'
                }
                
                if self.api_key:
                    payload['api_key'] = self.api_key
                
                response = requests.post(url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    translation = data.get('translatedText')
                    
                    if translation:
                        # Armazena no cache
                        self.cache.set(text, translation, source_lang, target_lang)
                        
                        # Registra uso (apenas para estatísticas)
                        self.usage_tracker.add_usage('libre', len(text))
                        
                        return translation
                
                elif response.status_code == 429:
                    # Rate limited - tenta outro servidor
                    self._try_next_server()
                    continue
                
            except requests.exceptions.RequestException:
                # Erro de conexão - tenta outro servidor
                self._try_next_server()
                continue
            except Exception as e:
                print(f"Erro ao traduzir com LibreTranslate: {e}")
                break
        
        return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                       target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos com LibreTranslate"""
        results = {}
        
        for text in texts:
            if not text or not text.strip():
                continue
            
            translation = self.translate(text, source_lang, target_lang)
            if translation:
                results[text] = translation
        
        return results

# ============================================================================
# GERENCIADOR DE APIs (COM FALLBACK INTELIGENTE)
# ============================================================================

class TranslationAPIManager:
    """Gerencia diferentes APIs de tradução com fallback inteligente"""
    
    def __init__(self):
        """Inicializa o gerenciador"""
        self.apis: Dict[str, TranslationAPI] = {}
        self.active_api: Optional[str] = None
        self.usage_tracker = UsageTracker()
        
        # Adiciona LibreTranslate como fallback gratuito padrão
        self.add_libre()
    
    def add_deepl(self, api_key: str):
        """Adiciona API DeepL"""
        self.apis['deepl'] = DeepLTranslator(api_key)
        if not self.active_api:
            self.active_api = 'deepl'
    
    def add_google(self, api_key: str):
        """Adiciona API Google"""
        self.apis['google'] = GoogleTranslator(api_key)
        if not self.active_api:
            self.active_api = 'google'
    
    def add_mymemory(self, email: str = None):
        """Adiciona API MyMemory (gratuita)"""
        self.apis['mymemory'] = MyMemoryTranslator(email)
        if not self.active_api:
            self.active_api = 'mymemory'
    
    def add_libre(self, server_url: str = None, api_key: str = None):
        """Adiciona API LibreTranslate (gratuita)"""
        self.apis['libre'] = LibreTranslator(server_url, api_key)
        # LibreTranslate é sempre fallback, não define como ativo automaticamente
    
    def set_active_api(self, api_name: str) -> bool:
        """Define a API ativa"""
        if api_name in self.apis:
            self.active_api = api_name
            return True
        return False
    
    def translate(self, text: str, source_lang: str = 'en',
                 target_lang: str = 'pt') -> Optional[str]:
        """
        Traduz usando a API ativa com fallback automático
        
        Ordem de fallback:
        1. API ativa configurada
        2. Outras APIs configuradas
        3. LibreTranslate (sempre disponível)
        """
        if not text or not text.strip():
            return text
        
        # Tenta API ativa primeiro
        if self.active_api and self.active_api in self.apis:
            result = self.apis[self.active_api].translate(text, source_lang, target_lang)
            if result:
                return result
        
        # Fallback para outras APIs
        for api_name, api in self.apis.items():
            if api_name == self.active_api:
                continue
            
            result = api.translate(text, source_lang, target_lang)
            if result:
                return result
        
        return None
    
    def translate_batch(self, texts: List[str], source_lang: str = 'en',
                       target_lang: str = 'pt') -> Dict[str, str]:
        """Traduz múltiplos textos usando a API ativa"""
        if not texts:
            return {}
        
        # Remove duplicatas mantendo ordem
        unique_texts = list(dict.fromkeys(t for t in texts if t and t.strip()))
        
        if self.active_api and self.active_api in self.apis:
            return self.apis[self.active_api].translate_batch(unique_texts, source_lang, target_lang)
        
        # Fallback para LibreTranslate
        if 'libre' in self.apis:
            return self.apis['libre'].translate_batch(unique_texts, source_lang, target_lang)
        
        return {}
    
    def get_available_apis(self) -> List[str]:
        """Retorna lista de APIs disponíveis"""
        return list(self.apis.keys())
    
    def get_usage_stats(self) -> dict:
        """Retorna estatísticas de uso de todas as APIs"""
        return self.usage_tracker.get_stats()
    
    def get_api_info(self) -> dict:
        """Retorna informações sobre as APIs configuradas"""
        info = {}
        
        for name, api in self.apis.items():
            info[name] = {
                'name': api.get_name(),
                'active': name == self.active_api,
                'cache_size': len(api.cache.cache)
            }
        
        return info
