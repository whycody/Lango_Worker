from datetime import datetime, time, date, timezone
from zoneinfo import ZoneInfo


def to_minutes(dt: datetime) -> int:
    return dt.hour * 60 + dt.minute


def median_minutes(values: list[int]) -> int:
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) // 2
    return sorted_values[mid]


def local_hour_to_utc(today_local: date, tz: ZoneInfo, local_hour: int) -> int:
    local_dt = datetime.combine(today_local, time(local_hour, 0), tzinfo=tz)
    utc_dt = local_dt.astimezone(timezone.utc)
    return utc_dt.hour


def clamp_end_minutes(end_minutes: int, start_minutes: int, end_max_minutes: int) -> int:
    if end_max_minutes <= start_minutes:
        if end_minutes < start_minutes:
            end_minutes += 24 * 60
        end_max_minutes += 24 * 60
    end_minutes = max(end_minutes, start_minutes)
    end_minutes = min(end_minutes, end_max_minutes)
    return end_minutes % (24 * 60)


def get_utc_hour(local_hour: int, tz_name: str) -> int:
    local_dt = datetime.now().replace(hour=local_hour, minute=0, second=0, microsecond=0, tzinfo=ZoneInfo(tz_name))
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

    return utc_dt.hour


def make_range_hours(today_local: date, tz: ZoneInfo, start_h: int, end_h: int) -> tuple[int, int]:
    start_utc = local_hour_to_utc(today_local, tz, start_h)
    end_utc = local_hour_to_utc(today_local, tz, end_h)
    return start_utc, end_utc
