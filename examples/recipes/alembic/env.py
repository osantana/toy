import sys
from logging.config import fileConfig

from alembic import context
from prettyconf import config as pretty_config
from sqlalchemy import create_engine, pool

sys.path.append('')
from recipes.database import db  # NOQA

# noinspection PyUnresolvedReferences
from recipes.models import Recipe, Rating, User  # NOQA

url = pretty_config('DATABASE_URL')

config = context.config
fileConfig(config.config_file_name)
target_metadata = db.Model.metadata


def run_migrations_offline():
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
