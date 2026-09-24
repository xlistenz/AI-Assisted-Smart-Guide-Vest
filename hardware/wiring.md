# Wiring

The application code contains BCM GPIO assignments, but no wiring diagram, physical pin mapping, or motor-driver circuit was present in the inspected workspace. Do not connect hardware based on guessed electrical details.

| Raspberry Pi BCM GPIO / physical pin | Component | Function | Status |
| --- | --- | --- | --- |
| BCM 17 / physical pin 待補充 | Left motor driver | Left-zone target cue | BCM number appears in code; circuit and physical pin unverified |
| BCM 27 / physical pin 待補充 | Center motor driver | Center target cue | BCM number appears in code; circuit and physical pin unverified |
| BCM 22 / physical pin 待補充 | Right motor driver | Right-zone target cue | BCM number appears in code; circuit and physical pin unverified |
| BCM 23 / physical pin 待補充 | Red indicator | Red detection status | BCM number appears in code; circuit and physical pin unverified |
| BCM 24 / physical pin 待補充 | Green indicator | Green detection status | BCM number appears in code; circuit and physical pin unverified |
| BCM 4 / physical pin 待補充 | Master button | Toggle ready/sleep | BCM number appears in code; switch wiring unverified |
| BCM 25 / physical pin 待補充 | Action button | Toggle visual guidance | BCM number appears in code; switch wiring unverified |
| BCM 12, 26, 19, 13 / physical pins 待補充 | Voice module inputs | Encode voice-section triggers | BCM numbers appear in code; input order/electrical levels unverified |
| CSI / connector not documented | Camera | Capture frames through Picamera2 | Camera Module 3 is named in brief; actual module not verified in source |
| 待補充 | Speaker/audio module | Voice output | Program pulses voice module; output device wiring not documented |
| 待補充 | Microphone | Voice input, if present | Not used by supplied program |

Before adding a wiring diagram, record the Raspberry Pi board revision, supply voltage/current, driver circuit for each motor, common ground, connector pinout, and safe power-off procedure. Do not power a motor directly from a GPIO pin. The supplied program uses BCM numbering and performs static output toggling; hardware polarity and direction must be checked on the physical build.
