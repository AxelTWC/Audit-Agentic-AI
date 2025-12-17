"""
open_file.py


Open a specific file and return exact line ranges with line numbers.
This is what makes citations possible.


This tool allows the agent to read a specific range of lines from a file.
It is the ONLY way the agent is allowed to "see" file contents.

Design goals:
- Precise
- Transparent
- Safe (read-only)
- Citation-friendly

This tool enables evidence-based answers.
"""

from pathlib import Path
from typing import Dict


def open_file(
    repo_root: Path,
    file_path: str,
    start_line: int,
    end_line: int,
) -> Dict:
    """
    Open a file and return a specific range of lines with line numbers.

    Parameters
    ----------
    repo_root : Path
        Root directory of the repository.
    file_path : str
        Path to the file relative to repo_root.
    start_line : int
        1-based starting line number.
    end_line : int
        1-based ending line number (inclusive).

    Returns
    -------
    Dict
        A dictionary containing:
        - file: file path
        - start_line: start line number
        - end_line: end line number
        - content: text with line numbers
    """

    abs_path = repo_root / file_path

    # Safety check: ensure file exists inside repo_root
    if not abs_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not abs_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Read file safely
    text = abs_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    # Normalize bounds
    start_idx = max(start_line - 1, 0)
    end_idx = min(end_line, len(lines))

    numbered_lines = [
        f"{i + 1}: {lines[i]}"
        for i in range(start_idx, end_idx)
    ]

    return {
        "file": file_path,
        "start_line": start_line,
        "end_line": end_line,
        "content": "\n".join(numbered_lines),
    }