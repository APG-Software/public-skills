import re

from skilltools import REPO
from wordlists import BANNED

REF = REPO / "plugins/business-walkthrough/skills/business-walkthrough/references"


def _read(name):
    return (REF / name).read_text(encoding="utf-8")


def test_pages_are_self_contained():
    for name in ("example-working-page.html", "example-keep-page.html"):
        html = _read(name)
        assert not re.search(r"<script[^>]+src=", html), name
        assert not re.search(r"<link[^>]+href=\"https?:", html), name
        assert "color-scheme:light" in html, name
        assert "prefers-color-scheme: dark" not in html, name
        assert 'class="brand"' in html and "APG Software" in html, name
        assert "<svg" in html, name


def test_waiting_points_only_on_handoffs():
    html = _read("example-working-page.html")
    assert "wp-wait" in html
    for m in re.finditer(r'class="[^"]*wp-wait', html):
        before = html[:m.start()]
        assert before.rfind('class="wp-handoff') > before.rfind('class="wp-team'), \
            "waiting point not inside a hand-off"


def test_keep_page_has_no_waits_names_or_counts():
    html = _read("example-keep-page.html")
    assert "wp-wait" not in html
    assert "wp-fork" not in html
    assert "wp-idea" not in html
    text = re.sub(r"<[^>]+>", " ", html).lower()
    assert not re.search(r"\b\d+\s+(people|staff|fte)\b", text)
    for w in BANNED:
        assert w not in text, w


def test_working_page_shows_lines_ideas_and_repeats():
    html = _read("example-working-page.html")
    for cls in ("wp-lines", "wp-strip", "wp-teams", "wp-lane", "wp-idea", "wp-repeat"):
        assert f'class="{cls}' in html or f' {cls}"' in html or f'class="{cls}"' in html, cls


def test_guide_states_the_layout_and_fallbacks():
    g = _read("living-page.md").lower()
    for needle in ("progress bar", "value-chain strip", "amber", "projector",
                   "update the same artifact", "one new artifact per part",
                   "numbered list grouped by team", "mermaid", "draft-page.json",
                   "dashed", "idea note", "repeat badge", "service line"):
        assert needle in g, needle


def test_guide_says_how_to_draw_from_a_file():
    g = _read("living-page.md").lower()
    for needle in ("## 6. drawn from a file", "coverage bar", "still open", "wp-open",
                   "solid", "dashed", "added by", "never fill it in by guessing"):
        assert needle in g, needle


def test_page_template_is_complete_and_clean():
    html = _read("page-template.html")
    assert not re.search(r"<script[^>]+src=", html)
    assert not re.search(r"<link[^>]+href=\"https?:", html)
    assert "color-scheme:light" in html and "prefers-color-scheme: dark" not in html
    assert 'class="brand"' in html and "APG Software" in html and 'class="foot"' in html
    for cls in ("wp-coverage", "wp-lines", "wp-strip", "wp-lanegrid", "wp-step", "wp-cards",
                "wp-teams", "wp-idea", "wp-repeat", "wp-parking", "wp-open"):
        assert cls in html, cls
    for h in ("What you sell", "The customer's journey", "How a typical job moves",
              "Where work waits", "Teams and sites", "Your systems", "Ideas and repeated work",
              "Parking list", "Still open"):
        assert f"<h2>{h}</h2>" in html, h
    sized = re.sub(r'<span class="size">\d+ people</span>', " ", html)
    sized = re.sub(r"(<div class=\"org-top\">.*?</div>)", " ", sized, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", " ", sized, flags=re.S)).lower()
    assert not re.search(r"\b\d+\s+(people|staff|fte)\b", text), "a count outside the org chart"
    for w in BANNED:
        assert w not in text, w


def test_template_waits_sit_on_handoffs_in_the_swimlane():
    html = _read("page-template.html")
    lanes = re.findall(r'<div class="wp-lanegrid".*?</div></div>', html, re.S)
    assert lanes
    for lane in lanes:
        for m in re.finditer(r'class="wp-wait"', lane):
            before = lane[:m.start()]
            assert before.rfind('class="wp-handoff"') > before.rfind('class="wp-step'), \
                "waiting point not inside a hand-off"


def test_guide_and_skill_point_at_the_template():
    g = _read("living-page.md")
    assert "references/page-template.html" in g and "copy it exactly" in g.lower()
    skill = (REF.parent / "SKILL.md").read_text(encoding="utf-8")
    assert "references/page-template.html" in skill


def test_template_draws_an_org_chart_of_roles():
    html = _read("page-template.html")
    assert 'class="wp-org"' in html and 'class="org-top"' in html
    org = html.split('class="wp-org"', 1)[1].split("</div>\n</div>", 1)[0]
    assert org.count('class="wp-team') >= 3
    assert org.count('class="roles"') >= 3
    g = _read("living-page.md").lower()
    assert "org chart" in g and "roles, each once" in g and "no names" in g


def test_every_department_box_shows_its_size():
    html = _read("page-template.html")
    org = html.split('class="wp-org"', 1)[1].split("</div>\n</div>", 1)[0]
    boxes = re.findall(r'<div class="wp-team[^"]*">(.*?)</div>', org, re.S)
    assert boxes and all(re.search(r'<span class="size">\d+ people</span>', b) for b in boxes)
    g = _read("living-page.md").lower()
    assert "how many people are in it" in g
