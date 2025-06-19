# /src/models/notificacao_endividamento.py

from src.models.db import db
from datetime import datetime

class NotificacaoEndividamento(db.Model):
    __tablename__ = 'notificacao_endividamento'
    
    id = db.Column(db.Integer, primary_key=True)
    endividamento_id = db.Column(db.Integer, db.ForeignKey('endividamento.id'), nullable=False)
    emails = db.Column(db.Text, nullable=False)  # JSON string
    whatsapps = db.Column(db.Text, nullable=True)  # JSON string de números
    ativo = db.Column(db.Boolean, default=True)
    notificar_whatsapp = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    endividamento = db.relationship('Endividamento', back_populates='notificacoes')

    def __repr__(self):
        return f'<NotificacaoEndividamento {self.endividamento_id}>'
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'endividamento_id': self.endividamento_id,
            'emails': json.loads(self.emails) if self.emails else [],
            'whatsapps': json.loads(self.whatsapps) if self.whatsapps else [],
            'ativo': self.ativo,
            'notificar_whatsapp': self.notificar_whatsapp,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class HistoricoNotificacao(db.Model):
    __tablename__ = 'historico_notificacao'
    
    id = db.Column(db.Integer, primary_key=True)
    endividamento_id = db.Column(db.Integer, db.ForeignKey('endividamento.id'), nullable=False)
    tipo_notificacao = db.Column(db.String(20), nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    emails_enviados = db.Column(db.Text, nullable=False)  # JSON string
    whatsapps_enviados = db.Column(db.Text, nullable=True)  # JSON string
    sucesso = db.Column(db.Boolean, default=True)
    erro_mensagem = db.Column(db.Text, nullable=True)
    
    endividamento = db.relationship('Endividamento')
    
    def __repr__(self):
        return f'<HistoricoNotificacao {self.endividamento_id} - {self.tipo_notificacao}>'
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'endividamento_id': self.endividamento_id,
            'tipo_notificacao': self.tipo_notificacao,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'emails_enviados': json.loads(self.emails_enviados) if self.emails_enviados else [],
            'whatsapps_enviados': json.loads(self.whatsapps_enviados) if self.whatsapps_enviados else [],
            'sucesso': self.sucesso,
            'erro_mensagem': self.erro_mensagem
        }