# cli.py
import argparse
import asyncio
import contextlib
import os
from fastapi_users.exceptions import UserAlreadyExists

from app.api.user.db import get_user_db
from app.api.user.schemas import UserCreate
from app.api.user.users import get_user_manager
import click

from app.core.database import db

API_DIR = "app/api"


def generate_api(api_input):
    global api_name
    global api_prefix
    api_name = api_input
    api_prefix = f"{api_input}s"
    api_path = os.path.join(API_DIR, api_name)
    os.makedirs(api_path, exist_ok=True)

    generate_db_file(api_path)
    generate_controller_file(api_path)
    generate_router_file(api_path)
    generate_model_file(api_path)


def generate_db_file(api_path):
    db_file_content = f"""from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class {api_name.capitalize()}(Base):
    __tablename__ = "{api_prefix}"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
"""

    with open(os.path.join(api_path, "db.py"), "w") as db_file:
        db_file.write(db_file_content)


def generate_controller_file(api_path):
    controller_file_content = f'''from api.{api_name}.db import {api_name.capitalize()}
from app.quickapi.core.quickapi import QuickAPI

qa = QuickAPI()

async def find_{api_name}s(request):
    return await qa.find(table={api_name.capitalize()}, request=request)

async def find_{api_name}(id: int):
    return {{}}

async def create_{api_name}():
    return {{}}

async def update_{api_name}(id: int):
    return {{}}

async def delete_{api_name}(id: int):
    return {{}}
'''

    with open(os.path.join(api_path, "controller.py"), "w") as controller_file:
        controller_file.write(controller_file_content)


def generate_router_file(api_path):
    router_file_content = f'''from fastapi import APIRouter, Request
from .controller import (
    find_{api_name}s,
    find_{api_name},
    create_{api_name},
    update_{api_name},
    delete_{api_name},
)

router = APIRouter()

@router.get("/{api_prefix}", tags=["{api_prefix}"])
async def find(request: Request):
    return await find_{api_name}s(request)

@router.get("/{api_prefix}/{{id}}/", tags=["{api_prefix}"])
async def findOne(id: int):
    return await find_{api_name}(id)

@router.post("/{api_prefix}", tags=["{api_prefix}"])
async def create():
    return await create_{api_name}()

@router.patch("/{api_prefix}/{{id}}", tags=["{api_prefix}"])
async def update(id: int):
    return await update_{api_name}(id)

@router.delete("/{api_prefix}/{{id}}", tags=["{api_prefix}"])
async def delete(id: int):
    return await delete_{api_name}(id)
'''

    with open(os.path.join(api_path, "router.py"), "w") as router_file:
        router_file.write(router_file_content)


def generate_model_file(api_path):
    model_file_content = """class BaseModel:
    @classmethod
    def before_create(cls, *args, **kwargs):
        pass

    @classmethod
    def after_create(cls, *args, **kwargs):
        pass

    @classmethod
    def before_update(cls, *args, **kwargs):
        pass

    @classmethod
    def after_update(cls, *args, **kwargs):
        pass
"""

    with open(os.path.join(api_path, "model.py"), "w") as model_file:
        model_file.write(model_file_content)


async def create_user(email: str, password: str, is_superuser: bool = False):
    try:
        get_user_db_context = contextlib.asynccontextmanager(get_user_db)
        get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
        async with db.get_session() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    click.secho(f"User created success user_id: {user.id}", fg="green")
                    return user
    except UserAlreadyExists:
        click.secho(f"User {email} already exists", fg="yellow")


async def main():
    parser = argparse.ArgumentParser(description="FastAPI CLI")
    parser.add_argument("command", choices=["make:api", "make:user"])

    args = parser.parse_args()
    api_input = ""
    if args.command == "make:api":
        while not api_input:
            api_input = input("Please enter the name of the API: ")
        generate_api(api_input)

    elif args.command == "make:user":
        email = ""
        while not email:
            email = input(f"Please enter the email (default is admin@quickapi.com): ").strip()
            if not email:
                email = "admin@quickapi.com"

        password = ""
        while not password:
            password = input("Please enter the password (default is admin@123): ").strip()
            if not password:
                password = "admin@123"

        is_superuser = ""
        while is_superuser not in ["0", "1"]:
            is_superuser = input("Please enter the superuser 1/0 (default is 1): ").strip()
            if not is_superuser:
                is_superuser = "1"
        if is_superuser == "1":
            is_superuser = True
        else:
            is_superuser = False

        await create_user(email.strip(), password.strip(), is_superuser)


if __name__ == "__main__":
    asyncio.run(main())
