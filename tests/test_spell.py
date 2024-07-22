import typing

import pytest

from tests._fixtures import COMMON_TEXT_MESSAGE
from tests.test_spell_views import RU_LANG
from whole_app import models
from whole_app.settings import SETTINGS
from whole_app.spell import SpellCheckService


def test_correct_spell() -> None:
    fake_engine: SpellCheckService = SpellCheckService()
    # нужно сделать несколько тестов. B одном text рандомизировать
    # в другом брать из _fixtures
    fake_engine.prepare(
        models.SpellCheckRequest(text="Превед медвет", language="ru_RU"),
    ).run_check()
    # a тут надо проверять, что first_position и last_position корректные, что word соответствует слову из text
    # что в corrections есть правильные варианты (в рандомизированном случае можно такое не проверять)
    # важно: нужно ВРУЧНУЮ подбирать first_position, last_position и правильные слова и вручную вносить сюда


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
