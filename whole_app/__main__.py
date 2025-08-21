"""Application server here.

This file meant only for basic workers wrappers and fastapi exposure.
For end-points look in views.py
"""

import typing

from granian import Granian  # type: ignore[attr-defined]
from granian.constants import Interfaces

from .settings import SETTINGS


APPLICATION_TARGET: typing.Final[str] = "whole_app.views:SPELL_APP"


def launch_server() -> None:
    Granian(
        APPLICATION_TARGET,
        address=SETTINGS.server_address,
        port=SETTINGS.port,
        workers=SETTINGS.workers,
        interface=Interfaces.ASGI,
    ).serve()


if __name__ == "__main__":
    launch_server()
