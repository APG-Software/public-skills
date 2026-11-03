import re

import yaml

from skilltools import REPO

REF = REPO / "plugins/business-walkthrough/skills/business-walkthrough/references/walkthrough-file.md"
KEYS = {"walkthrough", "walkthrough_version", "status", "date", "business", "website",
        "in_the_room", "recorded", "page_confirmed", "flows", "reference_jobs",
        "consent_to_send", "sent_via", "bundle_version", "service_lines",
        "updated", "runs", "open_gaps"}
SECTIONS = ["## What they sell", "## The customer's journey", "## Teams and sites",
            "## Systems by step", "## How a typical job moves", "## Where work waits",
            "## Ideas and repeated work", "## Parking list", "## Still open",
            "## Questions log"]


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
             "added by", "assumed", "UNCONFIRMED")
    bullets = [l for l in rest.splitlines() if l.startswith("- ") and "## Parking" not in l]
    unmarked = [b for b in bullets if not any(m in b for m in marks) and "→" not in b]
    assert not unmarked, unmarked[:3]


def test_no_names_emails_or_counts_in_example():
    _, rest = _example()
    assert "@" not in rest
    teams = rest.split("**Teams**", 1)[1].split("\n\n", 1)[0]
    outside = rest.replace(teams, "")
    assert not re.search(r"\b\d+\s+(people|staff|fte)\b", outside.lower()), "a count outside Teams"
    assert all(re.search(r", \d+ people:", l) for l in teams.splitlines() if l.startswith("- "))


def test_example_has_two_runs_in_one_file():
    header, rest = _example()
    runs = header["runs"]
    assert [r["run"] for r in runs] == list(range(1, len(runs) + 1))
    assert len(runs) >= 2
    for r in runs:
        assert {"run", "date", "by", "recorded", "parts"} <= set(r), r
    assert str(header["updated"]) == str(runs[-1]["date"])
    assert "added by" in rest


def test_open_gaps_matches_still_open():
    header, rest = _example()
    section = rest.split("## Still open", 1)[1].split("\n## ", 1)[0]
    items = re.findall(r"^\d+\. ", section, re.M)
    assert header["open_gaps"] == len(items)
    assert (header["status"] == "complete") == (header["open_gaps"] == 0)


def test_questions_log_has_a_run_column():
    _, rest = _example()
    log = rest.split("## Questions log", 1)[1]
    assert log.lstrip().startswith("| Run | Q |")


def test_file_is_named_without_a_date():
    text = REF.read_text(encoding="utf-8")
    assert "`walkthrough-<business-slug>.md`" in text
    assert "-<YYYY-MM-DD>.md" not in text
