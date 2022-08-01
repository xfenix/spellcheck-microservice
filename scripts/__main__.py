#!/usr/bin/env python3
"""Simple dockerhub readme generator."""
import argparse
import pathlib
import re
import sys

from ._helpers import parse_last_git_tag, replace_tag_in_readme


PARENT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
README_PATH: pathlib.Path = PARENT_DIR / "README.md"


def _update_dockerhub_readme():
    new_content: str = re.sub(r"\#\# Development.*", r"", README_PATH.read_text(), flags=re.I | re.S).strip()
    new_content = replace_tag_in_readme(new_content, parse_last_git_tag())
    README_PATH.write_text(new_content + "\n")


def _update_readme():
    from whole_app.settings import SETTINGS

    new_content: str = README_PATH.read_text()
    settings_schema: dict = SETTINGS.schema()["properties"]
    pack_of_readme_lines: list = []
    for _, props in settings_schema.items():
        settings_env_key: str = props["env_names"].pop().upper()
        if "description" not in props:
            print("-", settings_env_key, "not be available in README")
            continue
        default_value: any = props["default"] if "default" in props else None
        if default_value == "":
            default_value = "''"
        allowed_restrictions: str = (
            ""
            if "exclusiveMinimum" not in props
            else f", allowed values from `{props['exclusiveMinimum'] + 1}`"
            + (f"to `{props['exclusiveMaximum'] - 1}`" if "exclusiveMaximum" in props else "")
        )
        pack_of_readme_lines.append(
            f'`{settings_env_key}` {props["description"].rstrip(".")}. '
            f"Default is `{default_value}`{allowed_restrictions}"
        )
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

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("action")
    arguments_list: argparse.Namespace = parser.parse_args()
    match arguments_list.action:
        case "update-dockerhub-readme":
            _update_dockerhub_readme()
        case "update-readme":
            _update_readme()
        case _:
            print("Unknown action")
