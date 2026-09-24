# Workflow

The first six items below are visible in the supplied program by static inspection. They have not been run on the Raspberry Pi or verified against the physical vest.

1. Picamera2 obtains 640×480 frames; the program resizes them to 640×640 for inference.
2. Ultralytics YOLO detects the model's named classes. The code recognizes cross road/crosswalk and generic red/green light labels, but generic signal labels cannot tell a pedestrian signal from a vehicle signal.
3. A detected crosswalk box's horizontal center is smoothed and compared with x=280 and x=360 zones.
4. When guidance is active, the program updates red/green indicators and triggers center/left/right motors and voice-module sections.
5. A red detection can trigger a red voice section, then a wait voice section after two seconds. A green voice section is triggered after a red-to-green state transition.
6. G4 toggles ready/sleep. G25 toggles the visual target guidance loop; it does not call a route API or identify the user's mapped route.
7. Keep the user responsible for checking the physical environment before crossing.

The code contains the described red-to-green voice transition and two-second wait prompt, but no temporal confirmation or signal timeout logic from the source. The repository copy returns to `NONE` on frames with no recognized signal so it will not preserve a stale green state. Route-to-crosswalk matching, mapped-route guidance, and distance thresholds are not implemented.
