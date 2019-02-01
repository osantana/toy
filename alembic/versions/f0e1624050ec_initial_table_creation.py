import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import TSVectorType

from alembic import op

revision = 'f0e1624050ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recipes',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('prep_time', sa.Interval(), nullable=False),
                    sa.Column('difficulty', sa.SmallInteger(), nullable=False),
                    sa.Column('vegetarian', sa.Boolean(), nullable=False),
                    sa.Column('search', TSVectorType(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_recipes_name'), 'recipes', ['name'], unique=False)
    op.create_index('ix_recipes_search', 'recipes', ['search'], unique=False, postgresql_using='gin')
    op.create_table('users',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('password', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('ratings',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('recipe_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('value', sa.SmallInteger(), nullable=False),
                    sa.ForeignKeyConstraint(('recipe_id',), ['recipes.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('ratings')
    op.drop_table('users')
    op.drop_index('ix_recipes_search', table_name='recipes')
    op.drop_index(op.f('ix_recipes_name'), table_name='recipes')
    op.drop_table('recipes')
