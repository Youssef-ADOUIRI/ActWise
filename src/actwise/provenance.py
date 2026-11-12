"""What made an output: a file's hash and the commit. Standard library only, so the
training notebook can import it without the project's dependencies.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def file_hash(path: Path) -> str:
    """The first 16 hex digits of a file's SHA-256: it names weights that have no Hub commit."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()[:16]


def git_commit() -> str:
    """Short commit hash, marked "-dirty" if the code or data have uncommitted changes."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"  # not a git checkout
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "src", "data", "evals/*.py"],
        capture_output=True,
        text=True,
    )
    return commit.stdout.strip() + ("-dirty" if status.stdout.strip() else "")
