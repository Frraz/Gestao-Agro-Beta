# /src/utils/tasks_notificacao.py

from src.utils.notificacao_endividamento_service import NotificacaoEndividamentoService
from src.utils.notificacao_documentos_service import NotificacaoDocumentosService
import logging

logger = logging.getLogger(__name__)

def processar_notificacoes():
    """Tarefa agendada para processar notificações de endividamento e documentos"""
    try:
        endividamento_service = NotificacaoEndividamentoService()
        notificacoes_endividamento = endividamento_service.verificar_e_enviar_notificacoes()
        doc_service = NotificacaoDocumentosService()
        doc_service.verificar_e_enviar_notificacoes()
        logger.info(f"Notificações processadas. Endividamento: {notificacoes_endividamento}")
        return notificacoes_endividamento
    except Exception as e:
        logger.error(f"Erro ao processar notificações agendadas: {str(e)}")
        return 0