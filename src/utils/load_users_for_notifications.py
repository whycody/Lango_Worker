from db import db
from datetime import datetime, timezone
import pytz

async def load_users_for_notifications():
    now_utc = datetime.now(timezone.utc)

    users_cursor = db.users.find(
        {
            "notifications.enabled": True,
            "notifications.deviceTokens.0": {"$exists": True}
        },
        {
            "_id": 1,
            "timezone": 1,
            "translationLang": 1,
            "notifications": 1,
            "stats": 1
        }
    )

    users_for_notifications = []

    async for user in users_cursor:
        tz_name = user.get("timezone") or "UTC"
        tz = pytz.timezone(tz_name)
        today = datetime.now(tz).strftime("%Y-%m-%d")

        study_days = user.get("stats", {}).get("studyDays", [])
        if today not in study_days:
            users_for_notifications.append(user)

    return users_for_notifications