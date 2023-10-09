"""Application server here.

This file meant only for basic workers wrappers and fastapi exposure.
For end-points look in views.py
"""
import typing

import fastapi
from gunicorn.app.base import BaseApplication

from .settings import SETTINGS
from .views import SPELL_APP


# pylint: disable=abstract-method
class GunicornCustomApplication(BaseApplication):  # type: ignore[misc]
    def load_config(self: "GunicornCustomApplication") -> None:
        _options: typing.Final[dict[str, str | int]] = {
            "worker_class": "uvicorn.workers.UvicornWorker",
            "bind": f"0.0.0.0:{SETTINGS.port}",
            "workers": SETTINGS.workers,
        }
        for key, value in _options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self: "GunicornCustomApplication") -> fastapi.FastAPI:
        return SPELL_APP


if __name__ == "__main__":
    GunicornCustomApplication().run()
