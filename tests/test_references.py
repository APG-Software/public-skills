from skilltools import REPO, body

SK = REPO / "plugins/business-walkthrough/skills/business-walkthrough"
DEPTS = ["Sales and estimating", "Design and drawings", "Engineering", "Procurement",
         "Production scheduling", "Manufacture", "Quality", "Stock and dispatch",
         "Install", "Invoicing and accounts", "People and culture", "In-house software"]


def test_starter_page_format_is_defined():
    t = (SK / "references/starter-page.md").read_text(encoding="utf-8")
    for h in ("## What you make", "## Who buys, and how work arrives", "## Sites and regions",
              "## Your teams", "## Tools and systems", "## Where the sources don't agree"):
        assert h in t, h
    assert "Source:" in t
    assert "confirmation" in t.lower()


def test_process_list_covers_a_manufacturer():
    t = (SK / "references/processes-manufacturing.md").read_text(encoding="utf-8")
    for d in DEPTS:
        assert f"## {d}" in t, d
    assert "not a list of costs" in t.lower()


def test_skill_points_at_both():
    b = body(SK / "SKILL.md")
    assert "references/starter-page.md" in b
    assert "references/processes-manufacturing.md" in b
