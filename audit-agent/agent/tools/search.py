"""

Search the repository for files containing a query string and return contextual snippets so the agent can decide what to read next.


search_repo.py

This tool allows the agent to search through a codebase for a given query.
It returns file paths and small code snippets where the query appears.

Design goals:
- Deterministic
- Read-only
- Fast enough for medium/large repos
- No hidden side effects

This tool is the agent's "eyes" for discovering where to look next.
"""

from pathlib import Path
from typing import List, Dict

def search_repo(
    repo_root: Path,
    query: str,
    max_results: int = 10,
    context_lines: int = 2,
 ) -> List[Dict]:

    """
    Search all text files in the repository for a query string.

    Parameters
    ----------
    repo_root : Path
    Root directory of the repository to search.
    query : str
    The string to search for (case-insensitive).
    max_results : int
    Maximum number of matches to return.
    context_lines : int
    Number of lines of context to include before and after the match.

    Returns
    -------
    List[Dict]
    A list of matches. Each match contains:
    - file: relative file path
    - line_number: line where the match occurred
    - snippet: surrounding lines for context
    """

    results = []
    query_lower = query.lower()

    # Walk the entire repository tree
    for file_path in repo_root.rglob("*"):
    # Skip directories
        if not file_path.is_file():
            continue
        # Skip binary files and very large files
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        lines = text.splitlines()

        for idx, line in enumerate(lines):
            if query_lower in line.lower():
                start = max(idx - context_lines, 0)
                end = min(idx + context_lines + 1, len(lines))

                snippet = "\n".join(
                    f"{i + 1}: {lines[i]}" for i in range(start, end)
                )

                results.append(
                    {
                        "file": str(file_path.relative_to(repo_root)),
                        "line_number": idx + 1,
                        "snippet": snippet,
                    }
                )

                # Stop early if we reach the result limit
                if len(results) >= max_results:
                    return results

    return results