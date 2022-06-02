"""Application server here.

This file meant only for basic workers wrappers and fastapi exposure.
For end-points look in views.py
"""
from gunicorn.app.base import BaseApplication
from uvicorn.workers import UvicornWorker

from .settings import SETTINGS
from .views import SPELL_APP


if __name__ == "__main__":
    BaseApplication(
        SPELL_APP,
        {
            "worker_class": UvicornWorker,
            "bind": f"0.0.0.0:{SETTINGS.port}",
            "workers": SETTINGS.workers,
        },
    ).run()
