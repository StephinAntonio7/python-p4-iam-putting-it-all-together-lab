"""empty message

Revision ID: 5f2d775ed14c
Revises: 7bd1aafd03f5
Create Date: 2024-05-24 14:05:30.245275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f2d775ed14c'
down_revision = '7bd1aafd03f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('instructions',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_constraint('fk_recipes_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_password_hash', sa.String(), nullable=True))
        batch_op.drop_column('_hashed_password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_hashed_password', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('_password_hash')

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('fk_recipes_user_id_users', 'users', ['user_id'], ['id'])
        batch_op.alter_column('instructions',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###