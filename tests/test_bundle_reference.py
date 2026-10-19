import json
import re

from skilltools import REPO

REF = REPO / "plugins/business-walkthrough/skills/business-walkthrough/references/context-bundle.md"
DRAFT_KEYS = {"business", "service_lines", "journeys", "behind_the_scenes", "departments",
              "sites", "systems"}


def test_reference_names_the_four_parts():
    t = REF.read_text(encoding="utf-8")
    for name in ("about.json", "starter-page.md", "draft-page.json", "their-documents/"):
        assert name in t, name


def test_draft_page_example_parses_with_every_key():
    t = REF.read_text(encoding="utf-8")
    m = re.search(r"```json\n(\{.*?\})\n```", t, re.S)
    assert m, "no json example"
    d = json.loads(m.group(1))
    assert DRAFT_KEYS <= set(d), DRAFT_KEYS - set(d)
    assert all(l.get("status") == "draft" for l in d["service_lines"])
    lines = {l["id"] for l in d["service_lines"]}
    assert lines == {j["line"] for j in d["journeys"]}
