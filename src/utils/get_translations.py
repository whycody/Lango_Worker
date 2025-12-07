import json
from pathlib import Path
from constants.languages import LanguageCodeValue

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