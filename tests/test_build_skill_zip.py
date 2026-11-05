"""The claude.ai upload ZIP (scripts/build_skill_zip.py).

claude.ai wants `<name>/SKILL.md` at the top of the archive, the folder named
like SKILL.md's `name`, and a description of at most 1,024 characters. The
skill's own scripts must still run from the unpacked ZIP.
"""

import os
import subprocess
import sys
import zipfile

import pytest

import build_skill_zip as bz
from conftest import REPO


@pytest.mark.parametrize("rel,shipped", [
    ("SKILL.md", True),
    ("skills/higgsfield-models/SKILL.md", True),
    ("specs/model-specs.json", True),
    ("scripts/preflight.py", True),
    ("db/ledger/README.md", True),
    ("docs/claude-ai.md", True),
    ("tests/test_ledger.py", False),
    ("evals/spec-claims.json", False),
    (".github/workflows/validate.yml", False),
    (".claude/settings.json", False),
    ("workspace/input/README.md", False),
    ("docs/archive/HISTORY.md", False),
    ("docs/user-guide/MANIFEST.json", False),
    ("assets/fonts/DejaVuSansMono.ttf", False),
    (".gitignore", False),
    ("scripts/__pycache__/preflight.cpython-313.pyc", False),
])
def test_what_ships(rel, shipped):
    assert bz.is_shipped(rel) is shipped


def test_frontmatter_problems():
    assert bz.check_frontmatter("higgsfield", "Writes prompts.", "higgsfield") == []
    assert bz.check_frontmatter("Higgsfield", "x", "Higgsfield")       # capitals
    assert bz.check_frontmatter("higgsfield", "x", "higgsfield-main")  # folder ≠ name
    assert bz.check_frontmatter("higgsfield", "", "higgsfield")        # no description
    assert any("1025 characters" in p
               for p in bz.check_frontmatter("higgsfield", "x" * 1025, "higgsfield"))


def test_the_root_skill_meets_claude_ai_limits():
    name, description = bz._frontmatter(REPO / "SKILL.md")
    assert name == "higgsfield"
    assert 0 < len(description) <= bz.DESCRIPTION_MAX
    assert bz.check_frontmatter(name, description, name) == []


def test_build_layout_and_determinism(tmp_path):
    out = tmp_path / "higgsfield.zip"
    name, files = bz.build(out)
    names = zipfile.ZipFile(out).namelist()
    assert all(n.startswith(f"{name}/") for n in names)
    for must in ("SKILL.md", "scripts/preflight.py", "scripts/higgsfield_memory.py",
                 "specs/model-specs.json", "db/filter-memory.json", "model-guide.md"):
        assert f"{name}/{must}" in names
    assert not [n for n in names if n.split("/")[1] in ("tests", "evals", ".github", ".claude")]
    first = out.read_bytes()
    bz.build(out)
    assert out.read_bytes() == first                     # same input, same bytes
    assert not list(tmp_path.glob("*.partial"))


def test_the_skill_scripts_run_from_the_unpacked_zip(tmp_path):
    out = tmp_path / "higgsfield.zip"
    bz.build(out)
    zipfile.ZipFile(out).extractall(tmp_path / "unpacked")
    skill = tmp_path / "unpacked" / "higgsfield"
    env = {**os.environ, "HOME": str(tmp_path / "home")}
    env.pop("HF_DB_DIR", None)
    for args in (["scripts/preflight.py", "--model", "kling3_0", "--strict"],
                 ["scripts/higgsfield_memory.py", "health"],
                 ["scripts/seedance_lint.py", "A slow push-in on a rainy street."]):
        r = subprocess.run([sys.executable, *args], cwd=skill, env=env,
                           capture_output=True, text=True, timeout=120)
        assert r.returncode == 0, (args, r.stdout[-400:], r.stderr[-400:])
