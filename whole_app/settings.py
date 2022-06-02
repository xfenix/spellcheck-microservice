"""Core settings of whole project."""
import pydantic


class _SettingsWrapperWhoseNameNobodyCaresAbout(pydantic.BaseSettings):
    """Literally no one cares."""

    debug: bool = True
    workers: int = 4
    port: int = 10113
    api_prefix: str = "/api/"

    @pydantic.validator("api_prefix")
    def api_prefix_must_be_with_slash_for_left_part_and_without_it_for_right(cls, possible_value: str) -> str:
        """Helps not mess up the API prefix in the application.."""
        return f"/{possible_value.strip('/')}"

    class Config:
        """I hate this config classes in classes."""

        env_prefix: str = "spellcheck_microservice_"


SETTINGS: _SettingsWrapperWhoseNameNobodyCaresAbout = _SettingsWrapperWhoseNameNobodyCaresAbout()
