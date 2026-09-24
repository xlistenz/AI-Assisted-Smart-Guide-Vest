# Wiring

The application code contains BCM GPIO assignments, but no wiring diagram, physical pin mapping, or motor-driver circuit was present in the inspected workspace. Do not connect hardware based on guessed electrical details.

| Raspberry Pi BCM GPIO / physical pin | Component | Function | Status |
| --- | --- | --- | --- |
| BCM 17 / physical pin TBD | Left motor driver | Left-zone target cue | BCM number appears in code; circuit and physical pin unverified |
| BCM 27 / physical pin TBD | Center motor driver | Center target cue | BCM number appears in code; circuit and physical pin unverified |
| BCM 22 / physical pin TBD | Right motor driver | Right-zone target cue | BCM number appears in code; circuit and physical pin unverified |
| BCM 23 / physical pin TBD | Red indicator | Red detection status | BCM number appears in code; circuit and physical pin unverified |
| BCM 24 / physical pin TBD | Green indicator | Green detection status | BCM number appears in code; circuit and physical pin unverified |
| BCM 4 / physical pin TBD | Master button | Toggle ready/sleep | BCM number appears in code; switch wiring unverified |
| BCM 25 / physical pin TBD | Action button | Toggle visual guidance | BCM number appears in code; switch wiring unverified |
| BCM 12, 26, 19, 13 / physical pins TBD | Voice module inputs | Encode voice-section triggers | BCM numbers appear in code; input order/electrical levels unverified |
| CSI / connector not documented | Camera | Capture frames through Picamera2 | Camera Module 3 is named in brief; actual module not verified in source |
| TBD | Speaker/audio module | Voice output | Program pulses voice module; output device wiring not documented |
| TBD | Microphone | Voice input, if present | Not used by supplied program |

Before adding a wiring diagram, record the Raspberry Pi board revision, supply voltage/current, driver circuit for each motor, common ground, connector pinout, and safe power-off procedure. Do not power a motor directly from a GPIO pin. The supplied program uses BCM numbering and performs static output toggling; hardware polarity and direction must be checked on the physical build.
