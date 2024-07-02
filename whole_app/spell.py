import re
import typing

import pylru
import urlextract
from enchant.checker import SpellChecker

from . import models
from .settings import SETTINGS


_MISSPELED_CACHE: typing.Final[dict[str, list[str]]] = (
    pylru.lrucache(SETTINGS.cache_size) if SETTINGS.cache_size > 0 else {}
)


class SpellCheckService:
    __slots__ = ("_input_text", "_spellcheck_engine", "_exclusion_words")
    _input_text: str
    _spellcheck_engine: SpellChecker
    _exclusion_words: list[str]
    _url_extractor: urlextract.URLExtract = urlextract.URLExtract()

    def prepare(
        self: "SpellCheckService",
        request_payload: models.SpellCheckRequest,
        exclusion_words: list[str] | None = None,
    ) -> "SpellCheckService":
        """Initialize machinery."""
        self._input_text = request_payload.text
        self._exclusion_words = exclusion_words if exclusion_words else []

        if request_payload.exclude_urls:
            for url in self._url_extractor.find_urls(self._input_text):
                self._exclusion_words.extend(
                    [word.lower() for word in re.split(r"\.|\:|\/\/|\/|\?|\&|\=|\+|\#|\-", url)]
                )

        self._spellcheck_engine = SpellChecker(request_payload.language)
        return self

    @staticmethod
    def get_memorized_suggestions(word_spellcheck_result: SpellChecker) -> list[str]:
        misspelled_suggestions: list[str]
        if word_spellcheck_result.word in _MISSPELED_CACHE:
            misspelled_suggestions = _MISSPELED_CACHE[word_spellcheck_result.word]
        else:
            misspelled_suggestions = word_spellcheck_result.suggest()
            _MISSPELED_CACHE[word_spellcheck_result.word] = misspelled_suggestions
        return (
            misspelled_suggestions[: SETTINGS.max_suggestions]
            if SETTINGS.max_suggestions > 0
            else misspelled_suggestions
        )

    def run_check(self: "SpellCheckService") -> list[models.OneCorrection]:
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
                ),
            )
        return corrections_output
