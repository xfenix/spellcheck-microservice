# pylint: disable=no-member
"""Models for input/output."""
import typing

import pydantic

from .settings import SETTINGS, AvailableLanguages, AvailableLanguagesType


class OneCorrection(pydantic.BaseModel):
    """This model is one correction for one word."""

    first_position: int
    last_position: int
    word: str
    suggestions: set[str]


class SpellCheckRequest(pydantic.BaseModel):
    """Request model for spell check request."""

    text: str = pydantic.Field(..., example="Привед как дила")
    language: AvailableLanguagesType


class SpellCheckResponse(SpellCheckRequest):
    """This model for check response."""

    corrections: list[OneCorrection]


class UserDictionaryRequest(pydantic.BaseModel):
    """Request model for user dictionary request."""

    user_name: pydantic.constr(regex="^[a-zA-Z0-9-_]*$", min_length=3, max_length=60) = pydantic.Field(  # type: ignore
        ..., example="username"
    )


class UserDictionaryRequestWithWord(UserDictionaryRequest):
    """Request model for user dictionary request with word."""

    exception_word: str


class HealthCheckResponse(pydantic.BaseModel):
    """This model for health check response."""

    service_name: str = SETTINGS.service_name
    supported_languages: tuple[str, ...] = AvailableLanguages
    version: str
    status: typing.Literal["ok", "notok"] = "ok"
