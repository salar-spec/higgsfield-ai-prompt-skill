#!/usr/bin/env python3
"""
build_skill_zip.py
==================
Build the ZIP that claude.ai's Customize > Skills upload expects. Stdlib only.

claude.ai looks for `<skill-name>/SKILL.md` inside the archive, the folder
name must equal the `name` in SKILL.md's frontmatter, and the description is
capped at 1,024 characters. Built by hand (clone, rename, zip the folder not
its contents) this goes wrong easily, above all on Windows; this script does it
in one step and checks the result.

What goes in: everything the skill reads while working: SKILL.md, skills/,
templates/, specs/, db/, scripts/ and the root reference files. What stays out:
maintainer-only folders (tests/, evals/, .github/, .claude/), the user-guide
build (docs/user-guide/, assets/fonts/), docs/archive/, workspace/ (a user's
files never ship), dotfiles and Python caches.

Usage (from the repo root, or anywhere):
  python3 scripts/build_skill_zip.py                 # → dist/<name>.zip
  python3 scripts/build_skill_zip.py --out my.zip
  python3 scripts/build_skill_zip.py --list          # print what would go in
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Top-level folders that never ship, and nested ones (as path prefixes).
EXCLUDED_DIRS = {".git", ".github", ".claude", "tests", "evals", "workspace", "dist", "build"}
EXCLUDED_PREFIXES = ("docs/archive/", "docs/user-guide/", "assets/fonts/")
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
DESCRIPTION_MAX = 1024  # Agent Skills specification limit, enforced by claude.ai


def _frontmatter(skill_md: Path) -> tuple[str, str]:
    """`name` and `description` from SKILL.md's YAML frontmatter (the subset
    this repo uses: plain scalars and `>` folded blocks)."""
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError(f"{skill_md}: no frontmatter")
    lines = m.group(1).splitlines()
    fields, i = {}, 0
    while i < len(lines):
        km = re.match(r"^([a-z_]+):\s*(.*)$", lines[i])
        if not km:
            i += 1
            continue
        key, value = km.group(1), km.group(2).strip()
        if value in (">", ">-", "|", "|-"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            sep = " " if value.startswith(">") else "\n"
            value = sep.join(b for b in block if b) if sep == " " else "\n".join(block).strip()
        else:
            value = value.strip("'\"")
            i += 1
        fields[key] = value
    return fields.get("name", ""), fields.get("description", "")


def check_frontmatter(name: str, description: str, folder: str) -> list[str]:
    """The problems claude.ai would reject the upload for; empty when fine."""
    problems = []
    if not NAME_RE.match(name):
        problems.append(f"name {name!r} must be 1-64 lowercase letters, digits or hyphens")
    if folder != name:
        problems.append(f"folder {folder!r} must equal the name {name!r}")
    if not description:
        problems.append("description is empty")
    elif len(description) > DESCRIPTION_MAX:
        problems.append(f"description is {len(description)} characters (max {DESCRIPTION_MAX})")
    return problems


def is_shipped(rel: str) -> bool:
    """True for a repo-relative POSIX path that belongs in the skill ZIP."""
    parts = rel.split("/")
    if parts[0] in EXCLUDED_DIRS or rel.startswith(EXCLUDED_PREFIXES):
        return False
    if any(p.startswith(".") for p in parts) or "__pycache__" in parts:
        return False
    return not rel.endswith((".pyc", ".pyo"))


def source_files(root: Path = REPO_ROOT) -> list[str]:
    """The repo's files as repo-relative POSIX paths: the tracked files in a
    git checkout (so local scratch never ships), every file in a plain
    download of the repo."""
    if (root / ".git").exists():
        try:
            out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                                 capture_output=True, check=True).stdout
            return sorted(p for p in out.decode("utf-8").split("\0")
                          if p and (root / p).is_file())
        except (OSError, subprocess.CalledProcessError):
            pass
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def build(out: Path, root: Path = REPO_ROOT) -> tuple[str, list[str]]:
    """Write the ZIP to `out`; return the skill name and the files it holds."""
    name, description = _frontmatter(root / "SKILL.md")
    problems = check_frontmatter(name, description, name)
    if problems:
        raise ValueError("; ".join(problems))
    files = [rel for rel in source_files(root) if is_shipped(rel)]
    if "SKILL.md" not in files:
        raise ValueError("SKILL.md is missing from the files to ship")
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".partial")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in files:
            info = zipfile.ZipInfo(f"{name}/{rel}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, (root / rel).read_bytes())
    tmp.replace(out)
    return name, files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the claude.ai skill upload ZIP.")
    ap.add_argument("--out", type=Path, help="output path (default: dist/<name>.zip)")
    ap.add_argument("--list", action="store_true", help="print the files and exit")
    args = ap.parse_args(argv)
    try:
        name, description = _frontmatter(REPO_ROOT / "SKILL.md")
        if args.list:
            for rel in source_files():
                if is_shipped(rel):
                    print(f"{name}/{rel}")
            return 0
        out = args.out or REPO_ROOT / "dist" / f"{name}.zip"
        name, files = build(out)
    except (OSError, ValueError) as e:
        print(f"build_skill_zip: {e}", file=sys.stderr)
        return 1
    size = out.stat().st_size / 1_048_576
    print(f"Built {out} ({len(files)} files, {size:.1f} MB)")
    print(f"Upload it in claude.ai under Customize > Skills; it appears as '{name}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
