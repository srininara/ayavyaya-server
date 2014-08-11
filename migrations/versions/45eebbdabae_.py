"""empty message

Revision ID: 45eebbdabae
Revises: 1015e396890
Create Date: 2014-08-09 11:54:12.504657

"""

# revision identifiers, used by Alembic.
revision = '45eebbdabae'
down_revision = '1015e396890'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expenses_tags',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('expense_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('tags')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('tag_id', sa.INTEGER(), nullable=True),
    sa.Column('expense_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('expenses_tags')
    ### end Alembic commands ###
