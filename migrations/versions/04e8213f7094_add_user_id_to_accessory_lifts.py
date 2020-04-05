"""Add user id to accessory lifts

Revision ID: 04e8213f7094
Revises: 6ffcd15e8d40
Create Date: 2020-04-04 18:13:15.667029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e8213f7094'
down_revision = '6ffcd15e8d40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accessory_lifts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'accessory_lifts', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'accessory_lifts', type_='foreignkey')
    op.drop_column('accessory_lifts', 'user_id')
    # ### end Alembic commands ###