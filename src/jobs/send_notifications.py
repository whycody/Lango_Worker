import datetime
from zoneinfo import ZoneInfo
from pymongo.collection import Collection
from utils.notifications_helper import get_random_neutral_notification, get_random_end_of_day_notification
from utils.should_notify import should_notify
from firebase import send_push_notification
from constants.notifications_types import NOTIFICATION_TYPES


async def process_notification(user, token, user_now, now_utc, tz_name, db, cfg):
    last_notified_at = user["notifications"].get(cfg["last_key"])
    time_cfg = user["notifications"].get(cfg["time_key"], cfg["default_time"])

    if not should_notify(user_now, time_cfg["hour"], time_cfg["minute"], last_notified_at, tz_name):
        return

    lang = user.get("translationLang", "en")
    content = cfg["content_provider"](lang)

    await send_push_notification(token, content["title"], content["body"], cfg["notif_type"])

    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {f"notifications.{cfg['last_key']}": now_utc}},
    )


async def send_notifications(db: Collection):
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    users_cursor = db.users.find({
        "notifications.enabled": True,
        "notifications.deviceTokens.0": {"$exists": True},
    })

    for user in users_cursor:
        tz_name = user.get("timezone", "UTC")
        tz = ZoneInfo(tz_name)
        user_now = now_utc.astimezone(tz)

        today_str = user_now.strftime("%Y-%m-%d")
        if today_str in user.get("stats", {}).get("studyDays", []):
            continue

        for token_obj in user["notifications"]["deviceTokens"]:
            token = token_obj["token"]

            for cfg in NOTIFICATION_TYPES.values():
                await process_notification(
                    user, token, user_now, now_utc, tz_name, db, cfg
                )