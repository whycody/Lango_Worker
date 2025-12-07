import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.send_notifications import send_notifications
from jobs.update_notification_times import update_notification_times
from db import db


async def run_worker_loop():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(send_notifications, 'cron', args=[db], minute='*')

    scheduler.add_job(update_notification_times, 'cron', args=[db], hour=3, minute=0, second=0)

    scheduler.start()

    while True:
        await asyncio.sleep(60)
