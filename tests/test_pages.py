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
        assert "prefers-color-scheme: dark" in html, name
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
