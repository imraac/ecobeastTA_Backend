"""Added detailed safari fields

Revision ID: 880fa5bf85c3
Revises: 77ecc5ff54c9
Create Date: 2025-05-11 23:53:42.641810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '880fa5bf85c3'
down_revision = '77ecc5ff54c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('safari_package', schema=None) as batch_op:
        batch_op.add_column(sa.Column('overview', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('day_by_day', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('rates', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('inclusions', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('getting_there', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('offered_by', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('tour_features', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('route_details', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('safari_package', schema=None) as batch_op:
        batch_op.drop_column('route_details')
        batch_op.drop_column('tour_features')
        batch_op.drop_column('offered_by')
        batch_op.drop_column('getting_there')
        batch_op.drop_column('inclusions')
        batch_op.drop_column('rates')
        batch_op.drop_column('day_by_day')
        batch_op.drop_column('overview')

    # ### end Alembic commands ###
