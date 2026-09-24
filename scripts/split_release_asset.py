#!/usr/bin/env python3
"""Split a large binary into bounded GitHub Release parts without changing it."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

DEFAULT_PART_BYTES = 1_500_000_000
CHUNK_BYTES = 8 * 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--part-bytes", type=int, default=DEFAULT_PART_BYTES)
    args = parser.parse_args()
    if not args.source.is_file() or args.part_bytes <= 0:
        parser.error("source must be a file and --part-bytes must be positive")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    size = args.source.stat().st_size
    count = (size + args.part_bytes - 1) // args.part_bytes
    targets = [args.output_dir / f"{args.source.name}.part{index:02d}" for index in range(1, count + 1)]
    if any(path.exists() for path in targets):
        parser.error("refusing to overwrite an existing release part")

    original_hash = hashlib.sha256()
    with args.source.open("rb") as source:
        for target in targets:
            remaining = min(args.part_bytes, size - source.tell())
            part_hash = hashlib.sha256()
            with target.open("xb") as output:
                while remaining:
                    block = source.read(min(CHUNK_BYTES, remaining))
                    if not block:
                        raise OSError("unexpected end of source archive")
                    output.write(block)
                    original_hash.update(block)
                    part_hash.update(block)
                    remaining -= len(block)
            print(f"{target.name}\t{target.stat().st_size}\tSHA256 {part_hash.hexdigest()}")
    print(f"Original {args.source.name}\t{size}\tSHA256 {original_hash.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
