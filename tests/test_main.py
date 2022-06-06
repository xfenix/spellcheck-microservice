# pylint: disable=no-member
"""Test __main__.py."""
import runpy


class FakeGunicorn:
    """Fake gunicorn."""

    def __init__(self, *_, **__):
        """Init."""

    @property
    def cfg(self):
        """Fake config object."""
        return self

    @property
    def settings(self):
        """Fake settings object."""
        return {
            "bind": None,
            "workers": 666_13,
        }

    def set(self, _, __):
        """Fake setter for «config» object."""

    def run(self, *_, **__):
        """Faky run."""
        self.load_config()
        self.load()


def test_main_py(monkeypatch):
    """Test __main__.py."""
    monkeypatch.setattr("gunicorn.app.base.BaseApplication", FakeGunicorn)
    runpy.run_module("whole_app.__main__", run_name="__main__")
