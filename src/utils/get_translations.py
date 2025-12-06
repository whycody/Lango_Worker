import json
from pathlib import Path
from typing import Literal

LanguageCodeValue = Literal["en", "pl", "es", "it"]
NotificationKey = Literal[
    "time_for_study",
    "keep_it_up",
    "learning_moment",
    "daily_goal_reminder",
    "hydration_break",
    "streak_safety",
    "small_step",
    "consistency_matters",
    "mini_challenge",
    "dont_forget_session",
    "finish_before_midnight",
    "almost_end_of_day",
    "last_call",
    "quick_session",
    "end_of_day_focus",
]

TranslationKey = str

translations_map: dict[LanguageCodeValue, dict[TranslationKey, str]] = {}

for lang in ["en", "pl", "es", "it"]:
    path = Path(__file__).parent.parent / "translations" / f"{lang}.json"
    with open(path, "r", encoding="utf-8") as f:
        translations_map[lang] = json.load(f)

def get_translations(lang: LanguageCodeValue) -> dict[TranslationKey, str]:
    data = translations_map.get(lang)
    if not data:
        raise ValueError(f"Translations not found for language: {lang}")
    return data