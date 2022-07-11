"""User dictionaries implementation."""
import typing


class UserDictProtocol(typing.Protocol):
    """Default storage protocol/interface."""

    def prepare(self, user_name: str) -> "UserDictProtocol":
        """Prepare class for user name."""

    async def save_record(self, exception_word: str) -> None:
        """Save record to user dictionary."""

    async def remove_record(self, exception_word: str) -> None:
        """Remove record from user dictionary."""

    async def fetch_records(self) -> typing.Any:
        """Fetch records from user dictionary."""
