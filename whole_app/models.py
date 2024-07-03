# pylint: disable=no-member
"""Models for input/output."""

import typing

import pydantic

from .settings import SETTINGS, AvailableLanguages, AvailableLanguagesType


class OneCorrection(pydantic.BaseModel):
    first_position: int
    last_position: int
    word: str
    suggestions: set[str]


class SpellCheckRequest(pydantic.BaseModel):
    text: str = pydantic.Field(..., examples=["Привед как дила"])
    language: AvailableLanguagesType
    user_name: str | None = pydantic.Field(
        None,
        examples=["username"],
        pattern=SETTINGS.username_regex,
        min_length=SETTINGS.username_min_length,
        max_length=SETTINGS.username_max_length,
    )
    exclude_urls: bool = True


class SpellCheckResponse(pydantic.BaseModel):
    text: str
    language: str
    corrections: list[OneCorrection]


class UserDictionaryRequest(pydantic.BaseModel):
    user_name: str = pydantic.Field(
        examples=["username"],
        pattern=SETTINGS.username_regex,
        min_length=SETTINGS.username_min_length,
        max_length=SETTINGS.username_max_length,
    )


class UserDictionaryRequestWithWord(UserDictionaryRequest):
    exception_word: str = pydantic.Field(..., examples=["привед"])


class HealthCheckResponse(pydantic.BaseModel):
    service_name: str = SETTINGS.service_name
    supported_languages: tuple[str, ...] = AvailableLanguages
    version: str = SETTINGS.current_version
    status: typing.Literal["ok", "notok"] = "ok"
