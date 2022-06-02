"""All projects end-points lie here."""
import typing

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from . import models, spell
from .settings import SETTINGS


SPELL_APP: typing.Final[fastapi.FastAPI] = fastapi.FastAPI(docs_url="/docs/")
if SETTINGS.debug:
    SPELL_APP.add_middleware(
        CORSMiddleware,
        allow_origins=("*",),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@SPELL_APP.post(f"{SETTINGS.api_prefix}/check/", summary="Check spelling")
def spell_check_main_endpoint(request_payload: models.SpellCheckRequest) -> list[list[str]]:
    """Check spelling of text for exact language."""
    return models.SpellCheckResponse(
        **request_payload.dict(),
        corrections=spell.run_spellcheck(request_payload.text, request_payload.language),
    )
