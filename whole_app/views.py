"""All projects end-points lie here."""
import typing

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from . import dictionaries, misc_helpers, models, spell
from .dictionaries.protocol import UserDictProtocol
from .settings import SETTINGS


SPELL_APP: typing.Final[fastapi.FastAPI] = fastapi.FastAPI(
    docs_url=SETTINGS.docs_url, openapi_url=f"{SETTINGS.api_prefix}/openapi.json"
)
CURRENT_APP_VERSION: typing.Final[str] = misc_helpers.parse_version_from_local_file()
if SETTINGS.enable_cors:
    SPELL_APP.add_middleware(
        CORSMiddleware,
        allow_origins=("*",),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@SPELL_APP.on_event("startup")
def startup() -> None:
    """Initialize storage."""
    dictionaries.init_storage()
    misc_helpers.init_logger()


@SPELL_APP.post(f"{SETTINGS.api_prefix}/check/", summary="Check spelling")
def spell_check_main_endpoint(
    request_payload: models.SpellCheckRequest, spell_service: spell.SpellCheckService = fastapi.Depends()
) -> models.SpellCheckResponse:
    """Check spelling of text for exact language."""
    return models.SpellCheckResponse(
        **request_payload.dict(),
        corrections=spell_service.prepare(request_payload).run_check(),
    )


@SPELL_APP.get(f"{SETTINGS.api_prefix}/health/", summary="Regular healthcheck api")
async def check_health_of_service() -> models.HealthCheckResponse:
    """Check health of service."""
    return models.HealthCheckResponse(version=misc_helpers.parse_version_from_local_file())


if not SETTINGS.dictionaries_disabled:

    @SPELL_APP.post(
        f"{SETTINGS.api_prefix}/dictionaries/",
        summary="Add word to user dictionary",
        status_code=201,
    )
    async def save_word(
        request_model: models.UserDictionaryRequestWithWord,
        storage_engine: UserDictProtocol = fastapi.Depends(dictionaries.prepare_storage_engine),
    ) -> bool:
        """Save word to user dictionary."""
        await storage_engine.prepare(request_model.user_name).save_record(request_model.exception_word)
        return True

    @SPELL_APP.delete(
        f"{SETTINGS.api_prefix}/dictionaries/",
        summary="Remove word from user dictionary",
    )
    async def delete_word(
        request_model: models.UserDictionaryRequestWithWord,
        storage_engine: UserDictProtocol = fastapi.Depends(dictionaries.prepare_storage_engine),
    ) -> bool:
        """Save word to user dictionary."""
        await storage_engine.prepare(request_model.user_name).remove_record(request_model.exception_word)
        return True
