"""Add is_archived column to SafariPackage

Revision ID: 5cb34c6c2b1f
Revises: c0444d333b27
Create Date: 2025-05-25 18:44:48.614052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb34c6c2b1f'
down_revision = 'c0444d333b27'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('safari_package', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))

def downgrade():
    with op.batch_alter_table('safari_package', schema=None) as batch_op:
        batch_op.drop_column('is_archived')
