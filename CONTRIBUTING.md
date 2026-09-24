# Contributing

Contributions are welcome. Please keep prototype behavior, verified hardware facts, and future plans clearly distinguished.

## Development setup

The repository includes the prototype entry point at `src/main.py` and a basic `requirements.txt`. The hardware-specific environment has not been verified, so the install notes are a starting point rather than a tested setup. When changing source code, keep dependencies documented and state the operating system and Raspberry Pi model used for validation. Do not add credentials; use environment variables and document their names in `.env.example` only.

## Changes and issues

- Open an issue describing the observed behavior, hardware, OS, and reproducible steps. Remove API keys and personal data from logs.
- Keep pull requests focused and describe the hardware/software setup used to validate them.
- Use clear names and follow existing style. For Python changes, document syntax, import, and hardware checks that were performed; do not present desktop checks as hardware validation.

## Dataset rules

- Preserve class IDs and order in `dataset/classes.txt`.
- Do not silently remap, remove, or relabel source annotations. Submit a documented conversion as a separate derived dataset.
- Before adding images or annotations, verify redistribution rights, remove private or identifying material where appropriate, record provenance, and provide a dataset license.
- Keep source exports immutable. Store generated splits and derived data outside the Git history unless their size and license permit distribution.

## Safety claims

Do not describe planned features as implemented or imply that the vest guarantees safe crossing. Report actual hardware, test conditions, limitations, and failures.
