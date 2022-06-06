"""Spellcheck service functions."""
import pymorphy2
import spellchecker

from . import models
from .settings import SETTINGS


def _make_one_correction_and_append_to_list(
    mutable_result: list[models.OneCorrection],
    index: int,
    one_word_buf: list[str],
    spellcheck_engine: spellchecker.SpellChecker,
    morph_engine: pymorphy2.MorphAnalyzer,
) -> None:
    ready_word: str = "".join(one_word_buf)
    if len(ready_word) < SETTINGS.minimum_length_for_correction:
        return
    if spellcheck_engine.word_probability(morph_engine.parse(ready_word)[0].normal_form) > 0:
        return
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
    morph_engine: pymorphy2.MorphAnalyzer = pymorphy2.MorphAnalyzer(lang=desired_language)
    user_corrections: list[models.OneCorrection] = []
    one_char: str
    one_word_buf: list[str] = []
    for index, one_char in enumerate(input_text):
        if one_char.isalpha():
            one_word_buf.append(one_char)
        elif one_word_buf:
            _make_one_correction_and_append_to_list(
                user_corrections, index, one_word_buf, spellcheck_engine, morph_engine
            )
            one_word_buf = []
    if one_word_buf:
        _make_one_correction_and_append_to_list(
            user_corrections, len(input_text), one_word_buf, spellcheck_engine, morph_engine
        )
    return user_corrections
