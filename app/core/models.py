# app/models.py
import importlib
from sqlalchemy import MetaData
from pathlib import Path

combined_metadata = MetaData()

api_dir = Path(__file__).parent.parent / "api"
db_files = list(api_dir.rglob('db.py'))


def create_tables_async():
    for db_file in db_files:
        relative_path = db_file.parent.relative_to(Path(__file__).parent.parent)
        module_path = "app." + str(relative_path).replace("/", ".")
        module = importlib.import_module(f"{module_path}.db")
        base = module.Base

        base.metadata.schema = None  # Remove the schema if it's not needed
        base.metadata.bind = None

        for table in base.metadata.tables.values():
            combined_metadata._add_table(table.name, table.schema, table)


create_tables_async()
