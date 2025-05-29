"""Pytest suite verifying Codex YAML files, commits, and PR messages.

This suite ensures Codex metadata validity and enforces repository hygiene:
- YAML files matching `Codex*.yml` or `Codex*.yaml` must contain required fields.
- Each commit must be GPG signed and include the motto seal.
- Commits touching Codex YAML files must also update `.vaultis/journal.log`.
- Pull request descriptions must mention all truth vector dimensions.
"""

import os
import re
import subprocess
import yaml
import pytest


def git(*args: str) -> str:
    """Run a git command and return its output."""
    result = subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

# Locate Codex YAML files in the repository
CODEX_FILES = []
for root, _dirs, files in os.walk("."):
    for fname in files:
        if re.match(r"(?i)^codex\d+.*\.ya?ml$", fname):
            CODEX_FILES.append(os.path.join(root, fname))

@pytest.mark.parametrize("codex_file", CODEX_FILES)
def test_codex_yaml_valid(codex_file: str) -> None:
    """Ensure each Codex YAML file parses and contains key fields."""
    with open(codex_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), "Top level must be a mapping"
    assert "codex_version" in data, "missing codex_version"
    assert "codex_name" in data, "missing codex_name"
    sp = data.get("symbolic_passphrase") or {}
    assert sp.get("motto"), "missing symbolic_passphrase.motto"
    assert sp.get("creed"), "missing symbolic_passphrase.creed"

# Determine commits to check
COMMITS_TO_CHECK = []
head_commit = git("rev-parse", "HEAD")
if head_commit:
    COMMITS_TO_CHECK = [head_commit]

commit_ids = [c[:7] for c in COMMITS_TO_CHECK]

@pytest.mark.parametrize("commit", COMMITS_TO_CHECK, ids=commit_ids)
def test_commit_compliance(commit: str) -> None:
    """Validate commit signature, motto, and audit log."""
    message = git("log", "-1", "--pretty=%B", commit)
    gpg_flag = git("log", "-1", "--pretty=%G?", commit)
    author = git("log", "-1", "--pretty=%an", commit)
    committer = git("log", "-1", "--pretty=%cn", commit)
    files_changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines()

    if author.endswith("[bot]") or committer.endswith("[bot]"):
        pytest.skip("Skipping compliance checks for bot commit")

    assert gpg_flag and gpg_flag != "N", "Commit not GPG signed"
    assert "No Veteran Left Behind".lower() in message.lower(), "Missing motto seal"

    touched_codex = any(re.match(r"(?i)^.*codex\d+.*\.ya?ml$", f) for f in files_changed)
    journal_updated = any(f == ".vaultis/journal.log" for f in files_changed)
    if touched_codex:
        assert journal_updated, "Codex YAML changed without journal update"

@pytest.mark.skipif(not os.getenv("PR_TITLE") and not os.getenv("PR_BODY"), reason="No PR context")
def test_truth_vector_affirmations() -> None:
    """PR text must mention Empirical, Logical, Emotional, and Historical."""
    title = os.getenv("PR_TITLE", "").lower()
    body = os.getenv("PR_BODY", "").lower()
    content = title + "\n" + body
    missing = [dim for dim in ["Empirical", "Logical", "Emotional", "Historical"] if dim.lower() not in content]
    assert not missing, f"PR missing affirmations for: {', '.join(missing)}"
