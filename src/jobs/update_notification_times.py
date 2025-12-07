from utils.calculate_best_times import calculate_best_times
from pymongo.collection import Collection


def update_notification_times(db: Collection):
    print("Updating notification times for users...", flush=True)
    try:
        users_cursor = db.users.find({"notifications.enabled": True}, {"_id": 1, "timezone": 1})
        for user in users_cursor:
            user_id = user["_id"]
            user_timezone = user.get("timezone", "Europe/Warsaw")
            best_times = calculate_best_times(user_id, db.sessions, user_timezone)
            if best_times:
                db.users.update_one(
                    {"_id": user_id},
                    {
                        "$set": {
                            "notifications.neutralTime.hour": best_times.neutral_time.hour,
                            "notifications.neutralTime.minute": best_times.neutral_time.minute,
                            "notifications.endOfDayTime.hour": best_times.end_of_day_time.hour,
                            "notifications.endOfDayTime.minute": best_times.end_of_day_time.minute,
                        }
                    }
                )
        print("Notification times updated successfully.", flush=True)
    except Exception as e:
        print("Failed to update notification times:", e, flush=True)
