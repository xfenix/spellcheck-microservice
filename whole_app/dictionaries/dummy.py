"""Dummy provider."""


class DummyProvider:
    """Dummy provider for user dictionaries.

    In case if you want to use dcitionaries API, but don't want to do
    actual work.
    """

    def prepare(self, _: str) -> "DummyProvider":
        """Initialize class from user id."""
        return self

    async def save_record(self, _: str) -> None:
        """Save record to user dictionary."""

    async def remove_record(self, _: str) -> None:
        """Remove record from user dictionary."""

    async def fetch_records(self) -> list[str]:
        """Fetch records from user dictionary."""
        return []
