from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

def should_notify(
    user_time: datetime,
    notif_hour: int,
    notif_minute: int,
    last_sent: Optional[datetime] = None,
    user_timezone: str = "Europe/Warsaw"
) -> bool:
    tz = ZoneInfo(user_timezone)
    user_time = user_time.astimezone(tz)

    notif_time = datetime(
        year=user_time.year,
        month=user_time.month,
        day=user_time.day,
        hour=notif_hour,
        minute=notif_minute,
        tzinfo=tz
    )

    if last_sent and last_sent.astimezone(tz).date() == user_time.date():
        return False

    max_allowed_time = notif_time + timedelta(minutes=5)
    return notif_time <= user_time <= max_allowed_time