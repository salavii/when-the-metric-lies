"""Verify the four frozen coverage reference files by SHA-256.

Usage:
    python verify_references.py

Recomputes the SHA-256 of each file in references/ and compares it with the
value expected for that reference version. Exits with status 0 if all four
match and 1 otherwise. Standard library only.
"""

import hashlib
import sys
from pathlib import Path

REFERENCES = Path(__file__).resolve().parent / "references"

# version, paper label, file name, expected SHA-256
EXPECTED = [
    ("v1", "H1", "eval_reference_union.json",
     "7ca04545ed124960072574751babbfdf6271f961dfb159f39f9733ef207ddf40"),
    ("v2", "H2", "eval_reference_union_v2_20260818.json",
     "1ff27271a429a94ad42c734bf8504ffe1e563497f75ccfc5b29938240182e641"),
    ("v3", "H3", "eval_reference_union_v3_20260819.json",
     "e7146ced6e8d317e5971da30ad70150d45459203a01a486d069fcd59e362c6a6"),
    ("v4", "H4", "eval_reference_union_v4_20260822.json",
     "4b364bfff47a58d81126afe5f5389ea365ab2e8e4085cf9fe5cde37540dc0376"),
]


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    failures = 0
    for version, label, name, expected in EXPECTED:
        path = REFERENCES / name
        if not path.is_file():
            status, actual = "MISSING", "-"
        else:
            actual = sha256(path)
            status = "OK" if actual == expected else "MISMATCH"
        if status != "OK":
            failures += 1
        print(f"{status:<9}{version} ({label})  {name}")
        print(f"         expected {expected}")
        print(f"         actual   {actual}")
    print()
    if failures:
        print(f"{failures} of {len(EXPECTED)} reference files failed verification.")
        return 1
    print(f"All {len(EXPECTED)} reference files match.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
