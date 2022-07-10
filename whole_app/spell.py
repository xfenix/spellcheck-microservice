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

    def __init__(self, request_payload: models.SpellCheckRequest) -> None:
        """Initialize class from user request."""
        self._language = request_payload.language
        self._input_text = request_payload.text

    def prepare(self) -> "SpellCheckService":
        """Initialize machinery."""
        self._spellcheck_engine = SpellChecker(self._language)
        return self

    def run_check(self) -> list[models.OneCorrection]:
        """Main spellcheck procedure."""
        corrections_output: list[models.OneCorrection] = []
        self._spellcheck_engine.set_text(self._input_text)
        for one_result in self._spellcheck_engine:
            misspelled_suggestions: list[str]
            if one_result.word in _CACHE_STORAGE:
                misspelled_suggestions = _CACHE_STORAGE[one_result.word]
            else:
                misspelled_suggestions = one_result.suggest()
                _CACHE_STORAGE[one_result.word] = misspelled_suggestions
            corrections_output.append(
                models.OneCorrection(
                    first_position=one_result.wordpos,
                    last_position=one_result.wordpos + len(one_result.word),
                    word=one_result.word,
                    suggestions=misspelled_suggestions[: SETTINGS.max_suggestions]
                    if SETTINGS.max_suggestions
                    else misspelled_suggestions,
                )
            )
        return corrections_output
