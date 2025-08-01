# alembic/versions/0001_create_tables.py
"""
Cria tabelas de usuários e tarefas
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import uuid

# Revisão Alembic
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('senha_hash', sa.String(), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('now()'))
    )

    op.create_table(
        'tarefas',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('titulo', sa.String(), nullable=False),
        sa.Column('descricao', sa.Text()),
        sa.Column('data_vencimento', sa.DateTime()),
        sa.Column('prioridade', sa.Enum('baixa', 'media', 'alta', name='prioridadeenum'), nullable=False, server_default='media'),
        sa.Column('status', sa.Enum('pendente', 'em_andamento', 'concluida', name='statusenum'), nullable=False, server_default='pendente'),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('dono_id', pg.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False)
    )

def downgrade():
    op.drop_table('tarefas')
    op.drop_table('usuarios')
    op.execute("DROP TYPE IF EXISTS prioridadeenum")
    op.execute("DROP TYPE IF EXISTS statusenum")
