# /migrations/versions/2c700239e98a_unifica_tabelas_de_auditoria_e_usuario.py

"""Unifica tabelas de auditoria e usuario

Revision ID: 2c700239e98a
Revises: 
Create Date: 2025-06-20 00:16:47.067802

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2c700239e98a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Cria tabela usuario, pois auditoria depende da FK usuario.id
    op.create_table(
        'usuario',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(length=150), nullable=False)
        # Adicione outros campos necessários do usuário!
    )

    # Cria a tabela auditoria já com o modelo novo, pois não há nada anterior no banco
    op.create_table(
        'auditoria',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('usuario_id', sa.Integer, sa.ForeignKey('usuario.id'), nullable=True),
        sa.Column('username', sa.String(length=150), nullable=True),
        sa.Column('acao', sa.String(length=100), nullable=False),
        sa.Column('entidade', sa.String(length=100), nullable=True),
        sa.Column('valor_anterior', sa.Text(), nullable=True),
        sa.Column('valor_novo', sa.Text(), nullable=True),
        sa.Column('detalhes', sa.Text(), nullable=True),
        sa.Column('ip', sa.String(length=45), nullable=True),
        sa.Column('data_hora', sa.DateTime(), nullable=False)
    )

    # Caso queira garantir remoção de tabelas antigas (opcional)
    try:
        op.drop_table('audit_log')
    except Exception:
        pass

    try:
        op.drop_table('user')
    except Exception:
        pass

def downgrade():
    op.drop_table('auditoria')
    op.drop_table('usuario')