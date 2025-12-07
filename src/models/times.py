from dataclasses import dataclass

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