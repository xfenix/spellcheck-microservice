#!/usr/bin/env python3
"""Simple dockerhub readme generator."""
import pathlib
import re
import shlex
import subprocess


_LAST_TAG_HASH: str = subprocess.check_output(shlex.split("git rev-list --tags --max-count=1")).strip().decode()
LAST_TAG_VALUE: str = subprocess.check_output(shlex.split(f"git describe --tags {_LAST_TAG_HASH}")).strip().decode()
LAST_TAG_VALUE = LAST_TAG_VALUE.lstrip("v")
README_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent / "README.md"
NEW_CONTENT: str = re.sub(r"\#\# Development.*", r"", README_PATH.read_text(), flags=re.I | re.S).strip()
NEW_CONTENT = re.sub(
    r"(xfenix/spellcheck-microservice\:)(\d{1,}\.\d{1,}\.\d{1,})",
    r"\g<1>" + LAST_TAG_VALUE,
    NEW_CONTENT,
    flags=re.I | re.S,
)
README_PATH.write_text(NEW_CONTENT + "\n")
