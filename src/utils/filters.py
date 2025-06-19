#/src/utils/filters.py

import json
from markupsafe import Markup
import logging

def prettyjson(value):
    """
    Converte um valor (dict, list ou JSON string) em JSON formatado para exibir no template Jinja.
    Retorna Markup seguro.
    """
    try:
        if isinstance(value, str):
            value = json.loads(value)
        return Markup(json.dumps(value, indent=2, ensure_ascii=False))
    except Exception as e:
        logging.warning(f"Erro ao formatar JSON em prettyjson: {e}")
        return value

def register_filters(app):
    """
    Registra filtros customizados no ambiente Jinja do Flask app.
    """
    app.jinja_env.filters['prettyjson'] = prettyjson