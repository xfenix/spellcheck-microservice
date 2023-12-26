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
