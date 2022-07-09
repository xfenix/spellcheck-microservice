"""Spellcheck service functions."""

import pylru
from enchant.checker import SpellChecker

from . import models
from .settings import SETTINGS


_CACHE_STORAGE: dict[str, list[str]] = pylru.lrucache(SETTINGS.cache_size)


class SpellCheckService:
    """Spellcheck service class."""

    _language: models.AvailableLanguagesType
    _spellcheck_engine: SpellChecker
    _user_corrections: list[models.OneCorrection]

    def __init__(self, desired_language: models.AvailableLanguagesType) -> None:
        """Initialize spellchecker."""
        self._language = desired_language

    def prepare(self) -> "SpellCheckService":
        """Initialize machinery."""
        self._user_corrections = []
        self._spellcheck_engine = SpellChecker(self._language)
        return self

    def run_check(self, input_text: str) -> list[models.OneCorrection]:
        """Main spellcheck procedure."""
        self._spellcheck_engine.set_text(input_text)
        for one_result in self._spellcheck_engine:
            misspeled_suggestions: list[str]
            if one_result.word in _CACHE_STORAGE:
                misspeled_suggestions = _CACHE_STORAGE[one_result.word]
            else:
                misspeled_suggestions = one_result.suggest()
                _CACHE_STORAGE[one_result.word] = misspeled_suggestions
            self._user_corrections.append(
                models.OneCorrection(
                    first_position=one_result.wordpos,
                    last_position=one_result.wordpos + len(one_result.word),
                    word=one_result.word,
                    suggestions=misspeled_suggestions[: SETTINGS.max_suggestions]
                    if SETTINGS.max_suggestions
                    else misspeled_suggestions,
                )
            )
        return self._user_corrections
