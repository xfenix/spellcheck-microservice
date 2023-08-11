# pylint: disable=no-member, no-self-argument
"""Core settings of whole project."""
import enum
import pathlib
import typing

import pydantic
import toml
from loguru import logger


AvailableLanguagesType = typing.Literal[
    "ru_RU",
    "en_US",
    "es_ES",
    "fr_FR",
    "de_DE",
    "pt_PT",
]
AvailableLanguages: tuple[str, ...] = typing.get_args(AvailableLanguagesType)


class StorageProviders(enum.Enum):
    """Default system storage providers."""

    FILE: str = "file"
    DUMMY: str = "dummy"


class SettingsOfMicroservice(pydantic.BaseSettings):
    """Main strict and totally validated settings of whole project."""

    app_title: str = pydantic.Field("Spellcheck API", const=True)
    service_name: str = pydantic.Field("spellcheck-microservice", const=True)
    sentry_dsn: str = pydantic.Field(
        "",
        description="Sentry DSN for integration. Empty field disables integration",
    )
    api_key: str = pydantic.Field(
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
    workers: pydantic.conint(gt=0, lt=301) = pydantic.Field(
        8,
        description=(
            "define application server workers count. "
            "If you plan to use k8s and only scale with replica sets, you might want to reduce this value to `1`"
        ),
    )
    port: pydantic.conint(gt=1_023, lt=65_536) = pydantic.Field(
        10_113,
        description="binding port",
    )
    cache_size: int = pydantic.Field(
        10_000,
        description=(
            "define LRU cache size for misspelled word/suggestions cache. "
            "Any value less than `1` makes the cache size unlimited, so be careful with this option"
        ),
    )
    api_prefix: str = pydantic.Field("/api/", description="define all API's URL prefix")
    docs_url: str = pydantic.Field(
        "/docs/",
        description="define documentation (swagger) URL prefix",
    )
    max_suggestions: pydantic.conint(gt=0) | None = pydantic.Field(
        None,
        description="defines how many maximum suggestions for each word will be available. `None` means unlimitied",
    )
    # version from this file will be available in the health check response
    # and version in the file itself will be updated in the CI through poetry version command
    path_to_version_file: pathlib.Path = (
        pathlib.Path(__file__).parent.parent / "pyproject.toml"
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
    current_version: str = ""
    username_min_length: int = pydantic.Field(
        3,
        description="minimum length of username",
    )
    username_max_length: int = pydantic.Field(
        60,
        description="maximum length of username",
    )
    username_regex: str = r"^[a-zA-Z0-9-_]*$"

    @pydantic.validator("api_prefix")
    def api_prefix_must_be_with_slash_for_left_part_and_without_it_for_right(
        self: "SettingsOfMicroservice",
        possible_value: str,
    ) -> str:
        """Help not mess up the API prefix in the application."""
        return f"/{possible_value.strip('/')}"

    @pydantic.validator("cache_size")
    def warn_about_poor_lru_cache_size(
        self: "SettingsOfMicroservice",
        possible_value: int,
    ) -> int:
        """Warn about poor LRU cache size."""
        if possible_value < 1:
            logger.warning(
                (
                    "You set cache size less then 1. In this case, "
                    "the cache size will be unlimited and polute your memory."
                ),
            )
            return 0
        return possible_value

    @pydantic.validator("api_key")
    def warn_about_empty_api_key(
        self: "SettingsOfMicroservice",
        possible_value: str,
    ) -> str:
        """Warn about empty API key."""
        if not possible_value:
            logger.warning("You set empty API key. This is not recommended.")
        return possible_value

    @pydantic.root_validator
    def parse_version_from_local_file(
        self: "SettingsOfMicroservice",
        values: dict,
    ) -> dict:
        """Parse version from pyproject (this file will be updated in the CI pipeline)."""
        try:
            pyproject_obj: dict = toml.loads(values["path_to_version_file"].read_text())
            values["current_version"] = pyproject_obj["tool"]["poetry"]["version"]
        except (toml.TomlDecodeError, KeyError, FileNotFoundError) as exc:
            logger.warning(f"Cant parse version from pyproject. Trouble {exc}")
        return values

    class Config:
        """I hate this config classes in classes."""

        env_prefix: str = "spellcheck_"


SETTINGS: SettingsOfMicroservice = SettingsOfMicroservice()
