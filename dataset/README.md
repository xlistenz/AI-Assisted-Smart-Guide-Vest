# Dataset status and downloads

## Published dataset archives

The two original exports selected for the project are published as GitHub Release assets:

| Archive | Size | Download | Release |
| --- | ---: | --- | --- |
| Primary Label Studio export | 2,676,999,967 bytes | [Part 1](https://github.com/xlistenz/AI-Assisted-Smart-Guide-Vest/releases/download/v0.1.0/data.zip.part01) + [Part 2](https://github.com/xlistenz/AI-Assisted-Smart-Guide-Vest/releases/download/v0.1.0/data.zip.part02) | `v0.1.0` |
| Secondary YOLO export | 199,120,755 bytes | [Download the archive](https://github.com/xlistenz/AI-Assisted-Smart-Guide-Vest/releases/download/v0.1.0/dataset-small-data.zip) | `v0.1.0` |

Prepared asset checksums:

| Release asset | Bytes | SHA-256 |
| --- | ---: | --- |
| [`data.zip.part01`](https://github.com/xlistenz/AI-Assisted-Smart-Guide-Vest/releases/download/v0.1.0/data.zip.part01) | 1,500,000,000 | `38dac5f09304dc54d882f8f39862b66dae63e1ed8c4a94d37195778fdb7f4ae8` |
| [`data.zip.part02`](https://github.com/xlistenz/AI-Assisted-Smart-Guide-Vest/releases/download/v0.1.0/data.zip.part02) | 1,176,999,967 | `c7dfb807137d41d2973d4305e2a61af56ace00270f2e89223ccabb9d04ba8c84` |
| Reassembled `data.zip` | 2,676,999,967 | `878d7d8866c9872fe1d59b50a48d206b31dc92ea2741b73f3f991914255bad10` |
| [`dataset-small-data.zip`](https://github.com/xlistenz/AI-Assisted-Smart-Guide-Vest/releases/download/v0.1.0/dataset-small-data.zip) | 199,120,755 | `4f446ab3f33c74227955b8e8221a8658bde09096f9b28476ae48519a38eb1908` |

After downloading the two large-file parts, restore the original ZIP without overwriting an existing file:

```bash
python scripts/join_release_parts.py --output data.zip data.zip.part01 data.zip.part02
```

The original archives remain unchanged at their source locations. The 2.67 GB ZIP exceeds GitHub Free/Pro's 2 GB Git LFS per-file limit, while each Release asset must be under 2 GiB; splitting preserves its content and permits reconstruction.

## Existing source metadata

The primary Label Studio export contains 554 image files and 572 annotation text files, plus `classes.txt` and `notes.json`. The annotation rows contain polygon coordinates rather than the five-field detection boxes expected by the supplied `task='detect'` program. After decoding the source filenames, a read-only scan found 554 images with labels, 13 duplicate label stems, zero malformed polygon rows, and no unreadable images. Class IDs are `0: 533`, `1: 82`, and `2: 254` annotated polygons. Its category metadata says `0 Crosswalk`, `1 Green light`, `2 Red light`.

The 199 MB export contains 128 image files and 147 annotation text files, plus metadata. After extraction and read-only checking, 19 label stems had no image, 15 image stems and 15 label stems were duplicated, two polygon rows had coordinates outside `[0,1]`, and three groups of images had identical contents. No images were unreadable. Its metadata says `0 cross road`, `1 green light`, `2 red light`. Neither export distinguishes pedestrian signals from vehicle signals.

Separately, the extracted `images/` and `labels/` directories in the primary workspace contain 554 matched image/label pairs in YOLO detection format. A read-only scan found 845 boxes, all with class ID 0, four groups of byte-identical images, and no unreadable images. Its `classes.txt` lists `Green light`, `Red light`, `Crosswalk`, making class ID 0's meaning conflict with the other export. This extracted set was not selected as a release asset.

The primary workspace `classes.txt` contains a different three-line order (`Green light`, `Red light`, `Crosswalk`). These metadata sources conflict with one another and with the requested five-class target in [`classes.txt`](classes.txt). Do not overwrite source labels or treat these exports as the requested five-class dataset.

The supplied exports do not document train/validation/test splits or redistribution licenses. Image sources and permissions are not established in the available files. The dataset should not be described as fully reproducible or unrestricted until provenance and licensing are confirmed.

## Validation

After extracting an export into a directory containing `images/` and `labels/`, install the optional validation dependency and run:

```bash
python -m pip install -r requirements-validation.txt
python scripts/check_dataset.py --root /path/to/extracted/export --task segment
```

The check is read-only and validates either YOLO detection rows (`--task detect`, class ID plus four normalized box values) or YOLO segmentation rows (`--task segment`, class ID plus normalized polygon coordinates). It reports missing image/label pairs, malformed/out-of-range rows, duplicate file contents, and images Pillow cannot decode. Label Studio's encoded source filenames are normalized for image pairing. The script does not rewrite or remove source files. It can inspect a ZIP directory table using `--zip`; add `--verify-zip` to read and CRC-check all members. A three-class export may pass format checks while still failing the five-class mapping requirement.

## Training

[`data.yaml`](data.yaml) documents the target five-class order and expected split paths only. It is not ready for training until a verified, converted dataset exists at those paths and its annotations use the prescribed IDs. Do not remap IDs by inference from English class names.
