# /src/config.py

"""
Configuração centralizada para o sistema de Gestão Agro.
Utilize variáveis de ambiente para definir valores sensíveis e específicos de cada ambiente.

Exemplo de uso:
    from src.config import config_by_name
    app.config.from_object(config_by_name[os.getenv("FLASK_ENV", "development")])
"""

import os

def str_to_bool(value, default=False):
    """Converte string de ambiente para booleano."""
    if value is None:
        return default
    return value.strip().lower() in ("true", "1", "yes", "on")

class Config:
    """
    Configuração base. Não utilize diretamente, use uma das subclasses.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = str_to_bool(os.getenv("MAIL_USE_TLS", "true"), True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "admin@example.com")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    # Adicione novas variáveis abaixo conforme necessário.
    # EXEMPLO:
    # LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    # CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))

class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True

class TestingConfig(Config):
    """Configurações para ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Outras configs específicas de teste abaixo...

class ProductionConfig(Config):
    """Configurações para produção."""
    DEBUG = False

config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)