# security.py
import ast
from pathlib import Path
from typing import Generic, TypeVar, Optional
from fastapi import HTTPException, Request, Depends
from pydantic.generics import GenericModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from app.api.user.users import get_user_role
from app.config import ROLES_HIERARCHY

DataT = TypeVar('DataT')


class ResponseModelStatus(GenericModel, Generic[DataT]):
    status: bool
    message: str
    data: Optional[DataT]


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail


# Define a function to get the permissions dictionary
def get_permissions_dict():
    permissions_py_path = Path(__file__).parent.parent / "core/permissions.py"
    with open(permissions_py_path, 'r') as f:
        module = ast.parse(f.read())
    return ast.literal_eval(module.body[0].value)


# Define a decorator to protect your routes
def has_permission(
        request: Request,
        current_user_role: str = Depends(get_user_role)):
    route_name = request.scope.get("endpoint").__name__
    permissions_dict = get_permissions_dict()
    # Check if the role is valid
    if current_user_role not in ROLES_HIERARCHY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role")
    # Check if the function is allowed for the role and its sub-roles
    allowed_roles = [current_user_role] + ROLES_HIERARCHY[current_user_role]
    if not any(permissions_dict.get(role, {}).get(route_name, True) for role in allowed_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")
    return True

def setup_security(app: FastAPI):
    # Configure CORS
    origins = ["http://localhost:3000"]  # Add your own origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": False,
                "message": exc.detail,
                "error": str(exc)
            },
        )
