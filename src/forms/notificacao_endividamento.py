# /src/forms/notificacao_endividamento.py

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
import re

class NotificacaoEndividamentoForm(FlaskForm):
    emails = TextAreaField(
        'E-mails para Notificação',
        validators=[DataRequired(), Length(max=2000)],
        description='Digite um e-mail por linha.'
    )
    whatsapps = TextAreaField(
        'WhatsApps para Notificação',
        description='Digite um número por linha, no formato internacional: +5511912345678'
    )
    ativo = BooleanField('Ativo', default=True)
    notificar_whatsapp = BooleanField('Notificar por WhatsApp', default=False)

    def validate_emails(self, field):
        from wtforms.validators import ValidationError
        if not field.data:
            return
        emails = [email.strip() for email in field.data.split('\n') if email.strip()]
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        for email in emails:
            if not email_pattern.match(email):
                raise ValidationError(f'E-mail inválido: {email}')

    def validate_whatsapps(self, field):
        from wtforms.validators import ValidationError
        if not field.data:
            return
        whats = [w.strip() for w in field.data.split('\n') if w.strip()]
        pattern = re.compile(r'^\+\d{10,15}$')
        for numero in whats:
            if not pattern.match(numero):
                raise ValidationError(f'WhatsApp inválido: {numero}')