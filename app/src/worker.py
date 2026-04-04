import asyncio
import random
import re
from sqlalchemy import text
# Используем абсолютный импорт для работы через python -m
from src.database import engine, AsyncSessionLocal

INITIAL_MASS = 100.0

async def get_last_mass():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                text("SELECT mass FROM observations ORDER BY id DESC LIMIT 1")
            )
            row = result.fetchone()
            if row and row[0]:
                val = str(row[0])
                # ХАК: Если в базе старый текст "Mass is now 100...", выцепляем только цифры
                # Если в базе уже чистое число - оно тоже пройдёт
                match = re.search(r"(\d+\.\d+)", val)
                if match:
                    return float(match.group(1))
                try:
                    return float(val)
                except ValueError:
                    return INITIAL_MASS
        except Exception as e:
            print(f"DB Read Error: {e}")
        return INITIAL_MASS

async def run_worker():
    print("SEARCHING FOR SINGULARITY...")
    
    while True:
        try:
            # 1. СИНХРОНИЗАЦИЯ (всегда берем актуальное из БД)
            mass = await get_last_mass()
            
            # 2. ВЫЧИСЛЕНИЯ (Accretion vs Hawking)
            mass += random.uniform(0.000000001, 0.000000009)
            mass -= random.uniform(0.0000000001, 0.0000000005)
            mass = round(mass, 15) # DOUBLE PRECISION в Postgres держит ~15-17 знаков
            
            # 3. ЗАПИСЬ (Только ЧИСЛО!)
            async with engine.begin() as conn:
                await conn.execute(
                    text("INSERT INTO observations (mass) VALUES (:m)"),
                    {"m": mass}
                )
            print(f"SUCCESS: PHOENIX A* MASS = {mass:.15f}")
            
        except Exception as e:
            print(f"CRITICAL WORKER LOOP ERROR: {e}")

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_worker())
