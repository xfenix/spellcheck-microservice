"""Test __main__.py."""
import runpy


class FakeGunicorn:
    """Fake gunicorn."""

    def __init__(self, *_, **__):
        """Init."""

    def run(self, *_, **__):
        """Run."""


def test_main_py(monkeypatch):
    """Test __main__.py."""
    monkeypatch.setattr("gunicorn.app.base.BaseApplication", FakeGunicorn)
    runpy.run_module("whole_app.__main__", run_name="__main__")
