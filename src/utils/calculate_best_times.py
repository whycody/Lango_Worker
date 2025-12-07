from typing import Optional
from pymongo.collection import Collection
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.time_helpers import to_minutes, median_minutes, local_hour_to_utc, get_utc_hour, clamp_end_minutes, \
    make_range_hours
from utils.session_helpers import get_sessions_in_hour_range
from models.times import SuggestedTime, BestTimes


def calculate_best_times(
        user_id: str,
        sessions_collection: Collection,
        user_timezone: str = "Europe/Warsaw"
) -> Optional[BestTimes]:
    try:
        tz = ZoneInfo(user_timezone)
        today = datetime.now(tz).date()

        neutral_start_utc, neutral_end_utc = make_range_hours(today, tz, 0, 21)
        neutral_sessions = get_sessions_in_hour_range(
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

        end_sessions = get_sessions_in_hour_range(
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

        print(f'Neutral time: {neutral_time}, End of day time: {end_of_day_time}')

        return BestTimes(
            neutral_time=neutral_time,
            end_of_day_time=end_of_day_time
        )

    except Exception as e:
        print("Failed to calculate best times:", e)
        return None
