"""User dictionaries implementation."""
import typing


class UserDictProtocol(typing.Protocol):
    """Default storage protocol/interface."""

    def prepare(self: "UserDictProtocol", user_name: str) -> "UserDictProtocol":
        """Prepare class for user name."""

    async def save_record(self: "UserDictProtocol", exception_word: str) -> None:
        """Save record to user dictionary."""

    async def remove_record(self: "UserDictProtocol", exception_word: str) -> None:
        """Remove record from user dictionary."""

    async def fetch_records(self: "UserDictProtocol") -> list[str]:
        """Fetch records from user dictionary."""
