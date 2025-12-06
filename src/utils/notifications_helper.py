import random
from typing import Literal
from utils.get_translations import get_translations

LanguageCodeValue = Literal["en", "pl", "es", "it"]

neutral_notifications = [
    "time_for_study",
    "keep_it_up",
    "learning_moment",
    "daily_goal_reminder",
    "hydration_break",
    "streak_safety",
    "small_step",
    "consistency_matters",
    "mini_challenge",
]

end_of_day_notifications = [
    "dont_forget_session",
    "finish_before_midnight",
    "almost_end_of_day",
    "last_call",
    "quick_session",
    "end_of_day_focus",
]

def get_random_neutral_notification(lang: LanguageCodeValue) -> dict[str, str]:
    translations = get_translations(lang)
    key = random.choice(neutral_notifications)
    return {
        "title": translations[f"{key}_title"],
        "body": translations[f"{key}_body"]
    }

def get_random_end_of_day_notification(lang: LanguageCodeValue) -> dict[str, str]:
    translations = get_translations(lang)
    key = random.choice(end_of_day_notifications)
    return {
        "title": translations[f"{key}_title"],
        "body": translations[f"{key}_body"]
    }
