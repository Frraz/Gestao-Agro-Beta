#/src/utils/whatsapp_service.py

from twilio.rest import Client
import logging
import os

logger = logging.getLogger(__name__)

def send_whatsapp_message(numero, mensagem):
    """
    Envia mensagem WhatsApp usando Twilio.
    Retorna True se enviado com sucesso, False em caso de erro.
    """
    # Pegue as credenciais do ambiente para segurança!
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    from_num = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')  # Default sandbox correto

    if not account_sid or not auth_token:
        logger.error("Credenciais do Twilio não configuradas.")
        return False

    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            from_=from_num,
            body=mensagem,
            to=f'whatsapp:{numero}' if not str(numero).startswith('whatsapp:') else str(numero)
        )
        logger.info(f"Mensagem WhatsApp enviada para {numero}: SID {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar WhatsApp para {numero}: {str(e)}")
        return False