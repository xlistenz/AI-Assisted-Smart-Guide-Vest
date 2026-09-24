#!/usr/bin/env python3
"""Read-only checks for a flat YOLO detection dataset (images/ and labels/)."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from urllib.parse import unquote
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_CLASS_ID = 4


def normalized_label_stem(path: Path) -> str:
    """Handle Label Studio names like hash__wico_image%5Cyolo%20%281%29.txt."""
    stem = path.stem
    if "__" in stem:
        stem = unquote(stem.split("__", 1)[1])
        stem = stem[stem.rfind(chr(92)) + 1 :]
    elif re.match(r"^[0-9a-fA-F]{8}-", stem):
        stem = stem.split("-", 1)[1]
    return Path(stem).stem.casefold()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_zip(path: Path, verify_crc: bool) -> int:
    try:
        with zipfile.ZipFile(path) as archive:
            entries = [entry for entry in archive.infolist() if not entry.is_dir()]
            images = [entry for entry in entries if Path(entry.filename).suffix.lower() in IMAGE_EXTENSIONS]
            labels = [entry for entry in entries if Path(entry.filename).suffix.lower() == ".txt"]
            print(f"ZIP: {path}")
            print(f"Files: {len(entries)} | images: {len(images)} | text files: {len(labels)}")
            if verify_crc:
                bad_member = archive.testzip()
                if bad_member:
                    print(f"ERROR: CRC failed for {bad_member}")
                    return 1
                print("ZIP CRC: passed")
            else:
                print("ZIP CRC: not checked (pass --verify-zip to read every archive member)")
            return 0
    except (OSError, zipfile.BadZipFile) as error:
        print(f"ERROR: cannot read ZIP: {error}")
        return 1


def check_directory(root: Path, task: str) -> int:
    image_dir = root / "images"
    label_dir = root / "labels"
    if not image_dir.is_dir() or not label_dir.is_dir():
        print("ERROR: expected images/ and labels/ directories under", root)
        return 1

    images = sorted((p for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS))
    labels = sorted(label_dir.rglob("*.txt"))
    images_by_stem: dict[str, list[Path]] = defaultdict(list)
    labels_by_stem: dict[str, list[Path]] = defaultdict(list)
    for image in images:
        images_by_stem[normalized_label_stem(image)].append(image)
    for label in labels:
        if label.name.casefold() != "classes.txt":
            labels_by_stem[normalized_label_stem(label)].append(label)

    missing_labels = sorted(set(images_by_stem) - set(labels_by_stem))
    missing_images = sorted(set(labels_by_stem) - set(images_by_stem))
    duplicate_image_names = {name: paths for name, paths in images_by_stem.items() if len(paths) > 1}
    duplicate_label_names = {name: paths for name, paths in labels_by_stem.items() if len(paths) > 1}
    invalid_rows: list[tuple[Path, int, str]] = []
    empty_labels: list[Path] = []
    class_counts: Counter[int] = Counter()

    for label in labels:
        if label.name.casefold() == "classes.txt":
            continue
        try:
            lines = label.read_text(encoding="utf-8-sig").splitlines()
        except (OSError, UnicodeError) as error:
            invalid_rows.append((label, 0, f"cannot read: {error}"))
            continue
        rows = [line.strip() for line in lines if line.strip()]
        if not rows:
            empty_labels.append(label)
            continue
        for line_number, row in enumerate(lines, start=1):
            row = row.strip()
            if not row:
                continue
            fields = row.split()
            valid_field_count = len(fields) == 5 if task == "detect" else len(fields) >= 7 and (len(fields) - 1) % 2 == 0
            if not valid_field_count:
                expected = "class plus four box values" if task == "detect" else "class plus at least three (x,y) polygon points"
                invalid_rows.append((label, line_number, f"expected YOLO {task} row: {expected}"))
                continue
            try:
                class_id = int(fields[0])
                box = [float(value) for value in fields[1:]]
            except ValueError:
                invalid_rows.append((label, line_number, "class ID/box contains a non-numeric value"))
                continue
            if not 0 <= class_id <= MAX_CLASS_ID:
                invalid_rows.append((label, line_number, f"class ID {class_id} outside 0..{MAX_CLASS_ID}"))
                continue
            bad_values = any(value < 0 or value > 1 for value in box)
            if task == "detect":
                bad_values = bad_values or box[2] <= 0 or box[3] <= 0
            if bad_values:
                invalid_rows.append((label, line_number, "coordinates must be normalized to [0,1]"))
                continue
            class_counts[class_id] += 1

    duplicate_contents: dict[str, list[Path]] = defaultdict(list)
    unreadable: list[tuple[Path, str]] = []
    try:
        from PIL import Image
    except ImportError:
        Image = None
        print("WARNING: Pillow is not installed; full image decoding check skipped.")

    for image in images:
        try:
            duplicate_contents[sha256(image)].append(image)
            if Image is not None:
                with Image.open(image) as decoded:
                    decoded.verify()
            else:
                with image.open("rb") as stream:
                    header = stream.read(8)
                valid_header = header.startswith(b"\xff\xd8\xff") or header == b"\x89PNG\r\n\x1a\n" or header[:4] == b"RIFF"
                if not valid_header:
                    unreadable.append((image, "unrecognized image header"))
        except Exception as error:  # Image plugins may raise several decoder-specific exceptions.
            unreadable.append((image, str(error)))

    duplicate_contents = {digest: paths for digest, paths in duplicate_contents.items() if len(paths) > 1}
    print(f"Root: {root} | expected task: {task}")
    print(f"Images: {len(images)} | label files: {len(labels_by_stem)} | empty labels: {len(empty_labels)}")
    print(f"Annotated boxes by class ID: {dict(sorted(class_counts.items()))}")
    print(f"Images without labels: {len(missing_labels)} | labels without images: {len(missing_images)}")
    print(f"Duplicate image stems: {len(duplicate_image_names)} | duplicate image contents: {len(duplicate_contents)}")
    print(f"Duplicate label stems: {len(duplicate_label_names)} | malformed/out-of-range rows: {len(invalid_rows)}")
    print(f"Unreadable/corrupt images: {len(unreadable)}")

    for name in missing_labels[:10]:
        print("  Missing label:", name)
    for name in missing_images[:10]:
        print("  Label without image:", name)
    for path, line_number, problem in invalid_rows[:10]:
        print(f"  Invalid label {path}:{line_number}: {problem}")
    for path, problem in unreadable[:10]:
        print(f"  Unreadable image {path}: {problem}")
    for paths in duplicate_contents.values():
        print("  Duplicate image content:", ", ".join(str(path) for path in paths[:5]))

    return 1 if missing_labels or missing_images or invalid_rows or unreadable or duplicate_image_names or duplicate_label_names else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="Extracted dataset directory containing images/ and labels/")
    parser.add_argument("--zip", type=Path, help="Inspect an archive without extracting it")
    parser.add_argument("--task", choices=("detect", "segment"), default="detect", help="YOLO annotation task; default: detect")
    parser.add_argument("--verify-zip", action="store_true", help="Read every ZIP member to verify CRC (can take time)")
    args = parser.parse_args()
    if bool(args.root) == bool(args.zip):
        parser.error("provide exactly one of --root or --zip")
    if args.zip:
        return check_zip(args.zip, args.verify_zip)
    return check_directory(args.root, args.task)


if __name__ == "__main__":
    sys.exit(main())
