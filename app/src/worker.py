import asyncio
import random
import re
from sqlalchemy import text
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
            mass = await get_last_mass()
            mass += random.uniform(0.00000000001, 0.00000000009)
            mass -= random.uniform(0.000000000001, 0.000000000005)
            mass = round(mass, 15) 
            
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
