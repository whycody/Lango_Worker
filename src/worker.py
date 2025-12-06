import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.send_notifications import send_notifications
from db import db

async def run_worker_loop():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(send_notifications, 'cron', args=[db], second='*')

    scheduler.start()

    while True:
        await asyncio.sleep(60)