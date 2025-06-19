# src/utils/auditoria.py

from src.models.auditoria import Auditoria
from src.models.db import db
from flask_login import current_user
from datetime import datetime
import json
import logging

def registrar_auditoria(acao, entidade, valor_anterior=None, valor_novo=None, usuario=None):
    """
    Registra uma entrada no log de auditoria.

    :param acao: Ação realizada (str)
    :param entidade: Nome da entidade afetada (str)
    :param valor_anterior: Valor antigo (dict, list ou str, será serializado para JSON)
    :param valor_novo: Valor novo (dict, list ou str, será serializado para JSON)
    :param usuario: (opcional) Usuário para registrar, default: current_user
    """
    try:
        usuario = usuario or current_user
        usuario_id = getattr(usuario, 'id', None)
        log = Auditoria(
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            valor_anterior=json.dumps(valor_anterior) if valor_anterior else None,
            valor_novo=json.dumps(valor_novo) if valor_novo else None,
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        logging.error(f"Erro ao registrar auditoria: {e}")