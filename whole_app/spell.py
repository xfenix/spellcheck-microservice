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

    def prepare(self, request_payload: models.SpellCheckRequest) -> "SpellCheckService":
        """Initialize machinery."""
        self._input_text = request_payload.text
        self._spellcheck_engine = SpellChecker(request_payload.language)
        return self

    def run_check(self) -> list[models.OneCorrection]:
        """Main spellcheck procedure."""
        corrections_output: list[models.OneCorrection] = []
        self._spellcheck_engine.set_text(self._input_text)
        for one_result in self._spellcheck_engine:
            misspeled_suggestions: list[str]
            if one_result.word in _CACHE_STORAGE:
                misspeled_suggestions = _CACHE_STORAGE[one_result.word]
            else:
                misspeled_suggestions = one_result.suggest()
                _CACHE_STORAGE[one_result.word] = misspeled_suggestions
            corrections_output.append(
                models.OneCorrection(
                    first_position=one_result.wordpos,
                    last_position=one_result.wordpos + len(one_result.word),
                    word=one_result.word,
                    suggestions=misspeled_suggestions[: SETTINGS.max_suggestions]
                    if SETTINGS.max_suggestions
                    else misspeled_suggestions,
                )
            )
        return corrections_output
