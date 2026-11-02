import re

from skilltools import REPO, body, say_blocks
from wordlists import BANNED, TIME_PATTERNS

SKILL = REPO / "plugins/business-walkthrough/skills/business-walkthrough/SKILL.md"


def questions():
    return re.findall(r"^\*\*Q(\d+)\.\*\* (.+)$", body(SKILL), re.M)


def test_parts_in_order():
    text = body(SKILL)
    heads = ["Part 0 of 6", "Part 1 of 6", "Part 2 of 6", "Part 3 of 6", "Part 4 of 6",
             "Part 5 of 6", "Part 6 of 6", "Check and finish"]
    positions = [text.find(h) for h in heads]
    assert all(p >= 0 for p in positions), dict(zip(heads, positions))
    assert positions == sorted(positions)


def test_at_most_twenty_numbered_questions():
    nums = [int(n) for n, _ in questions()]
    assert nums == list(range(1, len(nums) + 1))
    assert 10 <= len(nums) <= 20


def test_client_facing_words_are_clean():
    for block in say_blocks(SKILL):
        low = block.lower()
        for w in BANNED:
            assert w not in low, f"banned '{w}' in: {block[:80]}"


def test_no_time_or_volume_questions():
    for _, q in questions():
        for pat in TIME_PATTERNS:
            assert not re.search(pat, q.lower()), f"{pat} in Q: {q}"


def test_required_rules_are_stated():
    text = body(SKILL).lower()
    for needle in ("documentation", "view a / view b", "starter page", "numbered",
                   "not a specific real job", "amber", "parking list",
                   "fathom", "self-check", "ridgeline steel", "context bundle",
                   "draft-page.json", "service line", "journey", "idea"):
        assert needle in text, needle


def test_deflections_present():
    joined = "\n".join(say_blocks(SKILL)).lower()
    assert "that's what the team sessions are for" in joined
    assert "adam will want to see those systems first" in joined


def test_walkthrough_file_is_looked_for_first():
    text = body(SKILL)
    start = text.find("## Before you start")
    assert start >= 0
    section = text[start:text.find("## Part 0 of 6")]
    file_pos = section.find("walkthrough: business")
    bundle_pos = section.find("context bundle", file_pos if file_pos >= 0 else 0)
    assert 0 <= file_pos < bundle_pos, "the walkthrough file must be checked before the bundle"
    assert "Carrying on from a walkthrough file" in section
    assert "the most runs" in section
