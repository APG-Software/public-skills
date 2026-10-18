"""Zip one skill folder for Customize -> Skills -> Upload a skill."""
import pathlib
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parent.parent


def build(skill_dir, out_dir):
    skill_dir, out_dir = pathlib.Path(skill_dir), pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.name != ".DS_Store":
                z.write(f, f"{skill_dir.name}/{f.relative_to(skill_dir).as_posix()}")
    return out


if __name__ == "__main__":
    name = sys.argv[1]
    matches = list(REPO.glob(f"plugins/*/skills/{name}"))
    if len(matches) != 1:
        sys.exit(f"skill '{name}' not found exactly once")
    print(build(matches[0], REPO / "dist"))
