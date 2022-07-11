"""Basic test for views."""

from whole_app import models
from whole_app.spell import SpellCheckService


def test_correct_spell():
    """Basic test."""
    fake_engine: SpellCheckService = SpellCheckService()
    # нужно сделать несколько тестов. В одном text рандомизировать
    # в другом брать из _fixtures
    results: list[str] = fake_engine.prepare(
        models.SpellCheckRequest(text="Превед медвет", language="ru_RU")
    ).run_check()
    # а тут надо проверять, что first_position и last_position корректные, что word соответствует слову из text
    # что в corrections есть правильные варианты (в рандомизированном случае можно такое не проверять)
    print(results)
