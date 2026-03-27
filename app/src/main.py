from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/api/status")
async def get_status():

    return {
    "status": "Void-Watcher online",
    "timestamp": datetime.now().isoformat(),
    "node": "Debian-Production"
}
