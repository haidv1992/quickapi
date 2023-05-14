# app/api/user/db.py
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ROLES_HIERARCHY
from app.core.database import db
from app.core.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    role = Column(String, default='user', nullable=False)
    CheckConstraint(
        Column('role').in_(list(ROLES_HIERARCHY.keys())),
        name='check_valid_role'
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
