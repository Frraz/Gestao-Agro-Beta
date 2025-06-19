# /src/utils/notificacao_documentos_service.py

import logging
from flask import current_app
from src.models.documento import Documento
from src.utils.email_service import EmailService
from src.utils.whatsapp_service import send_whatsapp_message

logger = logging.getLogger(__name__)

class NotificacaoDocumentosService:
    """Serviço centralizado para envio de notificações de documentos por e-mail e WhatsApp."""

    def __init__(self):
        self.email_service = EmailService()

    def verificar_e_enviar_notificacoes(self):
        """
        Verifica documentos vencidos ou próximos do vencimento e envia notificações por e-mail e WhatsApp.
        Retorna listas de documentos vencidos e próximos do vencimento.
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

            # Enviar notificações para cada documento
            for doc in documentos_vencidos + documentos_proximos:
                self.notificar_responsaveis(doc)
            return documentos_vencidos, documentos_proximos
        except Exception as e:
            logger.error(f"Erro ao verificar documentos vencidos: {str(e)}")
            return [], []

    def notificar_responsaveis(self, documento):
        """
        Envia notificação por e-mail e WhatsApp para os contatos vinculados ao documento.
        """
        entidade_nome = getattr(documento, "nome_entidade", "")
        assunto = f"Alerta: Documento '{getattr(documento, 'nome', '')}' vencido ou próximo do vencimento"
        corpo = (
            f"Prezado(a),\n\n"
            f"O documento '{getattr(documento, 'nome', '')}' relacionado a '{entidade_nome}' com vencimento em {documento.data_vencimento.strftime('%d/%m/%Y')} "
            f"está {'vencido' if getattr(documento, 'esta_vencido', False) else 'próximo do vencimento'}.\n\n"
            "Por favor, regularize o quanto antes.\n"
            "Sistema Gestão Agrícola."
        )

        # E-mails do documento
        emails = getattr(documento, "emails_notificacao", [])
        if emails:
            try:
                self.email_service.send_email(
                    destinatarios=emails,
                    assunto=assunto,
                    corpo=corpo,
                    html=False
                )
            except Exception as e:
                logger.error(f"Erro ao enviar e-mail para {emails}: {str(e)}")

        # WhatsApps do documento
        if getattr(documento, "notificar_whatsapp", False):
            whatsapps = getattr(documento, "whatsapps_notificacao", [])
            for numero in whatsapps:
                try:
                    send_whatsapp_message(numero, corpo)
                except Exception as e:
                    logger.error(f"Erro ao enviar WhatsApp para {numero}: {str(e)}")

        # Notificação adicional para pessoa responsável
        pessoa = getattr(documento, "pessoa", None)
        if pessoa:
            # E-mail da pessoa
            if getattr(pessoa, "email", None) and getattr(pessoa, "notificar_email", True):
                try:
                    self.email_service.send_email(
                        destinatarios=[pessoa.email],
                        assunto=assunto,
                        corpo=corpo,
                        html=False
                    )
                except Exception as e:
                    logger.error(f"Erro ao enviar e-mail para {pessoa.email}: {str(e)}")
            # WhatsApp da pessoa
            if getattr(pessoa, "notificar_whatsapp", False) and getattr(pessoa, "whatsapp", None):
                try:
                    send_whatsapp_message(pessoa.whatsapp, corpo)
                except Exception as e:
                    logger.error(f"Erro ao enviar WhatsApp para {pessoa.whatsapp}: {str(e)}")

    def enviar_teste_whatsapp(self, documento, numeros_teste=None):
        """
        Envia mensagem de teste para os números de WhatsApp informados (ou configurados no documento).
        """
        whatsapps = numeros_teste or getattr(documento, "whatsapps_notificacao", [])
        corpo = (
            f"Teste de notificação via WhatsApp do Sistema Gestão Agrícola.\n"
            f"Documento: {getattr(documento, 'nome', '')}\n"
            f"Data de Vencimento: {documento.data_vencimento.strftime('%d/%m/%Y') if getattr(documento, 'data_vencimento', None) else 'N/A'}"
        )
        for numero in whatsapps:
            try:
                send_whatsapp_message(numero, corpo)
                logger.info(f"Mensagem de teste enviada para WhatsApp: {numero}")
            except Exception as e:
                logger.error(f"Erro ao enviar WhatsApp de teste para {numero}: {str(e)}")