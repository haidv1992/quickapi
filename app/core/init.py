# app/core/init.py
import ast
from pathlib import Path
from pprint import pformat

import astunparse
from fastapi import FastAPI

from app.config import IS_LOCAL, ROLES_HIERARCHY
from app.core.database import db
from migration import run_migrations


def update_permissions_py(app: FastAPI):
    # Get the current permissions.
    permissions_py_path = Path(__file__).parent.parent / "core/permissions.py"
    with open(permissions_py_path, 'r') as f:
        module = ast.parse(f.read())
    permissions_dict = ast.literal_eval(module.body[0].value)

    # Exclude these routes
    exclude_apis = {"redoc_html", "swagger_ui_html", "swagger_ui_redirect", "openapi"}
    # Exclude routes with these prefixes
    exclude_prefixes = {"auth:", "reset:", "verify:", "register:", "users:", "verify:"}

    # Initialize the permissions for each role.
    for role in ROLES_HIERARCHY:
        if role not in permissions_dict:
            permissions_dict[role] = {}

    # Update the permissions based on the current API routes.
    for route in app.routes:
        route_name = route.name
        if route_name in exclude_apis or any(route_name.startswith(prefix) for prefix in exclude_prefixes):
            continue
        for role in ROLES_HIERARCHY:
            if route_name not in permissions_dict[role]:
                permissions_dict[role][route_name] = False

    # Write the updated permissions to the Python file.
    with open(permissions_py_path, 'w') as f:
        f.write("permissions = " + pformat(permissions_dict))



async def init(app):
    await db.init()
    if IS_LOCAL:
        run_migrations()
        update_permissions_py(app)
