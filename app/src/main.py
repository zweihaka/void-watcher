import os
import logging
from fastapi import FastAPI
from .database import engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from pydantic import BaseModel
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Reading env variables
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

#The string for connecting
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

#Creating engine
engine = create_async_engine(DATABASE_URL, echo=True)

class StatusResponse(BaseModel):
    status: str
    database: str
    node: str

@app.get("/", response_model=StatusResponse)
async def home():
    try:
    # Simple SQL-request to check connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    return {
    "status": "Welcome home",
    "database": db_status,
    "node": "Debian-Production"
}

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    try:
    # Simple SQL-request to check connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            db_status = "Connected"
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        db_status = f"Error: {str(e)}"

    return {
    "status": "Void-Watcher online",
    "database": db_status,
    "node": "Debian-Production"
}
