#!/usr/bin/env python3
"""Populate NewMaterial/ from OldMaterial/, driven by course.yml.

Creates one folder per scheduled lecture that declares a `folder:` key, copies
the matching OldMaterial folder's contents in, and copies Homeworks, Textbook
and _shared across wholesale. Lectures with no prior material get an empty
folder with a .gitkeep so git tracks the slot.

Idempotent: existing files in NewMaterial are left alone unless --force.
"""
from __future__ import annotations
import argparse, shutil, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml\n")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
OLD, NEW = REPO_ROOT / "OldMaterial", REPO_ROOT / "NewMaterial"
BULK = ["Homeworks", "Textbook", "_shared"]


def copy_tree(src: Path, dst: Path, force: bool, log: list):
    dst.mkdir(parents=True, exist_ok=True)
    if not src.is_dir():
        return
    for item in sorted(src.rglob("*")):
        if item.is_dir():
            continue
        target = dst / item.relative_to(src)
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        log.append(target.relative_to(REPO_ROOT).as_posix())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite existing NewMaterial files")
    args = ap.parse_args()

    course = yaml.safe_load((REPO_ROOT / "course.yml").read_text(encoding="utf-8"))
    copied, created, missing = [], [], []

    for entry in course["schedule"]:
        folder = entry.get("folder")
        if not folder:
            continue
        src, dst = OLD / folder, NEW / folder
        copy_tree(src, dst, args.force, copied)
        if not any(dst.iterdir()):
            (dst / ".gitkeep").touch()
            created.append(folder)
        if not src.is_dir():
            missing.append(folder)

    for name in BULK:
        copy_tree(OLD / name, NEW / name, args.force, copied)

    print(f"copied {len(copied)} files into NewMaterial/")
    if created:
        print(f"empty lecture slots (.gitkeep): {', '.join(created)}")
    if missing:
        print(f"no OldMaterial source: {', '.join(missing)}")


if __name__ == "__main__":
    main()
