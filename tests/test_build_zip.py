import sys
import zipfile

from skilltools import REPO

sys.path.insert(0, str(REPO / "scripts"))
from build_zip import build  # noqa: E402


def test_zip_holds_the_folder_not_loose_files(tmp_path):
    skill = REPO / "plugins/business-walkthrough/skills/business-walkthrough"
    z = build(skill, tmp_path)
    assert z.name == "business-walkthrough.zip"
    names = zipfile.ZipFile(z).namelist()
    assert "business-walkthrough/SKILL.md" in names
    assert all(n.startswith("business-walkthrough/") for n in names)
    assert not any("__pycache__" in n or n.endswith(".DS_Store") for n in names)
