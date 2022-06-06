"""Spellcheck service functions."""


import spellchecker

from . import models
from .settings import SETTINGS


def _make_one_correction_and_append_to_list(
    mutable_result: list[models.OneCorrection],
    spellcheck_engine: spellchecker.SpellChecker,
    index: int,
    one_word_buf: list[str],
) -> None:
    ready_word: str = "".join(one_word_buf)
    possible_candidates: set[str] = spellcheck_engine.candidates(ready_word)
    if len(possible_candidates) == 0 or len(possible_candidates) == 1 and ready_word in possible_candidates:
        return
    mutable_result.append(
        models.OneCorrection(
            first_position=index - len(one_word_buf),
            last_position=index - 1,
            word=ready_word,
            suggestions=set(tuple(possible_candidates)[: SETTINGS.max_suggestions])
            if SETTINGS.max_suggestions
            else possible_candidates,
        )
    )


def run_spellcheck(input_text: str, desired_language: str) -> list[models.OneCorrection]:
    """Main spellcheck procedure."""
    spellcheck_engine: spellchecker.SpellChecker = spellchecker.SpellChecker(language=desired_language)
    user_corrections: list[models.OneCorrection] = []
    one_char: str
    one_word_buf: list[str] = []
    for index, one_char in enumerate(input_text):
        if one_char.isalpha():
            one_word_buf.append(one_char)
        elif one_word_buf:
            _make_one_correction_and_append_to_list(user_corrections, spellcheck_engine, index, one_word_buf)
            one_word_buf = []
    if one_word_buf:
        _make_one_correction_and_append_to_list(user_corrections, spellcheck_engine, len(input_text), one_word_buf)
    return user_corrections
