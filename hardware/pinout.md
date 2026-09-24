# GPIO pinout

The BCM assignments below come from `src/main.py`. Physical header numbers and electrical connections were not supplied, so those fields remain pending.

| BCM GPIO | Physical pin | Connected part | Active state / purpose | Evidence source |
| ---: | --- | --- | --- | --- |
| 4 | 待補充 | Master button | Input, pull-up; falling edge toggles ready/sleep | `src/main.py` |
| 25 | 待補充 | Action/navigation button | Input, pull-up; falling edge toggles target guidance | `src/main.py` |
| 17 | 待補充 | Left motor driver | HIGH when crosswalk target center is left of x=280 and guidance is active | `src/main.py` |
| 27 | 待補充 | Center motor driver | HIGH for center-zone target when signal is GREEN | `src/main.py` |
| 22 | 待補充 | Right motor driver | HIGH when target center is right of x=360 and guidance is active | `src/main.py` |
| 23 | 待補充 | Red indicator | HIGH when detected state is RED during guidance | `src/main.py` |
| 24 | 待補充 | Green indicator | HIGH when detected state is GREEN during guidance | `src/main.py` |
| 12 | 待補充 | Voice module B3 | Encoded voice trigger | `src/main.py` |
| 26 | 待補充 | Voice module A27 | Encoded voice trigger | `src/main.py` |
| 19 | 待補充 | Voice module A26 | Encoded voice trigger | `src/main.py` |
| 13 | 待補充 | Voice module A25 | Encoded voice trigger | `src/main.py` |

The code calls `GPIO.setmode(GPIO.BCM)`. Physical pin numbers, driver circuit, polarity, current limits, ground, and voice-module pin labels must be confirmed from the actual assembled device. Do not treat these GPIO assignments as wiring instructions. The code's left/right voice section comments may not match target direction and require an in-place test before use.
