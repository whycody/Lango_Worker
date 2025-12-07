from utils.notifications_helper import get_random_neutral_notification, get_random_end_of_day_notification

NOTIFICATION_TYPES = {
    "neutral": {
        "notif_type": "reminder_neutral",
        "time_key": "neutralTime",
        "last_key": "neutralTimeLastNotifiedAt",
        "default_time": {"hour": 9, "minute": 0},
        "content_provider": get_random_neutral_notification,
    },
    "end_of_day": {
        "notif_type": "reminder_end_of_day",
        "time_key": "endOfDayTime",
        "last_key": "endOfDayTimeLastNotifiedAt",
        "default_time": {"hour": 20, "minute": 0},
        "content_provider": get_random_end_of_day_notification,
    }
}