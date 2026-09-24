# Troubleshooting

No device runtime logs or field test results were supplied, so known device-specific faults and verified fixes are not available yet. When reporting a problem, include the exact board, OS, Python and package versions, command, complete error text with credentials removed, camera status, and relevant GPIO wiring. Do not probe motor pins while powered until the driver circuit and pin mapping are confirmed. If no signal is detected, the repository copy sets traffic state to `NONE` for that frame; it does not debounce or validate repeated detections.
