"""Upgraded Character model and created 1-to-many relations

Revision ID: b04bdbfd7639
Revises: 62972f64b697
Create Date: 2024-12-28 23:07:52.456172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b04bdbfd7639'
down_revision = '62972f64b697'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=5000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=5000),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###
