# app/database.py
import asyncio
import os

from alembic.command import revision, upgrade
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import Config
from alembic.config import Config as AlembicConfig

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(
            Config.DB_CONFIG,
            future=True,
            echo=True,
        )
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def migrate(self):
        alembic_config = AlembicConfig("alembic.ini")

        def do_revision():
            revision(alembic_config, autogenerate=True, message="Auto-generated migration")

        def do_upgrade(revision):
            upgrade(alembic_config, revision)

        loop = asyncio.get_event_loop()
        try:
            os.environ['AUTO_GENERATE_MIGRATE'] = '1'
            await loop.run_in_executor(None, do_revision)

        except Exception as e:
            print(f"Error do_revision: {e}")
            print("Continuing execution...")

        try:
            os.environ['AUTO_GENERATE_MIGRATE'] = '0'  # Reset the environment variable
            await loop.run_in_executor(None, do_upgrade, "head")
        except Exception as e:
            print(f"Error do_upgrade: {e}")
            print("Continuing execution...")



db = AsyncDatabaseSession()
