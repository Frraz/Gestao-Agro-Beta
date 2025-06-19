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

            # Enviar para cada documento
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
        # Assunto e corpo padrão
        entidade_nome = documento.nome_entidade
        assunto = f"Alerta: Documento '{documento.nome}' vencido ou próximo do vencimento"
        corpo = (
            f"Prezado(a),\n\n"
            f"O documento '{documento.nome}' relacionado a '{entidade_nome}' com vencimento em {documento.data_vencimento.strftime('%d/%m/%Y')} "
            f"está {'vencido' if documento.esta_vencido else 'próximo do vencimento'}.\n\n"
            "Por favor, regularize o quanto antes.\n"
            "Sistema Gestão Agrícola."
        )

        # E-mails do documento
        emails = documento.emails_notificacao if hasattr(documento, "emails_notificacao") else []
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
            whatsapps = documento.whatsapps_notificacao if hasattr(documento, "whatsapps_notificacao") else []
            for numero in whatsapps:
                try:
                    send_whatsapp_message(numero, corpo)
                except Exception as e:
                    logger.error(f"Erro ao enviar WhatsApp para {numero}: {str(e)}")

        # (Opcional) Notificação adicional para pessoa responsável, caso deseje manter compatibilidade
        if documento.pessoa:
            pessoa = documento.pessoa
            # E-mail da pessoa
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
            # WhatsApp da pessoa
            if getattr(pessoa, "notificar_whatsapp", False) and pessoa.whatsapp:
                try:
                    send_whatsapp_message(pessoa.whatsapp, corpo)
                except Exception as e:
                    logger.error(f"Erro ao enviar WhatsApp para {pessoa.whatsapp}: {str(e)}")

    def enviar_teste_whatsapp(self, documento, numeros_teste=None):
        """
        Envia mensagem de teste para os números de WhatsApp informados (ou configurados no documento).
        """
        whatsapps = numeros_teste or (documento.whatsapps_notificacao if hasattr(documento, "whatsapps_notificacao") else [])
        corpo = (
            f"Teste de notificação via WhatsApp do Sistema Gestão Agrícola.\n"
            f"Documento: {documento.nome}\n"
            f"Data de Vencimento: {documento.data_vencimento.strftime('%d/%m/%Y') if documento.data_vencimento else 'N/A'}"
        )
        for numero in whatsapps:
            try:
                send_whatsapp_message(numero, corpo)
                logger.info(f"Mensagem de teste enviada para WhatsApp: {numero}")
            except Exception as e:
                logger.error(f"Erro ao enviar WhatsApp de teste para {numero}: {str(e)}")