from typing import Optional
from pymongo.collection import Collection
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.time_helpers import to_minutes, median_minutes, get_utc_hour, make_range_hours
from utils.session_helpers import get_sessions_in_hour_range
from models.times import SuggestedTime, BestTimes

DEFAULT_NEUTRAL_HOUR = 15
DEFAULT_END_OF_DAY_HOUR = 22

def calculate_best_times(
    user_id: str,
    sessions_collection: Collection,
    user_timezone: str = "Europe/Warsaw"
) -> Optional[BestTimes]:

    def compute_time(hour_range_start: int, hour_range_end: int, default_hour: int) -> SuggestedTime:
        start_utc, end_utc = make_range_hours(today, tz, hour_range_start, hour_range_end)
        sessions = get_sessions_in_hour_range(sessions_collection, user_id, start_utc, end_utc)

        if sessions:
            minutes = median_minutes([to_minutes(s["date"]) for s in sessions])
        else:
            minutes = default_hour * 60

        start_minutes = start_utc * 60
        end_minutes = end_utc * 60
        if end_minutes <= start_minutes:
            if minutes < start_minutes:
                minutes += 24 * 60
            end_minutes += 24 * 60

        minutes = max(minutes, start_minutes)
        minutes = min(minutes, end_minutes)
        minutes %= 24 * 60

        return SuggestedTime.from_minutes(minutes)

    try:
        tz = ZoneInfo(user_timezone)
        today = datetime.now(tz).date()
        neutral_hour = get_utc_hour(DEFAULT_NEUTRAL_HOUR, user_timezone)
        end_of_day_hour = get_utc_hour(DEFAULT_END_OF_DAY_HOUR, user_timezone)

        neutral_time = compute_time(0, 21, neutral_hour)
        end_of_day_time = compute_time(21, 0, end_of_day_hour)

        print(f'Calculated best times for user {user_id}: Neutral Time - {neutral_time}, End of Day Time - {end_of_day_time}')

        return BestTimes(neutral_time=neutral_time, end_of_day_time=end_of_day_time)

    except Exception as e:
        print("Failed to calculate best times:", e)
        return None