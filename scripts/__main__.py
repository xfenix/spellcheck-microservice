#!/usr/bin/env python3
"""Simple dockerhub readme generator."""
import argparse
import pathlib
import re
import sys
import typing

from ._helpers import parse_last_git_tag, replace_tag_in_readme
from whole_app.settings import SETTINGS


PARENT_DIR: typing.Final = pathlib.Path(__file__).parent.parent
README_PATH: typing.Final = PARENT_DIR / "README.md"


def _update_dockerhub_readme() -> None:
    new_content = re.sub(
        r"\#\# Development.*",
        r"",
        README_PATH.read_text(),
        flags=re.I | re.S,
    ).strip()
    new_content = replace_tag_in_readme(new_content, parse_last_git_tag())
    README_PATH.write_text(new_content + "\n")


def _update_readme() -> None:
    pack_of_readme_lines: list[str] = []
    new_content: str = README_PATH.read_text()
    env_prefix_value: typing.Final = SETTINGS.model_config["env_prefix"]
    for one_field_name, field_properties in SETTINGS.model_fields.items():
        if field_properties.description is None:
            print("-", one_field_name, "not be available in README")
            continue
        one_row_parts = [
            f"`{(env_prefix_value + one_field_name).upper()}`",
            field_properties.description + ".",
            f"Default value is `{field_properties.default}`.",
        ]
        if field_properties.metadata:
            one_row_parts.append(f"Restrictions is `{field_properties.metadata}`")
        pack_of_readme_lines.append(" ".join(one_row_parts))
    automatic_config_readme: str = "* " + "\n* ".join(pack_of_readme_lines)
    new_content = re.sub(
        r"(.*Here is a list of them\:).*?(\#\#\#\s.*)",
        r"\1\n" + automatic_config_readme + r"\n\n\2",
        new_content,
        flags=re.I | re.M | re.S,
    )
    new_content = replace_tag_in_readme(new_content, parse_last_git_tag())
    README_PATH.write_text(new_content)


if __name__ == "__main__":
    sys.path.append(str(PARENT_DIR.resolve()))

    parser_obj: typing.Final = argparse.ArgumentParser()
    parser_obj.add_argument("action")
    arguments_list: argparse.Namespace = parser_obj.parse_args()
    match arguments_list.action:
        case "update-dockerhub-readme":
            _update_dockerhub_readme()
        case "update-readme":
            _update_readme()
        case _:
            print("Unknown action")  # noqa: T201
