import time
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, AsyncSessionLocal
from sqlalchemy import text
from . import crud
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

last_reset_time = 0
COOLDOWN = 60

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/api/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    status = await crud.ping_db(db)
    return {"status": "Online", "db": status}


@app.get("/api/history")
async def get_history(db: AsyncSession = Depends(get_db)):
    mass = await crud.get_history(db)
    return {"mass_value": mass}

@app.post("/api/reset")
async def reset_data(db: AsyncSession = Depends(get_db)):
    global last_reset_time
    now = time.time()
    if now - last_reset_time < COOLDOWN:
        raise HTTPException(status_code=429, detail ="Too soon, wait before next reset.")
    last_reset_time = now

    await crud.reset_mass(db)

    return {"status": "Database reseted to singularity"}
