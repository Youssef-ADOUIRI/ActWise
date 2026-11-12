import re

from actwise.provenance import file_hash, git_commit


def test_git_commit_names_this_checkout():
    """A short hash, marked "-dirty" when the code has changes; "unknown" outside git."""
    assert re.fullmatch(r"[0-9a-f]{7,40}(-dirty)?|unknown", git_commit())


def test_file_hash_reads_the_bytes(tmp_path):
    """Equal bytes give equal hashes of 16 hex digits, whatever the file name."""
    (tmp_path / "a").write_bytes(b"weights")
    (tmp_path / "b").write_bytes(b"weights")

    assert file_hash(tmp_path / "a") == file_hash(tmp_path / "b")
    assert re.fullmatch(r"[0-9a-f]{16}", file_hash(tmp_path / "a"))
