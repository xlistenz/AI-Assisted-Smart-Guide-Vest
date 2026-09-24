# Development notes

The current repository includes one Raspberry Pi prototype entry point, model/data artifacts, and project documentation. Additional application modules, package lock/version constraints, and a verified Raspberry Pi runtime are not available.

When implementation source is added:

- Centralize real GPIO mappings in one configuration module.
- Keep credentials outside source control; document variable names in `.env.example` only.
- Preserve the dataset class IDs and require an explicit, documented conversion to change them.
- Separate device-independent vision/decision logic from GPIO and audio adapters.
- Document actual hardware, supported OS/runtime versions, and observed limitations.
- Add tests only for behavior that exists and can be exercised safely.
