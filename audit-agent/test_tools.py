"""Test script for search_repo and open_file tools."""

from pathlib import Path
from agent.tools.search import search_repo
from agent.tools.open_file import open_file

# Point to the audit-agent repository itself as test data
repo = Path(__file__).parent

print("=" * 60)
print("Testing search_repo and open_file tools")
print("=" * 60)

# Test 1: Search for "def" in the repository
print("\n[Test 1] Searching for 'def' in the repository...")
matches = search_repo(repo, "def", max_results=5)
print(f"Found {len(matches)} matches:\n")

for i, match in enumerate(matches[:3]):
    print(f"Match {i+1}:")
    print(f"  File: {match['file']}")
    print(f"  Line: {match['line_number']}")
    print(f"  Snippet:\n{match['snippet']}\n")

# Test 2: Open a specific file range
if matches:
    first_match = matches[0]
    file_path = first_match["file"]
    line_num = first_match["line_number"]
    
    print("=" * 60)
    print(f"[Test 2] Opening {file_path} from line {max(1, line_num-5)} to {line_num+10}...")
    print("=" * 60)
    
    try:
        file_view = open_file(repo, file_path, max(1, line_num - 5), line_num + 10)
        print(f"\nFile: {file_view['file']}")
        print(f"Lines {file_view['start_line']}-{file_view['end_line']}:")
        print(file_view["content"])
    except Exception as e:
        print(f"Error: {e}")

# Test 3: Search for "Path" 
print("\n" + "=" * 60)
print("[Test 3] Searching for 'Path' (commonly used imports)...")
print("=" * 60)

matches = search_repo(repo, "Path", max_results=5)
print(f"Found {len(matches)} matches:\n")

for i, match in enumerate(matches[:2]):
    print(f"Match {i+1}:")
    print(f"  File: {match['file']}")
    print(f"  Line: {match['line_number']}")
    print(f"  Snippet:\n{match['snippet']}\n")
