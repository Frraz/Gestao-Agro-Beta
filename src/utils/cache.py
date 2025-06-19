# src/utils/cache.py

import redis
from flask import current_app, has_app_context
import pickle
from datetime import timedelta
import logging
from functools import wraps

class CacheManager:
    """Gerenciador de cache usando Redis."""
    
    def __init__(self, app=None):
        self.redis_client = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa o cache com a aplicação Flask."""
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            self.redis_client.ping()
            app.logger.info('Cache Redis conectado com sucesso')
        except Exception as e:
            app.logger.warning(f'Não foi possível conectar ao Redis: {e}')
            self.redis_client = None
    
    def get(self, key):
        """Recupera valor do cache."""
        if not self.redis_client:
            return None
        try:
            value = self.redis_client.get(key)
            if value:
                return pickle.loads(value)
        except Exception as e:
            self._log_error(f'Erro ao recuperar cache {key}: {e}')
        return None
    
    def set(self, key, value, timeout=300):
        """Armazena valor no cache."""
        if not self.redis_client:
            return False
        try:
            serialized_value = pickle.dumps(value)
            return self.redis_client.setex(key, timeout, serialized_value)
        except Exception as e:
            self._log_error(f'Erro ao armazenar cache {key}: {e}')
            return False
    
    def delete(self, key):
        """Remove valor do cache."""
        if not self.redis_client:
            return False
        try:
            return self.redis_client.delete(key)
        except Exception as e:
            self._log_error(f'Erro ao deletar cache {key}: {e}')
            return False
    
    def clear_pattern(self, pattern):
        """Remove todas as chaves que correspondem ao padrão."""
        if not self.redis_client:
            return False
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return True
        except Exception as e:
            self._log_error(f'Erro ao limpar cache com padrão {pattern}: {e}')
            return False

    def _log_error(self, message):
        """Loga erro usando logger Flask se disponível, senão logger root."""
        if has_app_context():
            current_app.logger.error(message)
        else:
            logging.error(message)

# Instância global do cache
cache = CacheManager()

def cached(timeout=300, key_prefix='', key_func=None):
    """
    Decorator para cache de funções.
    :param timeout: Tempo de expiração em segundos.
    :param key_prefix: Prefixo da chave do cache.
    :param key_func: Função opcional para geração da chave (args, kwargs) -> str.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{key_prefix}:{f.__name__}:{hash(str(args) + str(kwargs))}"
            # Tentar recuperar do cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            # Executar função e armazenar no cache
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator