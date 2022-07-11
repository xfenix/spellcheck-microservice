"""Spellcheck service functions."""
import pylru
from enchant.checker import SpellChecker

from . import models
from .settings import SETTINGS


_CACHE_STORAGE: dict[str, list[str]] = pylru.lrucache(SETTINGS.cache_size) if SETTINGS.cache_size > 0 else {}


class SpellCheckService:
    """Spellcheck service class."""

    _input_text: str
    _spellcheck_engine: SpellChecker
    _exclusion_words: list[str]

    def prepare(self, request_payload: models.SpellCheckRequest, exclusion_words: list[str]) -> "SpellCheckService":
        """Initialize machinery."""
        self._input_text = request_payload.text
        self._exclusion_words = exclusion_words
        self._spellcheck_engine = SpellChecker(request_payload.language)
        return self

    def run_check(self) -> list[models.OneCorrection]:
        """Main spellcheck procedure."""
        corrections_output: list[models.OneCorrection] = []
        self._spellcheck_engine.set_text(self._input_text)
        for one_result in self._spellcheck_engine:
            if one_result.word.lower() in self._exclusion_words:
                continue
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
