"""Spellcheck service functions."""

import functools

import enchant

from . import models
from .settings import SETTINGS


_GLOBAL_SUGGESTIONS_CACHE: dict[str, list[str]] = {}


class SpellCheckService:
    """Spellcheck service class."""

    _language: models.AvailableLanguagesType
    _spellcheck_engine: enchant.Dict
    _user_corrections: list[models.OneCorrection] = []

    def __init__(self, desired_language: models.AvailableLanguagesType) -> None:
        """Initialize spellchecker."""
        self._language = desired_language

    def prepare(self) -> "SpellCheckService":
        """Initialize machinery."""
        self._spellcheck_engine: enchant.Dict = enchant.Dict(self._language)
        return self

    @functools.lru_cache(maxsize=SETTINGS.cache_size)
    def _made_suggestions(self, ready_word: str) -> list[str] | None:
        # skip to short words
        if len(ready_word) < SETTINGS.minimum_length_for_correction:
            return None
        # skip correct words
        if self._spellcheck_engine.check(ready_word):
            return None
        return self._spellcheck_engine.suggest(ready_word)

    def _make_one_correction_and_append_to_output(self, index: int, one_word_buf: list[str]) -> None:
        ready_word: str = "".join(one_word_buf)
        possible_candidates: list[str] | None = self._made_suggestions(ready_word)
        if not possible_candidates:
            return
        self._user_corrections.append(
            models.OneCorrection(
                first_position=index - len(one_word_buf),
                last_position=index - 1,
                word=ready_word,
                suggestions=possible_candidates[: SETTINGS.max_suggestions]
                if SETTINGS.max_suggestions
                else possible_candidates,
            )
        )

    def run_check(self, input_text: str) -> list[models.OneCorrection]:
        """Main spellcheck procedure."""
        one_char: str
        one_word_buf: list[str] = []
        for index, one_char in enumerate(input_text):
            if one_char.isalpha():
                one_word_buf.append(one_char)
            elif one_word_buf:
                self._make_one_correction_and_append_to_output(index, one_word_buf)
                one_word_buf = []
        if one_word_buf:
            self._make_one_correction_and_append_to_output(len(input_text), one_word_buf)
        return self._user_corrections
