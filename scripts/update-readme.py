#!/usr/bin/env python3
"""Simple dockerhub readme generator."""
import pathlib
import re
import sys


PARENT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent


def run_main():
    """Main fn."""
    sys.path.append(str(PARENT_DIR.resolve()))

    from whole_app.settings import SETTINGS

    readme_path: pathlib.Path = PARENT_DIR / "README.md"
    new_content: str = readme_path.read_text()
    settings_schema: dict = SETTINGS.schema()["properties"]
    pack_of_readme_lines: list = []
    for _, props in settings_schema.items():
        settings_env_key: str = props["env_names"].pop().upper()
        if "description" not in props:
            print("-", settings_env_key, "not be available in README")
            continue
        default_value: any = props["default"] if "default" in props else None
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
    automatic_config_readme: str = "\n".join(pack_of_readme_lines)
    new_content = re.sub(
        r"Here is a list of them\:(.*)(\#\# Development.*)",
        r"\0\n" + automatic_config_readme + r"\n\n\2",
        new_content,
        flags=re.I | re.M | re.S,
    )
    readme_path.write_text(new_content)


run_main()
