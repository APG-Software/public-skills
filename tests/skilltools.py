import pathlib
import re

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent


def iter_skills():
    return sorted(REPO.glob("plugins/*/skills/*/SKILL.md"))


def _split(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise AssertionError(f"{path}: no frontmatter")
    return m.group(1), m.group(2)


def frontmatter(path):
    return yaml.safe_load(_split(path)[0])


def body(path):
    return _split(path)[1]


def say_blocks(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    return re.findall(r"```say\n(.*?)\n```", text, re.S)
