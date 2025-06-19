# /src/utils/notificacao_documentos_service.py

import logging
from flask import current_app
from src.models.documento import Documento
from src.utils.email_service import EmailService
from src.utils.whatsapp_service import send_whatsapp_message

logger = logging.getLogger(__name__)

class NotificacaoDocumentosService:
    def __init__(self):
        self.email_service = EmailService()

    def verificar_e_enviar_notificacoes(self):
        """
        Verifica documentos vencidos ou próximos do vencimento e envia notificações por e-mail e WhatsApp.
        """
        try:
            documentos = Documento.query.filter(Documento.data_vencimento.isnot(None)).all()
            documentos_vencidos = []
            documentos_proximos = []

            for documento in documentos:
                if documento.esta_vencido:
                    documentos_vencidos.append(documento)
                elif documento.precisa_notificar:
                    documentos_proximos.append(documento)

            # Enviar para cada responsável
            for doc in documentos_vencidos + documentos_proximos:
                self.notificar_responsaveis(doc)
            return documentos_vencidos, documentos_proximos
        except Exception as e:
            logger.error(f"Erro ao verificar documentos vencidos: {str(e)}")
            return [], []

    def notificar_responsaveis(self, documento):
        """
        Envia notificação por e-mail e WhatsApp para as pessoas vinculadas ao documento.
        """
        # Supondo que documento.pessoa é o responsável (adapte se houver mais de um)
        if not documento.pessoa:
            return
        pessoa = documento.pessoa
        assunto = f"Alerta: Documento '{documento.nome}' vencido ou próximo do vencimento"
        corpo = (
            f"Prezado(a) {pessoa.nome},\n\n"
            f"O documento '{documento.nome}' com vencimento em {documento.data_vencimento.strftime('%d/%m/%Y')} "
            f"está {'vencido' if documento.esta_vencido else 'próximo do vencimento'}.\n\n"
            "Por favor, regularize o quanto antes.\n"
            "Sistema Gestão Agrícola."
        )

        # E-mail
        if pessoa.email and getattr(pessoa, "notificar_email", True):
            try:
                self.email_service.send_email(
                    destinatarios=[pessoa.email],
                    assunto=assunto,
                    corpo=corpo,
                    html=False
                )
            except Exception as e:
                logger.error(f"Erro ao enviar e-mail para {pessoa.email}: {str(e)}")

        # WhatsApp
        if getattr(pessoa, "notificar_whatsapp", False) and pessoa.whatsapp:
            try:
                send_whatsapp_message(pessoa.whatsapp, corpo)
            except Exception as e:
                logger.error(f"Erro ao enviar WhatsApp para {pessoa.whatsapp}: {str(e)}")