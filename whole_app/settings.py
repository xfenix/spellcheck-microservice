import enum
import pathlib
import typing

import pydantic
import structlog
import toml
from pydantic_settings import BaseSettings


LOGGER_OBJ: typing.Final = structlog.get_logger()
PATH_TO_PYPROJECT: typing.Final = pathlib.Path(__file__).parent.parent / "pyproject.toml"
AvailableLanguagesType = typing.Literal[
    "ru_RU",
    "en_US",
    "es_ES",
    "fr_FR",
    "de_DE",
    "pt_PT",
]
AvailableLanguages: tuple[str, ...] = typing.get_args(AvailableLanguagesType)


def _warn_about_poor_lru_cache_size(
    possible_value: int,
) -> int:
    if int(possible_value) < 1:
        LOGGER_OBJ.warning(
            (
                "You set cache size less then 1. In this case, "
                "the cache size will be unlimited and polute your memory."
            ),
        )
        return 0
    return possible_value


def _warn_about_empty_api_key(
    possible_value: str,
) -> str:
    if not possible_value:
        LOGGER_OBJ.warning("You set empty API key. This is not recommended.")
    return possible_value


def _parse_version_from_local_file(
    default_value: str,
) -> str:
    try:
        pyproject_obj: dict[str, dict[str, dict[str, str]]] = toml.loads(
            PATH_TO_PYPROJECT.read_text(),
        )
        return pyproject_obj["tool"]["poetry"]["version"]
    except (toml.TomlDecodeError, KeyError, FileNotFoundError) as exc:
        LOGGER_OBJ.warning("Cant parse version from pyproject. Trouble %s", exc)
    return default_value


class StorageProviders(enum.Enum):
    FILE: str = "file"
    DUMMY: str = "dummy"


class SettingsOfMicroservice(BaseSettings):
    app_title: typing.Literal["Spellcheck API"] = "Spellcheck API"
    service_name: typing.Literal["spellcheck-microservice"] = "spellcheck-microservice"
    sentry_dsn: str = pydantic.Field(
        "",
        description="Sentry DSN for integration. Empty field disables integration",
    )
    api_key: typing.Annotated[
        str,
        pydantic.BeforeValidator(_warn_about_empty_api_key),
    ] = pydantic.Field(
        "",
        description=(
            "define api key for users dictionaries mostly. "
            "Please, provide, if you want to enable user dictionaries API"
        ),
    )
    api_key_header_name: str = "Api-Key"
    enable_cors: bool = pydantic.Field(
        default=True,
        description="enable CORS for all endpoints. In docker container this option is disabled",
    )
    structured_logging: bool = pydantic.Field(
        default=True,
        description="enables structured (json) logging",
    )
    workers: typing.Annotated[int, pydantic.conint(gt=0, lt=301)] = pydantic.Field(
        8,
        description=(
            "define application server workers count. "
            "If you plan to use k8s and only scale with replica sets, you might want to reduce this value to `1`"
        ),
    )
    port: typing.Annotated[int, pydantic.conint(gt=1_023, lt=65_536)] = pydantic.Field(
        10_113,
        description="binding port",
    )
    cache_size: typing.Annotated[
        int,
        pydantic.BeforeValidator(_warn_about_poor_lru_cache_size),
    ] = pydantic.Field(
        10_000,
        description=(
            "define LRU cache size for misspelled word/suggestions cache. "
            "Any value less than `1` makes the cache size unlimited, so be careful with this option"
        ),
    )
    api_prefix: typing.Annotated[
        str,
        pydantic.BeforeValidator(
            lambda possible_value: f"/{possible_value.strip('/')}",
        ),
    ] = pydantic.Field("/api/", description="define all API's URL prefix")
    docs_url: str = pydantic.Field(
        "/docs/",
        description="define documentation (swagger) URL prefix",
    )
    max_suggestions: typing.Annotated[
        int | None,
        pydantic.conint(gt=0) | None,
    ] = pydantic.Field(
        None,
        description="defines how many maximum suggestions for each word will be available. `None` means unlimitied",
    )
    dictionaries_path: pathlib.Path = pydantic.Field(
        pathlib.Path("/data/"),
        description=(
            "define directory where user dicts is stored. "
            "This is inner directory in the docker image, please map it to volume as it "
            "shown in the quickstart part of this readme"
        ),
    )
    dictionaries_storage_provider: StorageProviders = pydantic.Field(
        StorageProviders.FILE,
        description="define wich engine will store user dictionaries",
    )
    dictionaries_disabled: bool = pydantic.Field(
        default=False,
        description="switches off user dictionaries API no matter what",
    )
    current_version: typing.Annotated[
        str,
        pydantic.BeforeValidator(_parse_version_from_local_file),
    ] = ""
    username_min_length: int = pydantic.Field(
        3,
        description="minimum length of username",
    )
    username_max_length: int = pydantic.Field(
        60,
        description="maximum length of username",
    )
    username_regex: str = r"^[a-zA-Z0-9-_]*$"

    class Config:
        env_prefix: str = "spellcheck_"


SETTINGS: SettingsOfMicroservice = SettingsOfMicroservice()
