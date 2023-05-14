# app/app.py
from fastapi import FastAPI

from app.core.database import db
from app.core.init import init
from app.core.security import setup_security

from app.core.routers import setup_routers


app = FastAPI()
setup_security(app)

setup_routers(app)

# setup security

# app/app.py
@app.on_event("startup")
async def on_startup():
    await init(app)


@app.on_event("shutdown")
async def shutdown():
    await db.close()
