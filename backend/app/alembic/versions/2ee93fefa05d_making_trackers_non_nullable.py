"""making trackers non nullable

Revision ID: 2ee93fefa05d
Revises: 66f3099714c2
Create Date: 2023-11-30 10:00:09.184056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ee93fefa05d'
down_revision = '66f3099714c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'uploads_counter',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user', 'queries_counter',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'queries_counter',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user', 'uploads_counter',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
