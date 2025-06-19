# /src/utils/notificacao_endividamento_service.py

from datetime import datetime, date
from sqlalchemy import and_
from src.models.db import db
from src.models.endividamento import Endividamento
from src.models.notificacao_endividamento import NotificacaoEndividamento, HistoricoNotificacao
from src.utils.email_service import EmailService
from src.utils.whatsapp_service import send_whatsapp_message
import json
import logging

logger = logging.getLogger(__name__)

class NotificacaoEndividamentoService:
    INTERVALOS_NOTIFICACAO = {
        '6_meses': 180,
        '3_meses': 90,
        '30_dias': 30,
        '15_dias': 15,
        '7_dias': 7,
        '3_dias': 3,
        '1_dia': 1
    }
    
    def __init__(self):
        self.email_service = EmailService()
    
    def verificar_e_enviar_notificacoes(self):
        hoje = date.today()
        notificacoes_enviadas = 0
        try:
            endividamentos = db.session.query(Endividamento).join(
                NotificacaoEndividamento
            ).filter(
                NotificacaoEndividamento.ativo == True,
                Endividamento.data_vencimento_final > hoje
            ).all()
            for endividamento in endividamentos:
                notificacoes_enviadas += self._processar_endividamento(endividamento, hoje)
            logger.info(f"Processamento de notificações concluído. {notificacoes_enviadas} notificações enviadas.")
            return notificacoes_enviadas
        except Exception as e:
            logger.error(f"Erro ao processar notificações: {str(e)}")
            return 0
    
    def _processar_endividamento(self, endividamento, hoje):
        notificacoes_enviadas = 0
        dias_para_vencimento = (endividamento.data_vencimento_final - hoje).days
        for tipo_notificacao, dias_antecedencia in self.INTERVALOS_NOTIFICACAO.items():
            if dias_para_vencimento == dias_antecedencia:
                if not self._ja_foi_enviada(endividamento.id, tipo_notificacao):
                    if self._enviar_notificacao(endividamento, tipo_notificacao):
                        notificacoes_enviadas += 1
        return notificacoes_enviadas
    
    def _ja_foi_enviada(self, endividamento_id, tipo_notificacao):
        return db.session.query(HistoricoNotificacao).filter(
            and_(
                HistoricoNotificacao.endividamento_id == endividamento_id,
                HistoricoNotificacao.tipo_notificacao == tipo_notificacao,
                HistoricoNotificacao.sucesso == True
            )
        ).first() is not None
    
    def _enviar_notificacao(self, endividamento, tipo_notificacao):
        try:
            notificacao_config = NotificacaoEndividamento.query.filter_by(
                endividamento_id=endividamento.id,
                ativo=True
            ).first()
            if not notificacao_config:
                return False
            emails = json.loads(notificacao_config.emails) if notificacao_config.emails else []
            whatsapps = json.loads(notificacao_config.whatsapps) if notificacao_config.whatsapps else []
            enviar_whatsapp = notificacao_config.notificar_whatsapp
            assunto, corpo = self._preparar_email(endividamento, tipo_notificacao)
            sucesso_email = sucesso_whatsapp = False

            # E-mail
            if emails:
                sucesso_email = self.email_service.send_email(
                    destinatarios=emails,
                    assunto=assunto,
                    corpo=corpo,
                    html=True
                )
            # WhatsApp
            if enviar_whatsapp and whatsapps:
                mensagem = self._preparar_mensagem_whatsapp(endividamento, tipo_notificacao)
                sucesso_whatsapp = all(
                    send_whatsapp_message(numero, mensagem) for numero in whatsapps
                )
            # Histórico
            self._registrar_historico(
                endividamento.id,
                tipo_notificacao,
                emails,
                whatsapps,
                sucesso_email or sucesso_whatsapp
            )
            return sucesso_email or sucesso_whatsapp
        except Exception as e:
            self._registrar_historico(
                endividamento.id,
                tipo_notificacao,
                [],
                [],
                False,
                str(e)
            )
            return False

    def _preparar_email(self, endividamento, tipo_notificacao):
        dias = self.INTERVALOS_NOTIFICACAO[tipo_notificacao]
        if dias >= 30:
            if dias == 180:
                periodo = "6 meses"
            elif dias == 90:
                periodo = "3 meses"
            else:
                periodo = f"{dias} dias"
        else:
            periodo = f"{dias} dia{'s' if dias > 1 else ''}"
        assunto = f"Lembrete: Endividamento vence em {periodo} - {endividamento.banco}"
        valor_total_pendente = sum(
            parcela.valor for parcela in endividamento.parcelas 
            if not parcela.pago
        )
        pessoas_nomes = [pessoa.nome for pessoa in endividamento.pessoas]
        corpo = f"""
        <html>
        <body>
            <h2>🚨 Lembrete de Vencimento de Endividamento</h2>
            <p>Este é um lembrete automático sobre um endividamento que vencerá em <strong>{periodo}</strong>.</p>
            <ul>
                <li><strong>Banco:</strong> {endividamento.banco}</li>
                <li><strong>Número da Proposta:</strong> {endividamento.numero_proposta}</li>
                <li><strong>Data de Vencimento:</strong> {endividamento.data_vencimento_final.strftime('%d/%m/%Y')}</li>
                <li><strong>Taxa de Juros:</strong> {endividamento.taxa_juros}% {'a.a.' if endividamento.tipo_taxa_juros == 'ano' else 'a.m.'}</li>
                {f'<li><strong>Valor da Operação:</strong> R$ {endividamento.valor_operacao:,.2f}</li>' if endividamento.valor_operacao else ''}
                <li><strong>Valor Total Pendente:</strong> R$ {valor_total_pendente:,.2f}</li>
                <li><strong>Pessoas Vinculadas:</strong> {', '.join(pessoas_nomes)}</li>
            </ul>
            <p>Este é um e-mail automático do Sistema de Gestão Agrícola. Não responda a este e-mail.<br>
            Data de envio: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
        </body>
        </html>
        """
        return assunto, corpo

    def _preparar_mensagem_whatsapp(self, endividamento, tipo_notificacao):
        dias = self.INTERVALOS_NOTIFICACAO[tipo_notificacao]
        if dias >= 30:
            if dias == 180:
                periodo = "6 meses"
            elif dias == 90:
                periodo = "3 meses"
            else:
                periodo = f"{dias} dias"
        else:
            periodo = f"{dias} dia{'s' if dias > 1 else ''}"
        valor_total_pendente = sum(
            parcela.valor for parcela in endividamento.parcelas 
            if not parcela.pago
        )
        pessoas_nomes = [pessoa.nome for pessoa in endividamento.pessoas]
        mensagem = (
            f"🚨 *Lembrete de Endividamento*\n"
            f"Vencimento em {periodo}\n"
            f"Banco: {endividamento.banco}\n"
            f"Número da Proposta: {endividamento.numero_proposta}\n"
            f"Vencimento: {endividamento.data_vencimento_final.strftime('%d/%m/%Y')}\n"
            f"Taxa de Juros: {endividamento.taxa_juros}% {'a.a.' if endividamento.tipo_taxa_juros == 'ano' else 'a.m.'}\n"
            f"{'Valor da Operação: R$ ' + format(endividamento.valor_operacao, ',.2f') if endividamento.valor_operacao else ''}\n"
            f"Valor Total Pendente: R$ {valor_total_pendente:,.2f}\n"
            f"Pessoas: {', '.join(pessoas_nomes)}\n"
            f"Não responda a esta mensagem. Sistema Gestão Agrícola."
        )
        return mensagem

    def _registrar_historico(self, endividamento_id, tipo_notificacao, emails, whatsapps, sucesso, erro_mensagem=None):
        try:
            historico = HistoricoNotificacao(
                endividamento_id=endividamento_id,
                tipo_notificacao=tipo_notificacao,
                emails_enviados=json.dumps(emails),
                whatsapps_enviados=json.dumps(whatsapps),
                sucesso=sucesso,
                erro_mensagem=erro_mensagem
            )
            db.session.add(historico)
            db.session.commit()
        except Exception as e:
            logger.error(f"Erro ao registrar histórico de notificação: {str(e)}")
            db.session.rollback()