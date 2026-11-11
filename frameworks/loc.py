"""Lines of code for frameworks/COMPARISON.md, without blank lines, comments, docstrings or imports.

    uv run python frameworks/loc.py

Each side counts what it needs and the other side doesn't. Both classifiers share
`agent/schemas.py`, `accept()`, `uncited()` and `ai_act_articles()`, which are counted
for neither. Hand-written retrieval counts the code that system H runs.
"""

from __future__ import annotations

import ast
from pathlib import Path

SHARED = {
    "Articles",
    "ClassificationError",
    "ClassifyOutcome",
    "ai_act_articles",
    "uncited",
    "accept",
}
SIDES: dict[str, list[tuple[str, set[str] | None]]] = {  # file, top-level names (None: all)
    "retrieval, hand-written (H)": [
        ("src/actwise/retrieval/dense.py", None),
        ("src/actwise/retrieval/stores.py", {"Store", "NumpyStore"}),
        (
            "src/actwise/retrieval/embedders.py",
            {"Embedder", "l2_normalize", "SentenceTransformerEmbedder"},
        ),
        ("src/actwise/retrieval/systems.py", {"dense", "minilm"}),
    ],
    "retrieval, LlamaIndex (K)": [("frameworks/llamaindex_pipeline.py", None)],
    "classifier, hand-written agent": [("src/actwise/agent/classifier.py", None)],
    "classifier, LangGraph": [("frameworks/langgraph_classifier.py", None)],
}


def names_of(node: ast.stmt) -> set[str]:
    """The names a top-level statement defines."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    targets = node.targets if isinstance(node, ast.Assign) else [getattr(node, "target", None)]
    return {t.id for t in targets if isinstance(t, ast.Name)}


def code_lines(path: Path, only: set[str] | None = None) -> int:
    """Lines of code of the file's top-level statements named in `only` (all if None)."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines: set[int] = set()
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        defined = names_of(node)
        if not defined & SHARED if only is None else defined & only:
            lines.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    owners = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    for owner in ast.walk(tree):  # docstrings
        if isinstance(owner, owners) and ast.get_docstring(owner) is not None:
            first = owner.body[0]
            lines -= set(range(first.lineno, (first.end_lineno or first.lineno) + 1))
    text = source.splitlines()
    return sum(1 for n in lines if text[n - 1].strip() and not text[n - 1].strip().startswith("#"))


def main() -> None:
    """Print each side's count, with the files behind it."""
    for side, files in SIDES.items():
        counts = [(name, code_lines(Path(name), only)) for name, only in files]
        detail = ", ".join(f"{Path(name).name} {n}" for name, n in counts)
        print(f"{side}: {sum(n for _, n in counts)} ({detail})")


if __name__ == "__main__":
    main()
