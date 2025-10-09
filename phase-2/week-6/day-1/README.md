# 📘 Week 6 - Day 1: Person Detection (Simulation Mode)
## 🎯 Objective

The goal of this day was to begin Phase 2 of the Vision Module — specifically, implementing Person Detection in simulation mode.
Since hardware (OAK-D Lite) is still pending delivery, this week focuses on developing and testing person detection logic using a webcam.

## 🧩 Key Updates

- Added detect_person_simulation() method to modules/vision.py.

- The method uses the laptop webcam to simulate person detection.

- Random bounding boxes labeled as "person" are drawn dynamically on the webcam feed.

- Designed to mimic real detection flow and visualize bounding boxes in real-time.

## 🧠 Technical Details

- Input: Laptop webcam (OpenCV capture)

- Output: Live video feed with dummy person boxes

- Dependencies:

**depthai (for pipeline consistency)**

- opencv-python

- numpy

- random

## 🧪 Run Command

To start the webcam simulation:

- python3 -m modules.vision


Then:

- Wait for the webcam window to open

- Observe random person detections drawn in green boxes

- Press q to exit the simulation

## 🧭 Summary
Component	Description
Mode	Simulation (Webcam)
Function Added	detect_person_simulation()
Purpose	Begin person detection phase without OAK-D hardware
Status	✅ Successfully tested on webcam