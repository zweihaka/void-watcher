from fastapi import FastAPI
from .database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/api/status")
async def get_status():
    try:
        # Database ping
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {e}"

    return {
        "status": "Void-Watcher online",
        "database": db_status
    }
