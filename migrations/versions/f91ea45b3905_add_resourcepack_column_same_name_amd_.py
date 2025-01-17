"""add ResourcePack Column same_name amd index

Revision ID: f91ea45b3905
Revises: 7790d20dde04
Create Date: 2019-03-13 11:41:44.098637

"""

# revision identifiers, used by Alembic.
revision = 'f91ea45b3905'
down_revision = '7790d20dde04'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource_pack', sa.Column('同名文件', sa.String(), nullable=True))
    op.add_column('resource_pack', sa.Column('文件下标', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_resource_pack_同名文件'), 'resource_pack', ['同名文件'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_resource_pack_同名文件'), table_name='resource_pack')
    op.drop_column('resource_pack', '文件下标')
    op.drop_column('resource_pack', '同名文件')
    # ### end Alembic commands ###
