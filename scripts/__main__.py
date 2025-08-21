#!/usr/bin/env python3
"""Simple dockerhub readme generator."""

import argparse
import contextlib
import json
import pathlib
import random
import re
import sys
import time
import types
import typing
import xml.etree.ElementTree as ET

from ._helpers import parse_last_git_tag, replace_tag_in_readme
from whole_app.settings import SETTINGS


PARENT_DIR: typing.Final = pathlib.Path(__file__).parent.parent
README_PATH: typing.Final = PARENT_DIR / "README.md"
COVERAGE_XML_PATH: typing.Final = pathlib.Path("coverage.xml")
BADGE_JSON_PATH: typing.Final = pathlib.Path(".github/badges/coverage.json")
LOW_BOUNDARY: typing.Final[float] = 60
HIGH_BOUNDARY: typing.Final[float] = 80
RETRY_ATTEMPTS: typing.Final[int] = 3


def _update_dockerhub_readme() -> None:
    new_content = re.sub(
        r"\#\# Development.*",
        r"",
        README_PATH.read_text(),
        flags=re.IGNORECASE | re.DOTALL,
    ).strip()
    new_content = replace_tag_in_readme(new_content, parse_last_git_tag())
    README_PATH.write_text(new_content + "\n")


def _update_readme() -> None:
    pack_of_readme_lines: list[str] = []
    new_content: str = README_PATH.read_text()
    env_prefix_value: typing.Final = SETTINGS.model_config["env_prefix"]
    for one_field_name, field_properties in SETTINGS.model_fields.items():
        if field_properties.description is None:
            print("-", one_field_name, "not be available in README")  # noqa: T201
            continue
        default_value_beautified: str = (
            "empty string"
            if isinstance(field_properties.default, str) and not field_properties.default
            else f"`{field_properties.default}`"
        )
        one_row_parts = [
            f"`{(env_prefix_value + one_field_name).upper()}`",
            field_properties.description + ".",
            f"Default value is {default_value_beautified}.",
        ]
        if field_properties.metadata:
            validators_buf: list[str] = []
            for one_obj in field_properties.metadata:
                restriction_stringified: str = str(one_obj)
                if any(("BeforeValidator" in restriction_stringified, "StringConstraints" in restriction_stringified)):
                    continue
                validators_buf.append(f"`{restriction_stringified}`")
            if validators_buf:
                one_row_parts.append(f"Restrictions: {', '.join(validators_buf)}")
        pack_of_readme_lines.append(" ".join(one_row_parts))
    automatic_config_readme: str = "* " + "\n* ".join(pack_of_readme_lines)
    new_content = re.sub(
        r"(.*Here is a list of them\:).*?(\#\#\#\s.*)",
        r"\1\n" + automatic_config_readme + r"\n\n\2",
        new_content,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    new_content = replace_tag_in_readme(new_content, parse_last_git_tag())
    README_PATH.write_text(new_content)


def _fetch_xml_text() -> str:
    for _attempt_index in range(RETRY_ATTEMPTS):
        with contextlib.suppress(OSError):
            return COVERAGE_XML_PATH.read_text()
        time.sleep(random.uniform(0.1, 0.3))  # noqa: S311
    error_message: typing.Final = f"Failed to read {COVERAGE_XML_PATH} after {RETRY_ATTEMPTS} attempts"
    raise OSError(error_message)


def _persist_badge_text(badge_text: str) -> None:
    BADGE_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    for _attempt_index in range(RETRY_ATTEMPTS):
        with contextlib.suppress(OSError):
            BADGE_JSON_PATH.write_text(badge_text)
            return
        time.sleep(random.uniform(0.1, 0.3))  # noqa: S311
    error_message: typing.Final = f"Failed to write {BADGE_JSON_PATH} after {RETRY_ATTEMPTS} attempts"
    raise OSError(error_message)


def _build_coverage_badge() -> None:
    xml_source_text: typing.Final[str] = _fetch_xml_text()
    root_element: typing.Final[ET.Element] = ET.fromstring(xml_source_text)  # noqa: S314
    line_rate_text: typing.Final[str | None] = root_element.attrib.get("line-rate")
    if line_rate_text is None:
        missing_attr_message: typing.Final[str] = "Missing 'line-rate' attribute in coverage report"
        raise KeyError(missing_attr_message)
    coverage_percent: typing.Final[float] = float(line_rate_text) * 100.0

    message_text: typing.Final[str] = f"{coverage_percent:.0f}%"
    color_text: str
    if coverage_percent < LOW_BOUNDARY:
        color_text = "#E63946"
    elif coverage_percent < HIGH_BOUNDARY:
        color_text = "#FFB347"
    else:
        color_text = "#2A9D8F"

    badge_mapping: typing.Final[typing.Mapping[str, typing.Any]] = types.MappingProxyType(
        {
            "schemaVersion": 1,
            "label": "coverage",
            "message": message_text,
            "color": color_text,
        },
    )
    _persist_badge_text(json.dumps(dict(badge_mapping)))


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
        case "build-coverage-badge":
            _build_coverage_badge()
        case _:
            print("Unknown action")  # noqa: T201
