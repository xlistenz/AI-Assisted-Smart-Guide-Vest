# Architecture

## Intended concept

The project brief describes a camera-based assistive vest that should detect zebra crossings and pedestrian signal states, then provide voice and vibration cues. Raspberry Pi, Camera Module 3, GPIO, audio, microphone, and portable power are named as the design direction.

## What is verified in this workspace

- A YOLO11s training artifact and its training arguments are present.
- Source label exports describe three classes, not the five-class target.
- `src/main.py` implements Picamera2 capture, YOLO inference, basic generic red/green state handling, crosswalk-center zones, GPIO motor/LED outputs, button toggles, and encoded voice-module triggers.
- No route/navigation API, pedestrian-vs-vehicle signal classification, electrical motor driver details, or physical-device validation record was found.

The program provides a prototype control loop, but the label metadata and signal classes do not establish pedestrian-only signal recognition. Do not treat it as a completed or validated accessibility/safety system.
