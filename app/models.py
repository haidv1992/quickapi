#app/models.py
import asyncio
import importlib
from sqlalchemy import MetaData
from pathlib import Path
from app.database import db

# Combine metadata from all Base objects
combined_metadata = MetaData()

api_dir = Path(__file__).parent.parent / "api"
db_files = list(api_dir.rglob('db.py'))
# print(f"Found {len(db_files)} db.py files")

async def create_tables_async():
    for db_file in db_files:
        relative_path = db_file.parent.relative_to(Path(__file__).parent.parent)
        module_path = str(relative_path).replace("/", ".")
        module = importlib.import_module(f"{module_path}.db")
        base = module.Base

        base.metadata.schema = None  # Remove the schema if it's not needed
        base.metadata.bind = None

        for table in base.metadata.tables.values():
            combined_metadata._add_table(table.name, table.schema, table)

try:
    asyncio.run(create_tables_async())  # Call the async function to create tables
    # print("Completed processing.")
except Exception as e:
    print(f"Error: {e}")
    print("Continuing execution...")
