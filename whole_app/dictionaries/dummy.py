"""Dummy provider."""


class DummyProvider:
    """Dummy provider."""

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
