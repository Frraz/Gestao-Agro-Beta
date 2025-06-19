# src/utils/audit.py

from flask_login import current_user
from flask import has_request_context, request
from src.models.audit_log import AuditLog
from src.models.db import db
import logging

def log_audit(action, details=None, user=None):
    """
    Registra uma ação de auditoria no banco de dados.

    :param action: Ação realizada (ex: 'login', 'delete_document', etc.)
    :param details: Detalhes adicionais (string ou JSON serializável)
    :param user: (opcional) Usuário para registrar (default: current_user)
    """
    try:
        # Permite passar usuário explicitamente, útil para tarefas background
        user = user or current_user
        user_id = getattr(user, 'id', None)
        username = getattr(user, 'nome', None) or getattr(user, 'email', None)

        # Só pega o IP se estiver em contexto de request
        ip = request.remote_addr if has_request_context() else None

        log = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            details=details,
            ip=ip
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        logging.error(f"Erro ao registrar auditoria: {e}")