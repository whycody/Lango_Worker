import json
from pathlib import Path
from constants.languages import LanguageCodeValue, SUPPORTED_LANGUAGES

TranslationKey = str

translations_map: dict[LanguageCodeValue, dict[TranslationKey, str]] = {}

for code in SUPPORTED_LANGUAGES:
    path = Path(__file__).parent.parent / "translations" / f"{code}.json"
    with open(path, "r", encoding="utf-8") as f:
        translations_map[code] = json.load(f)


def get_translations(lang: LanguageCodeValue) -> dict[TranslationKey, str]:
    try:
        return translations_map[lang]
    except KeyError:
        raise ValueError(f"Translations not found for language: {lang}")
