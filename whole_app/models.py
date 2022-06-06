# pylint: disable=no-member
"""Models for input/output."""
import typing

import pydantic

from .settings import SETTINGS


class OneCorrection(pydantic.BaseModel):
    """This model is one correction for one word."""

    first_position: int
    last_position: int
    word: str
    suggestions: set[str]


class SpellCheckRequest(pydantic.BaseModel):
    """Request model for spell check request."""

    text: str = pydantic.Field(..., example="Привед как дила")
    language: typing.Literal["ru", "en", "de", "es", "fr", "pt"]


class SpellCheckResponse(SpellCheckRequest):
    """This model for check response."""

    corrections: list[OneCorrection]


class HealthCheckResponse(pydantic.BaseModel):
    """This model for health check response."""

    service_name: str = SETTINGS.service_name
    version: str
    status: typing.Literal["ok", "notok"] = "ok"
