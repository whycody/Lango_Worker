# worker.py
import asyncio
import datetime
from db import db

async def run_worker_loop():
    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        print(f"[Worker] Tick at {now.isoformat()}")

        user_count = db.users.count_documents({})
        print(f"[Worker] Users in DB: {user_count}")

        await asyncio.sleep(1)