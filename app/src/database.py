import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

def get_secret(env_name, default=None):
    val = os.getenv(env_name, default)
    if val and os.path.isfile(val):
            with open(val, 'r') as f:
                return f.read().strip()
    return val

DB_HOST = get_secret("DB_HOST", "db")   
DB_USER = get_secret("DB_USER")
DB_PASS = get_secret("DB_PASS")
DB_NAME = get_secret("DB_NAME")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(DB_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
