"""Helper functions."""
import re
import shlex
import subprocess


def parse_last_git_tag() -> str:
    """Return last git tag."""
    last_tag_hash: str = subprocess.check_output(shlex.split("git rev-list --tags --max-count=1")).strip().decode()
    return subprocess.check_output(shlex.split(f"git describe --tags {last_tag_hash}")).strip().decode().lstrip("v")


def replace_tag_in_readme(readme_text: str, new_tag: str) -> str:
    """Place new tag in README text."""
    return re.sub(
        r"(xfenix/spellcheck-microservice\:)(\d{1,}\.\d{1,}\.\d{1,})",
        r"\g<1>" + new_tag,
        readme_text,
        flags=re.I | re.S,
    )
