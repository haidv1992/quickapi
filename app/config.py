#app/config.py
import os
from dotenv import load_dotenv
load_dotenv()

APP_ENV = os.getenv("APP_ENV")
IS_LOCAL = APP_ENV == 'local'
SECRET_KEY = os.getenv("SECRET_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_POST = os.getenv("DB_POST")
TIME_ZONE = os.getenv("TIME_ZONE")
DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_POST}/{DB_NAME}"
DB_URL_PS = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_POST}/{DB_NAME}"
