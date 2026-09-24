# Hardware bill of materials

This table preserves the supplied contest and repair inventory. Quantities and descriptions are transcribed from the provided list; presence in a contest kit does not establish that a part is installed in the vest. Project-specific integration status is marked pending unless confirmed in the project brief.

## Competition presentation kit

| Category | Item | Qty. | Purpose / note |
| --- | --- | ---: | --- |
| Showcase | Completed project | 1 | Details and final build photos not supplied |
| Power | Raspberry Pi battery case | 2 | Compatibility and use in final vest pending confirmation |
| Power | Adapter for Raspberry Pi battery case | 2 | Rating not supplied |
| Power | 18650 lithium battery | 12 | Insulate terminals and pack separately as stated in source list |
| Power | Four-slot lithium battery charger | 1 | Charger specification not supplied |
| Display | Poster | 1 | Public redistribution rights not confirmed |
| Display | Tri-fold leaflet | 250 | Public redistribution rights not confirmed |
| Demo | Laptop | 3 | Demo use |
| Demo | Computer with Q/A supplemental materials | 1 | Storage item; contents not supplied |
| Display | National flag | 1 | Country not specified in source list |
| Display | Science outreach banner | 1 | Dimensions and content not supplied |
| Demo | TV set-top box with remote and two USB-to-DC leads | 1 | Not identified as a vest component |
| Demo | HDMI-to-HDMI Mini cable | 1 | Demo connection |
| Demo | HDMI cable | 2 | Demo connection |
| Demo | USB male-to-male cable | 2 | Electrical use must be checked before connecting |
| Demo | Video capture device | 1 | Demo equipment |
| Supplies | Double-sided tape | 2 | Unit not specified |
| Outreach | Small souvenirs | 100 | Item not specified |
| Tools | Scissors | 1 | Presentation kit |
| Audio | USB speaker | 1 | Audio output candidate; vest integration pending confirmation |
| Power | 12 V adapter for set-top box | 1 | Set-top box use |

## Repair materials and tools

| Category | Item | Qty. | Purpose / note |
| --- | --- | ---: | --- |
| Compute | Raspberry Pi with cooling fan | 1 | OS and environment reportedly preconfigured; exact model in this inventory not stated |
| Storage | MicroSD card | 1 | OS and environment reportedly preconfigured |
| Audio | Voice module | 2 | Firmware flashed and IR learning completed per source list |
| Compute | D1 Mini development board | 2 | Integration not confirmed |
| Sensor | Ultrasonic module | 6 | Repair inventory; current design brief says ultrasonic is not used |
| Sensor | Ultrasonic sensor board | 1 | Repair inventory; current design brief says ultrasonic is not used |
| Tools | Battery-powered soldering iron | 1 | Repair tool |
| Tools | Diagonal cutters | 1 | Repair tool |
| Tools | Digital multimeter | 1 | Repair tool |
| Controls | Button with cap | 3 | Integration not confirmed |
| IR | Infrared emitter diode | 5 | Repair inventory |
| IR | Infrared receiver module | 5 | Repair inventory |
| Indicators | LED | 5 | Repair inventory |
| Supplies | Solder | Some | Quantity not specified |
| Tools | Phillips screwdriver | 1 | Repair tool |
| Wiring | Solid-core wire | Some | Quantity/gauge not specified |
| Wiring | Stranded wire | Some | Quantity/gauge not specified |
| Connectors | PH 2 mm 2-pin, 3-pin, and 4-pin connectors with leads | 3 each | Repair inventory |
| Connectors | 2.54 mm breakaway female header | 2 | Repair inventory |
| Audio | Speaker | 2 | Integration not confirmed |
| Audio | Microphone | 2 | Integration not confirmed |
| Tools | Hot glue gun with three glue sticks | 1 | Source notes supply must support AC 220 V |
| Display | OLED module | 3 | Integration not confirmed |
| Compute | USB-to-UART adapter with Micro USB cable | 2 | Repair inventory |
| IR | Infrared detector module | 2 | Repair inventory |
| Supplies | Heat-shrink tubing | Some | Quantity not specified |
| Supplies | Binder clip | 2 | Repair inventory |

## Design brief items to verify against the physical build

The project brief separately names Raspberry Pi 5 2GB, Raspberry Pi Camera Module 3, GPIO, vibration motors, speaker/audio output, microphone, power bank or power module, wiring, and the vest body. Exact quantities, model numbers, wiring, and whether each item is present in the current build are **TBD**. No prices were supplied.

## Interfaces referenced in the supplied program

The program configures two buttons, three motor outputs, two indicator outputs, and four voice-module inputs using BCM numbering. This confirms software pin assignments only; it does not confirm that physical parts, driver circuits, or wiring are present and functional. The camera is accessed through Picamera2. A microphone is not used by this program.
