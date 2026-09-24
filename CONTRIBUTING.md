# Contributing

Contributions are welcome once the implementation and dataset provenance are documented.

## Development setup

The current workspace does not include the vest application source or a dependency manifest, so a verified development install command is not available yet. When adding source code, include a minimal dependency list and exact setup instructions for the supported operating system and Raspberry Pi model. Do not add credentials; use environment variables and document their names in `.env.example` only.

## Changes and issues

- Open an issue describing the observed behavior, hardware, OS, and reproducible steps. Remove API keys and personal data from logs.
- Keep pull requests focused and describe the hardware/software setup used to validate them.
- Use clear names and follow existing style. Python changes should include syntax and import checks when the implementation is added.

## Dataset rules

- Preserve class IDs and order in `dataset/classes.txt`.
- Do not silently remap, remove, or relabel source annotations. Submit a documented conversion as a separate derived dataset.
- Before adding images or annotations, verify redistribution rights, remove private or identifying material where appropriate, record provenance, and provide a dataset license.
- Keep source exports immutable. Store generated splits and derived data outside the Git history unless their size and license permit distribution.

## Safety claims

Do not describe planned features as implemented or imply that the vest guarantees safe crossing. Report actual hardware, test conditions, limitations, and failures.
