from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from src.models import Observation
from src.database import AsyncSessionLocal

async def ping_db(db: AsyncSession):
    try:
        await db.execute(text("SELECT 1"))
        return "Connected"
    except Exception as e:
        return f"Error: {e}"

async def get_history(db: AsyncSessionLocal, limit: int = 20):
    query = text("SELECT * FROM observations ORDER BY id DESC LIMIT :limit")
    result = await db.execute(query, {"limit": limit})
    return [dict(row) for row in result.mappings()]


async def reset_mass(db: AsyncSessionLocal):
    await db.execute(text("TRUNCATE TABLE observations"))
    await db.commit()
