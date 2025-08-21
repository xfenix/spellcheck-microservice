import os
import re
import shlex
import subprocess
import typing


def parse_last_git_tag() -> str:
    environment_ref_name_raw: typing.Final[str | None] = os.getenv("GITHUB_REF_NAME")
    if environment_ref_name_raw is not None:
        environment_ref_name: str = environment_ref_name_raw.lstrip("v")
        if re.fullmatch(r"\d+\.\d+\.\d+", environment_ref_name):
            return environment_ref_name
        return "latest"

    git_tags_command: typing.Final[list[str]] = shlex.split(
        "git rev-list --tags --max-count=1",
    )
    last_tag_hash: typing.Final[str] = subprocess.check_output(git_tags_command).strip().decode()  # noqa: S603
    describe_command: typing.Final[list[str]] = shlex.split(
        f"git describe --tags {last_tag_hash}",
    )
    return subprocess.check_output(describe_command).strip().decode().lstrip("v")  # noqa: S603


def replace_tag_in_readme(readme_text: str, new_tag: str) -> str:
    return re.sub(
        r"(xfenix/spellcheck-microservice\:)([\w\.-]+)",
        r"\g<1>" + new_tag,
        readme_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

