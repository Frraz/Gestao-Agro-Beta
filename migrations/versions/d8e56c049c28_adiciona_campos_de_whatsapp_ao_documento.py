"""Adiciona campos de WhatsApp ao documento

Revision ID: d8e56c049c28
Revises: 98c49d7f246d
Create Date: 2025-06-18 22:43:09.137859

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd8e56c049c28'
down_revision = '98c49d7f246d'
branch_labels = None
depends_on = None

def upgrade():
    # As colunas já existem, não é necessário adicionar novamente!
    pass

def downgrade():
    with op.batch_alter_table('documento', schema=None) as batch_op:
        batch_op.drop_column('notificar_whatsapp')
        batch_op.drop_column('whatsapps_notificacao')