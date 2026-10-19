import re

import yaml

from skilltools import REPO

REF = REPO / "plugins/business-walkthrough/skills/business-walkthrough/references/walkthrough-file.md"
KEYS = {"walkthrough", "walkthrough_version", "status", "date", "business", "website",
        "in_the_room", "recorded", "page_confirmed", "flows", "reference_jobs",
        "consent_to_send", "sent_via", "bundle_version", "service_lines"}
SECTIONS = ["## What they sell", "## The customer's journey", "## Teams and sites",
            "## Systems by step", "## How a typical job moves", "## Where work waits",
            "## Ideas and repeated work", "## Parking list", "## Questions log"]


def _example():
    text = REF.read_text(encoding="utf-8")
    m = re.search(r"````markdown\n---\n(.*?)\n---\n(.*?)````", text, re.S)
    assert m, "no worked example"
    return yaml.safe_load(m.group(1)), m.group(2)


def test_example_header_has_every_key():
    header, _ = _example()
    assert KEYS <= set(header), KEYS - set(header)
    assert header["reference_jobs"] == "none"
    assert header["walkthrough"] == "business"


def test_example_has_every_section_in_order():
    _, rest = _example()
    pos = [rest.find(s) for s in SECTIONS]
    assert all(p >= 0 for p in pos) and pos == sorted(pos), dict(zip(SECTIONS, pos))


def test_every_line_is_marked():
    _, rest = _example()
    marks = ("confirmed in the room", "from their documents", "from the website",
             "assumed", "UNCONFIRMED")
    bullets = [l for l in rest.splitlines() if l.startswith("- ") and "## Parking" not in l]
    unmarked = [b for b in bullets if not any(m in b for m in marks) and "→" not in b]
    assert not unmarked, unmarked[:3]


def test_no_names_emails_or_counts_in_example():
    _, rest = _example()
    assert "@" not in rest
    assert not re.search(r"\b\d+\s+(people|staff|fte)\b", rest.lower())
