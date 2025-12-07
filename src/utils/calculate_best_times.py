from typing import Optional
from dataclasses import dataclass
from pymongo.collection import Collection
from datetime import datetime, time, date, timezone
from zoneinfo import ZoneInfo


@dataclass
class SuggestedTime:
    hour: int
    minute: int

    @staticmethod
    def from_minutes(total: int) -> "SuggestedTime":
        return SuggestedTime(total // 60, total % 60)


@dataclass
class BestTimes:
    neutral_time: SuggestedTime
    end_of_day_time: SuggestedTime


def to_minutes(d: datetime) -> int:
    return d.hour * 60 + d.minute


def median_minutes(values: list[int]) -> int:
    values = sorted(values)
    n = len(values)
    mid = n // 2
    if n % 2 == 0:
        return (values[mid - 1] + values[mid]) // 2
    return values[mid]


def local_hour_to_utc(today_local: date, tz: ZoneInfo, local_hour: int) -> int:
    local_dt = datetime.combine(today_local, time(local_hour, 0), tzinfo=tz)
    utc_dt = local_dt.astimezone(timezone.utc)
    return utc_dt.hour


def make_range_hours(today_local: date, tz: ZoneInfo, start_h: int, end_h: int) -> tuple[int, int]:
    start_utc = local_hour_to_utc(today_local, tz, start_h)
    end_utc = local_hour_to_utc(today_local, tz, end_h)
    return start_utc, end_utc


def get_sessions_by_local_hour_range(collection, user_id, start_hour: int, end_hour: int):
    all_sessions = list(collection.find({"userId": str(user_id)}))

    filtered = []
    for s in all_sessions:
        hour = s["date"].hour
        if start_hour <= end_hour:
            if start_hour <= hour < end_hour:
                filtered.append(s)
        else:
            if hour >= start_hour or hour < end_hour:
                filtered.append(s)
    return filtered


def get_utc_hour(local_hour: int, tz_name: str) -> int:
    local_dt = datetime.now().replace(hour=local_hour, minute=0, second=0, microsecond=0, tzinfo=ZoneInfo(tz_name))
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

    return utc_dt.hour


def calculate_best_times(
        user_id: str,
        sessions_collection: Collection,
        user_timezone: str = "Europe/Warsaw"
) -> Optional[BestTimes]:
    try:
        tz = ZoneInfo(user_timezone)
        now_local = datetime.now(tz)
        today = now_local.date()

        neutral_start_utc, neutral_end_utc = make_range_hours(today, tz, 0, 21)
        neutral_sessions = get_sessions_by_local_hour_range(
            sessions_collection, user_id, neutral_start_utc, neutral_end_utc
        )

        if neutral_sessions:
            neutral_minutes = median_minutes([
                to_minutes(s["date"]) for s in neutral_sessions
            ])
        else:
            neutral_minutes = get_utc_hour(15, user_timezone) * 60

        neutral_time = SuggestedTime.from_minutes(neutral_minutes)
        end_start_utc, end_end_utc = make_range_hours(today, tz, 21, 0)

        end_sessions = get_sessions_by_local_hour_range(
            sessions_collection, user_id, end_start_utc, end_end_utc
        )

        if end_sessions:
            end_minutes = median_minutes([
                to_minutes(s["date"]) for s in end_sessions
            ])
        else:
            end_minutes = get_utc_hour(22, user_timezone) * 60

        end_start_minutes = end_start_utc * 60
        end_end_minutes = end_end_utc * 60

        if end_end_minutes <= end_start_minutes:
            if end_minutes < end_start_minutes:
                end_minutes += 24 * 60
            end_end_minutes += 24 * 60

        end_minutes = max(end_minutes, end_start_minutes)
        end_minutes = min(end_minutes, end_end_minutes)
        end_minutes = end_minutes % (24 * 60)

        end_of_day_time = SuggestedTime.from_minutes(end_minutes)

        return BestTimes(
            neutral_time=neutral_time,
            end_of_day_time=end_of_day_time
        )

    except Exception as e:
        print("Failed to calculate best times:", e)
        return None
