import json

from skilltools import REPO, frontmatter, iter_skills


def test_marketplace_lists_existing_plugins():
    m = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    assert m["name"] == "public-skills"
    assert m["plugins"], "marketplace lists no plugins"
    for p in m["plugins"]:
        root = REPO / p["source"]
        assert (root / ".claude-plugin/plugin.json").is_file(), p["name"]
        assert json.loads((root / ".claude-plugin/plugin.json").read_text())["name"] == p["name"]


def test_every_skill_name_matches_its_folder():
    skills = iter_skills()
    assert skills, "no skills found"
    for s in skills:
        fm = frontmatter(s)
        assert fm["name"] == s.parent.name, s
        assert len(fm["name"]) <= 64
        assert 0 < len(fm["description"]) <= 1024, s


def test_skill_version_matches_plugin_version():
    for s in iter_skills():
        plugin = json.loads((s.parents[2] / ".claude-plugin/plugin.json").read_text())
        assert frontmatter(s)["metadata"]["version"] == plugin["version"], s
