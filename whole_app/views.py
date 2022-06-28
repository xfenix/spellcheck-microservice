"""All projects end-points lie here."""
import typing

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from . import misc_helpers, models, spell
from .settings import SETTINGS


SPELL_APP: typing.Final[fastapi.FastAPI] = fastapi.FastAPI(docs_url=SETTINGS.docs_url, openapi_url=f"{SETTINGS.api_prefix}/openapi.json")
CURRENT_APP_VERSION: typing.Final[str] = misc_helpers.parse_version_from_local_file()
if SETTINGS.debug:
    SPELL_APP.add_middleware(
        CORSMiddleware,
        allow_origins=("*",),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@SPELL_APP.post(f"{SETTINGS.api_prefix}/check/", summary="Check spelling")
def spell_check_main_endpoint(request_payload: models.SpellCheckRequest) -> models.SpellCheckResponse:
    """Check spelling of text for exact language."""
    return models.SpellCheckResponse(
        **request_payload.dict(),
        corrections=spell.SpellCheckService(request_payload.language).prepare().run_check(request_payload.text),
    )


@SPELL_APP.get(f"{SETTINGS.api_prefix}/health/", summary="Regular healthcheck api")
async def check_health_of_service() -> models.HealthCheckResponse:
    """Check health of service."""
    return models.HealthCheckResponse(version=CURRENT_APP_VERSION)
