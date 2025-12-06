import datetime
from typing import Literal
from zoneinfo import ZoneInfo
from pymongo.collection import Collection
from utils.notifications_helper import get_random_neutral_notification, get_random_end_of_day_notification
from utils.should_notify import should_notify
from firebase import send_push_notification

LanguageCodeValue = Literal["en", "pl", "es", "it"]

async def send_notifications(db: Collection):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    users_cursor = db.users.find({
        "notifications.enabled": True,
        "notifications.deviceTokens.0": {"$exists": True}
    })

    for user in users_cursor:
        tz_name = user.get("timezone") or "UTC"
        tz = ZoneInfo(tz_name)
        user_now = now_utc.astimezone(tz)

        today_str = user_now.strftime("%Y-%m-%d")
        study_days = user.get("stats", {}).get("studyDays", [])
        if today_str in study_days:
            continue

        neutral_last = user.get("notifications", {}).get("neutralTimeLastNotifiedAt")
        end_last = user.get("notifications", {}).get("endOfDayTimeLastNotifiedAt")

        for token in user.get("notifications", {}).get("deviceTokens", []):
            print(f"Processing user {user['_id']} for token {token}", flush=True)
            neutral_time = user.get("notifications", {}).get("neutralTime", {"hour": 9, "minute": 0})
            end_of_day_time = user.get("notifications", {}).get("endOfDayTime", {"hour": 20, "minute": 0})

            if should_notify(user_now, neutral_time["hour"], neutral_time["minute"], neutral_last, tz_name):
                content = get_random_neutral_notification(user.get("translationLang", "en"))
                await send_push_notification(token['token'], content['title'], content['body'])
                db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"notifications.neutralTimeLastNotifiedAt": now_utc}}
                )

            if should_notify(user_now, end_of_day_time["hour"], end_of_day_time["minute"], end_last, tz_name):
                content = get_random_end_of_day_notification(user.get("translationLang", "en"))
                await send_push_notification(token['token'], content['title'], content['body'])
                db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"notifications.endOfDayTimeLastNotifiedAt": now_utc}}
                )