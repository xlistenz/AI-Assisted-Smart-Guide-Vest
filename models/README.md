# Model artifact

The workspace contains `my_model.pt` (19,182,490 bytes) and a YOLO training run with `best.pt` and `last.pt` (both 19,182,490 bytes). One copy is included here. The other run files remain in the original workspace.

The supplied training record (`train/args.yaml`, not included in this repository) specifies `model: yolo11s.pt`, `imgsz: 640`, `epochs: 80`, and `data: /content/data.yaml`. Historical results and evaluation plots are included under `assets/screenshots/`.

The source class metadata includes only three categories and disagrees on their order. The target specification has five categories. The checkpoint's class mapping has not been independently verified, so this model must not be presented as a five-class model. Its confidence threshold, supported inference runtime, and performance on a held-out set are not established here.

The supplied program's default model path is `models/my_model.pt`; `MODEL_PATH` can override it. The source selects `task='detect'`. The model's class names and mapping were not read from the binary, so its suitability for the code's class-name checks remains unverified. Its license and the licenses of its training images have not been supplied; redistribution permission is pending confirmation. Do not assume that the repository's MIT license applies to this model.

## Reproduction status

The available configuration records an 80-epoch YOLO11s training run at 640 pixels, but the referenced `/content/data.yaml` is not included and the dataset splits are not documented. Exact training cannot yet be reproduced. The inference entry point is `src/main.py`; running it requires Raspberry Pi camera/GPIO hardware and the matching model.
