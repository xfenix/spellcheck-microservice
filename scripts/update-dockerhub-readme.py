#!/usr/bin/env python3
"""Simple dockerhub readme generator."""
import pathlib
import re


README_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent / "README.md"
NEW_CONTENT: str = re.sub(r"\#\# Development.*", r"", README_PATH.read_text(), flags=re.I | re.S).strip()
README_PATH.write_text(NEW_CONTENT)
