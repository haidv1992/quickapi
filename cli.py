#cli.py
import argparse
import os
from datetime import datetime

API_DIR = "api"

def generate_api(api_name):
    global api_prefix
    api_prefix = f"{api_name}s"
    api_path = os.path.join(API_DIR, api_name)
    os.makedirs(api_path, exist_ok=True)

    generate_db_file(api_path, api_name)
    generate_router_file(api_path)
    generate_model_file(api_path)


def generate_db_file(api_path, api_name):
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


def generate_router_file(api_path):
    router_file_content = f'''from fastapi import APIRouter

router = APIRouter()

@router.get("/{api_prefix}", tags=["{api_prefix}"])
async def find():
    return []

@router.get("/{api_prefix}/{{id}}/", tags=["{api_prefix}"])
async def findOne(id: int):
    return {{}}

@router.post("/{api_prefix}", tags=["{api_prefix}"])
async def create():
    return {{}}

@router.put("/{api_prefix}/{{id}}", tags=["{api_prefix}"])
async def update(id: int):
    return {{}}

@router.delete("/{api_prefix}/{{id}}", tags=["{api_prefix}"])
async def delete(id: int):
    return {{}}
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


def main():
    parser = argparse.ArgumentParser(description="FastAPI CLI")
    parser.add_argument("command", choices=["make:api"])

    args = parser.parse_args()

    if args.command == "make:api":
        api_name = input("Please enter the name of the API: ")
        generate_api(api_name)


if __name__ == "__main__":
    main()
