# Installation

## Current limitation

The supplied program is [`src/main.py`](../src/main.py). It was inspected statically but not run: this workspace is not a Raspberry Pi and has no camera or GPIO hardware attached. The exact Raspberry Pi OS/Python versions and tested package versions were not supplied, so the instructions below are a starting point rather than a verified installation recipe.

## Required information before an install guide can be completed

- Raspberry Pi model and supported Raspberry Pi OS release for the actual build.
- Camera interface and operating-system camera setup.
- Python version and pinned dependencies.
- Verified model path and inference invocation.
- GPIO numbering and motor driver wiring.
- Audio device setup and any speech-service configuration.
- Navigation/API requirements and names of environment variables (never the secret values).
- A safe startup, shutdown, and troubleshooting procedure.

## Python dependencies

The project lists `numpy`, `opencv-python`, and `ultralytics` in `requirements.txt`. Picamera2 and RPi.GPIO are hardware/OS-specific and are not installed from that file; install them using the package source documented for the chosen Raspberry Pi OS release. Compatibility between the pip OpenCV wheel, Raspberry Pi OS packages, and Picamera2 has not been tested.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Do not install hardware libraries or run the model on a Pi based only on the training configuration. First verify the board, OS camera stack, wiring, and motor driver. The model is experimental and its class mapping does not match the five-class target specification.

## Launch

The program expects a camera, BCM GPIO buttons, LEDs, vibration motor drivers, and a compatible voice module. The default model path is `models/my_model.pt`; override it with the `MODEL_PATH` environment variable. After confirming the hardware and model are appropriate for a controlled bench test, the entry point is `python src/main.py`. This command has not been run against hardware.
