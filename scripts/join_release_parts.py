#!/usr/bin/env python3
"""Reassemble ordered release parts into a new file without overwriting."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

CHUNK_BYTES = 8 * 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("parts", type=Path, nargs="+")
    args = parser.parse_args()
    if not args.parts or any(not part.is_file() for part in args.parts):
        parser.error("all part files must exist")

    digest = hashlib.sha256()
    total = 0
    try:
        with args.output.open("xb") as output:
            for part in args.parts:
                with part.open("rb") as source:
                    for block in iter(lambda: source.read(CHUNK_BYTES), b""):
                        output.write(block)
                        digest.update(block)
                        total += len(block)
    except FileExistsError:
        parser.error("refusing to overwrite an existing output file")
    print(f"Created {args.output} ({total} bytes), SHA256 {digest.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
