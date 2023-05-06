# migrations/env.py
import argparse
import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.models import combined_metadata

# Set target_metadata to the combined_metadata object
target_metadata = combined_metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

from app.config import Config

config.set_main_option("sqlalchemy.url", Config.DB_CONFIG)

class NoMigrationsRequired(Exception):
    pass

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def check_for_changes_and_migrate():

    api_dir = Path(__file__).parent.parent / "api"
    db_files = list(api_dir.rglob('db.py'))
    if not db_files:
        print("No db.py files found. Skipping migrations...")
        return False
    latest_db_modification_time = max(os.path.getmtime(db_file) for db_file in db_files)

    migrations_dir = Path(__file__).parent / "versions"

    migration_files = list(migrations_dir.glob("*.py"))

    if not migration_files:
        print("No migration files found. This is the first migration.")
        return True
    else:
        latest_migration_modification_time = max(os.path.getmtime(migration_file) for migration_file in migration_files)
        if latest_db_modification_time > latest_migration_modification_time:
            migration_context = context.configure()
            diff = migration_context.get_changes(target_metadata)
            if not diff:
                print("No actual changes detected in db.py files. Skipping migration.")
                raise NoMigrationsRequired()
            print("Changes detected in db.py files. Running migrations...")
            return True
        else:
            print("No changes detected in db.py files. Skipping migrations...")
            raise NoMigrationsRequired()


if context.is_offline_mode():
    run_migrations_offline()
# elif "--autogenerate" in sys.argv or os.environ.get('AUTO_GENERATE_MIGRATE') == '1':
elif os.environ.get('AUTO_GENERATE_MIGRATE') == '1':
    if check_for_changes_and_migrate():
        asyncio.run(run_migrations_online())
else:
    asyncio.run(run_migrations_online())
