from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, SelectMultipleField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Optional, ValidationError
import re

TIPOS_DOCUMENTO = [
    ('Certidões', 'Certidões'),
    ('Contratos', 'Contratos'),
    ('Documentos da Área', 'Documentos da Área'),
    ('Outros', 'Outros')
]

TIPOS_ENTIDADE = [
    ('Fazenda/Área', 'Fazenda/Área'),
    ('Pessoa', 'Pessoa')
]

# Prazos padrão para notificação
PRAZOS_NOTIFICACAO = [
    (30, '30 dias antes'),
    (15, '15 dias antes'),
    (7, '7 dias antes'),
    (3, '3 dias antes'),
    (1, '1 dia antes')
]

def validate_emails(form, field):
    if not field.data:
        return
    # Permite e-mails separados por vírgula ou por linha
    emails = [email.strip() for email in re.split(r'[\n,]+', field.data) if email.strip()]
    pattern = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
    for email in emails:
        if not pattern.match(email):
            raise ValidationError(f'E-mail inválido: {email}')

def validate_whatsapps(form, field):
    if not field.data:
        return
    # Permite números separados por vírgula ou por linha
    whatsapps = [num.strip() for num in re.split(r'[\n,]+', field.data) if num.strip()]
    pattern = re.compile(r'^\+\d{10,15}$')
    for num in whatsapps:
        if not pattern.match(num):
            raise ValidationError(f'Número de WhatsApp inválido (use formato internacional, ex: +5511999999999): {num}')

class DocumentoForm(FlaskForm):
    nome = StringField('Nome do Documento', [DataRequired(), Length(max=100)])
    tipo = SelectField('Tipo', choices=TIPOS_DOCUMENTO, validators=[DataRequired()])
    tipo_personalizado = StringField('Tipo Personalizado', [Optional(), Length(max=100)])
    data_emissao = DateField('Data de Emissão', format='%Y-%m-%d', validators=[DataRequired()])
    data_vencimento = DateField('Data de Vencimento', format='%Y-%m-%d', validators=[Optional()])
    tipo_entidade = SelectField('Tipo de Entidade', choices=TIPOS_ENTIDADE, validators=[DataRequired()])
    # Relacionamento: fazenda/pessoa será tratado na view

    emails_notificacao = TextAreaField(
        'E-mails para Notificação',
        description='Digite um e-mail por linha ou separados por vírgula.',
        validators=[Optional(), Length(max=2000), validate_emails]
    )
    whatsapps_notificacao = TextAreaField(
        'WhatsApps para Notificação',
        description='Digite um número por linha ou separados por vírgula, no formato internacional (+5511912345678).',
        validators=[Optional(), Length(max=2000), validate_whatsapps]
    )
    notificar_whatsapp = BooleanField('Notificar por WhatsApp', default=False)
    prazos_notificacao = SelectMultipleField(
        'Prazos de Notificação',
        choices=[(str(p[0]), p[1]) for p in PRAZOS_NOTIFICACAO],
        coerce=str,
        validators=[Optional()]
    )