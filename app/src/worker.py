import re
import asyncio
import os
import random
from sqlalchemy import text
from src.database import engine, AsyncSessionLocal # Using our engine

init_mass = 100.0 # If database is empty

async def get_last_mass():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT mass FROM observations ORDER BY id DESC LIMIT 1")
        )
        row = result.fetchone()
        if row:
                match = re.search(r"(\d+\.\d+)", row[0])
                if match:
                        return float(match.group(1))
        return init_mass

async def run_worker():
    mass = await get_last_mass()
    print(f"Worker started, observing Phoenix A...")
    print(f"Worker started with mass: {mass}")


    while True:
            try:
                mass += random.uniform(0.00000000001, 0.00000000009) # Accreation
                mass -= random.uniform(0.000000000001,0.0000000000001) # Hawking radiation
                mass = round(mass, 18)
                data = f"Mass is now {mass:.18f} solar masses"
                async with engine.begin() as conn:
                    await conn.execute(
                            text("INSERT INTO observations (mass) VALUES (:mass_value)"),
                            {"mass_value": data}
                    )
                print(f"Recorded: {data}")
            except Exception as e:
                print(f"Worker Error: {e}")

            await asyncio.sleep(15)

if __name__ == "__main__":
        asyncio.run(run_worker())
