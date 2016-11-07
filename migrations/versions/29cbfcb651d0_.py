"""empty message

Revision ID: 29cbfcb651d0
Revises: 141a75cd647d
Create Date: 2016-11-06 16:04:09.584905

"""

# revision identifiers, used by Alembic.
revision = '29cbfcb651d0'
down_revision = '141a75cd647d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint("expenses_tags_id_unique",
                                "expenses_tags",
                                ["expense_id", "tag_id"])
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint("expenses_tags_id_unique",
                      "expenses_tags",
                      "unique")
    ### end Alembic commands ###
