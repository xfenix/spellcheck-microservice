import os
import re
import shlex
import subprocess
import typing


def parse_last_git_tag() -> str:
    last_tag_from_environment: typing.Final[str | None] = os.getenv("GITHUB_REF_NAME")
    if last_tag_from_environment is None:
        git_tags_list: typing.Final = shlex.split(
            "git rev-list --tags --max-count=1",
        )
        last_tag_hash: typing.Final = subprocess.check_output(git_tags_list).strip().decode()  # noqa: S603
        git_tag_description: typing.Final = shlex.split(
            f"git describe --tags {last_tag_hash}",
        )
        return subprocess.check_output(git_tag_description).strip().decode().lstrip("v")  # noqa: S603
    return last_tag_from_environment.lstrip("v")


def replace_tag_in_readme(readme_text: str, new_tag: str) -> str:
    return re.sub(
        r"(xfenix/spellcheck-microservice\:)(\d{1,}\.\d{1,}\.\d{1,})",
        r"\g<1>" + new_tag,
        readme_text,
        flags=re.I | re.S,
    )
