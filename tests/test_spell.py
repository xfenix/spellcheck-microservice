import pytest

from tests._fixtures import COMMON_TEXT_MESSAGE
from whole_app import models
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
