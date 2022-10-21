"""Spellcheck service functions."""
import typing

import pylru
from enchant.checker import SpellChecker

from . import models
from .settings import SETTINGS


_MISSPELED_CACHE: dict[str, list[str]] = pylru.lrucache(SETTINGS.cache_size) if SETTINGS.cache_size > 0 else {}


class SpellCheckService:
    """Spellcheck service class."""

    __slots__ = ("_input_text", "_spellcheck_engine", "_exclusion_words")

    _input_text: str
    _spellcheck_engine: SpellChecker
    _exclusion_words: list[str]

    def prepare(
        self, request_payload: models.SpellCheckRequest, exclusion_words: typing.Optional[list[str]] = None
    ) -> "SpellCheckService":
        """Initialize machinery."""
        self._input_text = request_payload.text
        self._exclusion_words = exclusion_words if exclusion_words else []
        self._spellcheck_engine = SpellChecker(request_payload.language)
        return self

    @staticmethod
    def get_memorized_suggestions(word_spellcheck_result: SpellChecker) -> list[str]:
        """Try to get suggestions from lru cache or ask SpellChecker for
        them."""
        misspelled_suggestions: list[str]
        if word_spellcheck_result.word in _MISSPELED_CACHE:
            misspelled_suggestions = _MISSPELED_CACHE[word_spellcheck_result.word]
        else:
            misspelled_suggestions = word_spellcheck_result.suggest()
            _MISSPELED_CACHE[word_spellcheck_result.word] = misspelled_suggestions
        return (
            misspelled_suggestions[: SETTINGS.max_suggestions] if SETTINGS.max_suggestions else misspelled_suggestions
        )

    def run_check(self) -> list[models.OneCorrection]:
        """Main spellcheck procedure."""
        corrections_output: list[models.OneCorrection] = []
        self._spellcheck_engine.set_text(self._input_text)
        for one_result in self._spellcheck_engine:
            if one_result.word.lower() in self._exclusion_words:
                continue
            corrections_output.append(
                models.OneCorrection(
                    first_position=one_result.wordpos,
                    last_position=one_result.wordpos + len(one_result.word),
                    word=one_result.word,
                    suggestions=self.get_memorized_suggestions(one_result),
                )
            )
        return corrections_output
