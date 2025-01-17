"""init migrate

Revision ID: 9cd3fc83b337
Revises: None
Create Date: 2019-03-08 17:12:10.588570

"""

# revision identifiers, used by Alembic.
revision = '9cd3fc83b337'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_info',
    sa.Column('编号', sa.Integer(), nullable=False),
    sa.Column('文件名', sa.String(), nullable=False),
    sa.Column('路径', sa.String(), nullable=True),
    sa.Column('大小', sa.Integer(), nullable=True),
    sa.Column('f_md5', sa.String(), nullable=True),
    sa.Column('添加时间', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('\u7f16\u53f7')
    )
    op.create_table('resource_pack',
    sa.Column('编号', sa.Integer(), nullable=False),
    sa.Column('f_uid', sa.String(), nullable=False),
    sa.Column('名称', sa.String(), nullable=False),
    sa.Column('资源地址', sa.String(), nullable=True),
    sa.Column('封面图', sa.String(), nullable=True),
    sa.Column('添加时间', sa.DateTime(), nullable=True),
    sa.Column('修改时间', sa.DateTime(), nullable=True),
    sa.Column('f_file_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['f_file_id'], ['file_info.编号'], ),
    sa.PrimaryKeyConstraint('\u7f16\u53f7')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resource_pack')
    op.drop_table('file_info')
    # ### end Alembic commands ###
