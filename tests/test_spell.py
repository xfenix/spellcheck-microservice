import typing

import pytest

from tests._fixtures import COMMON_TEXT_MESSAGE
from tests.test_spell_views import RU_LANG
from whole_app import models
from whole_app.settings import SETTINGS
from whole_app.spell import SpellCheckService


@pytest.mark.parametrize(
    (
        "text_input",
        "expected_corrections",
    ),
    [
        (
            "Превед медвет",
            [
                ("Превед", 0, 6, None),
                ("медвет", 7, 13, "медведь"),
            ],
        ),
        (
            "превет как дила",
            [
                ("превет", 0, 6, "привет"),
                ("дила", 11, 15, "дела"),
            ],
        ),
    ],
)
def test_correct_spell(
    text_input: str,
    expected_corrections: list[tuple[str, int, int, str | None]],
) -> None:
    fake_engine: SpellCheckService = SpellCheckService()
    corrections = fake_engine.prepare(
        models.SpellCheckRequest(text=text_input, language=RU_LANG),
    ).run_check()
    assert len(corrections) == len(expected_corrections)
    for one_correction, (word, first_position, last_position, suggestion) in zip(
        corrections,
        expected_corrections, strict=False,
    ):
        assert one_correction.first_position == first_position
        assert one_correction.last_position == last_position
        assert one_correction.word == word
        assert text_input[first_position:last_position] == word
        if suggestion is None:
            assert one_correction.suggestions
        else:
            assert suggestion in one_correction.suggestions


@pytest.mark.parametrize(
    "url",
    [
        "www.rzb.ru",
        "https://rzb.ru",
        "https://www.rzb.ru",
        "rzb.ru/taCWpO",
        "www.rzb.ru/taCWpO",
        "https://rzb.ru/taCWpO",
        "https://www.rzb.ru/taCWpO",
        "https://www.asd.google.com/search?q=some+text&param=3#dfsdf",
        "https://www.google.com",
        "http://google.com/?q=some+text&param=3#dfsdf",
        "https://www.google.com/api/?",
        "https://www.google.com/api/login.php",
        "https://r-chat.raiffeisen.ru/admin/operator/",
        "https://r-chat.raiffeisen.ru/admin/operator/taCWpO",
    ],
)
def test_urls_ignored(
    url: str,
) -> None:
    fake_engine: SpellCheckService = SpellCheckService()
    corrections = fake_engine.prepare(
        models.SpellCheckRequest(text=COMMON_TEXT_MESSAGE.format(url), language="ru_RU", exclude_urls=True),
    ).run_check()
    assert not corrections


@pytest.mark.parametrize(
    ("wannabe_user_input", "excluded_words"),
    [("ШЯЧЛО ПОПЯЧТСА ПОПЯЧТСА", {"шячло", "попячтса"})],
)
def test_default_excluded_words(
    wannabe_user_input: str,
    excluded_words: str,
    monkeypatch: typing.Any,
) -> None:
    with monkeypatch.context() as patcher:
        patcher.setattr(SETTINGS, "_exclusion_words_set", excluded_words)
        fake_engine: SpellCheckService = SpellCheckService()
        prepared = fake_engine.prepare(
            models.SpellCheckRequest(text=wannabe_user_input, language=RU_LANG, exclude_urls=False),
        )

        corrections = prepared.run_check()
        assert corrections == [], f"{corrections=} --- {prepared._exclusion_words=}"  # noqa: SLF001
