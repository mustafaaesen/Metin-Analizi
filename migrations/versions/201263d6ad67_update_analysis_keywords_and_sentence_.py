"""update analysis keywords and sentence sentiment

Revision ID: 201263d6ad67
Revises: 4b97a484724d
Create Date: 2026-01-04 12:25:44.303319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '201263d6ad67'
down_revision = '4b97a484724d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('analyses', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('sentiment_sentences', sa.JSON(), nullable=True)
        )
        batch_op.drop_column('keywords')
        batch_op.add_column(
            sa.Column('keywords', sa.JSON(), nullable=True)
        )

    # ### end Alembic commands ###


def upgrade():
    with op.batch_alter_table('analyses', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('sentiment_sentences', sa.JSON(), nullable=True)
        )
        batch_op.drop_column('keywords')
        batch_op.add_column(
            sa.Column('keywords', sa.JSON(), nullable=True)
        )

    # ### end Alembic commands ###
