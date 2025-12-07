import random
from utils.get_translations import get_translations
from constants.languages import LanguageCodeValue
from constants.notifications_keys import NeutralNotification, EndOfDayNotification

neutral_notifications = list(NeutralNotification.__args__)
end_of_day_notifications = list(EndOfDayNotification.__args__)


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
