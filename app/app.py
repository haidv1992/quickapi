# app/app.py

from fastapi import FastAPI, Depends, Request
from starlette.responses import JSONResponse

from api.user.db import User
from api.user.schemas import UserRead, UserCreate, UserUpdate
from api.user.users import fastapi_users, auth_backend, current_active_user
from app.database import db
from app.quickapi.core.model import CustomException

from app.routers import setup_routers
from migration import run_migrations

app = FastAPI()


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "message": exc.detail,
            "error": str(exc)
        },
    )


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

setup_routers(app)

# app/app.py
@app.on_event("startup")
async def on_startup():
    await db.init()
    run_migrations()


@app.on_event("shutdown")
async def shutdown():
    await db.close()
