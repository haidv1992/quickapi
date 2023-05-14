#app/core/database.py
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DB_CONFIG, TIME_ZONE

Base = declarative_base()

logger = logging.getLogger(__name__)


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine(
            DB_CONFIG,
            future=True,
            echo=True,
            connect_args={"server_settings": {"timezone": TIME_ZONE}}
        )
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    @asynccontextmanager
    async def get_session(self):
        if self._session is None:
            await self.init()
        async with self._session() as session:
            yield session

    async def close(self):
        await self._engine.dispose()


db = AsyncDatabaseSession()
