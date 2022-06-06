"""Application server here.

This file meant only for basic workers wrappers and fastapi exposure.
For end-points look in views.py
"""
from gunicorn.app.base import BaseApplication
from uvicorn.workers import UvicornWorker

from .settings import SETTINGS
from .views import SPELL_APP


# pylint: disable=abstract-method
class GunicornCustomApplication(BaseApplication):
    """Our easing wrapper around gunicorn."""

    def load_config(self):
        """Load configuration from memory."""
        _options: dict = {
            "worker_class_str": UvicornWorker,
            "bind": f"0.0.0.0:{SETTINGS.port}",
            "workers": SETTINGS.workers,
        }
        for key, value in _options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        """Just return application."""
        return SPELL_APP


if __name__ == "__main__":
    GunicornCustomApplication().run()
