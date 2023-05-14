# migration.py
import os
from pathlib import Path

import alembic

from alembic.config import Config

from app.config import IS_LOCAL

def check_for_changes_and_migrate():
    api_dir = Path(__file__).parent / "app/api"
    db_files = list(api_dir.rglob('db.py'))
    if not db_files:
        print("No db.py files found. Skipping migrations...")
        return False
    latest_db_modification_time = max(os.path.getmtime(db_file) for db_file in db_files)

    migrations_dir = Path(__file__).parent / "alembic" / "versions"

    migration_files = list(migrations_dir.glob("*.py"))

    if not migration_files:
        print("No migration files found. This is the first migration.")
        return True
    else:
        latest_migration_modification_time = max(os.path.getmtime(migration_file) for migration_file in migration_files)
        if latest_db_modification_time > latest_migration_modification_time:
            return True
        else:
            print("No changes detected in db.py files. Skipping migrations...")
            return False


def run_migrations():
    if check_for_changes_and_migrate():
        try:
            alembic_args = [
                '--raiseerr',
                'revision',
                '--autogenerate',
                '-m',
                'Auto-generated migration'
            ]
            alembic.config.main(argv=alembic_args)

            alembic_args = [
                '--raiseerr',
                'upgrade',
                'head'
            ]
            alembic.config.main(argv=alembic_args)
            return True
        except Exception as e:
            print( e)
            pass


