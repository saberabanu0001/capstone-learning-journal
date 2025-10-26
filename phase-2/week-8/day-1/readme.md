# 🧾 Vision & Voice System for Capstone Robot
## 📌 Project Overview

This module is part of the Capstone Robot Project developed at Sejong University.
It integrates real-time computer vision and voice feedback using an OAK-D Lite AI camera and DepthAI SDK, designed to give the robot spatial awareness and vocal interaction capability.

**Over the past two days, we built and tested:**

- A real-time object detection system (YOLOv8n Spatial Detection Network).

- A macOS-compatible voice alert system that speaks detected objects aloud.

- A modular DepthAI pipeline compatible with SLAM and future motion systems.




## ⚙️ System Architecture

**Components:**

- OAK-D Lite Camera → Provides RGB + Depth input.

- DepthAI SDK (v2.30.0) → Builds real-time vision pipeline.

- YOLOv8n Model (COCO dataset) → Detects common objects with bounding boxes and depth data.

- Mac TTS (Text-to-Speech) → Gives audio feedback for detected objects.

- OpenCV → Displays bounding boxes and object labels.



## 🎯 Key Features
## Feature	Description
- 🎥 Object Detection	- Detects people, bottles, cups, plants, and phones in real time.
- 🧠 Spatial Awareness	- Measures distance (depth) of objects from the robot camera.
- 🗣️ Voice Announcements	- The robot audibly announces detected objects and their distance (macOS say command).
- 📦 Threaded Detection Queue	- Processes detections in parallel for smooth real-time updates.
- ⚡ Modular Code	- Vision and voice modules separated for easy integration with SLAM and motion control.
- 🌗 Lighting Adjustment	- Automatic frame normalization for better low-light detection.



## 🗣️ Voice Functionality (macOS)

### The voice module uses:

***subprocess.Popen(['say', phrase])***


#### Example output:

***“Person detected 1.2 meters away.”***

#### It triggers when:

***Confidence ≥ 70%***

- At least 4 seconds have passed since the last spoken alert for the same label

- This ensures natural feedback without repetition or lag.


## 📍 Detected Object Labels

- Currently detecting objects from:

- ***TARGET_LABELS = ["person", "bottle", "cup", "cell phone", "potted plant", "pen"]***


- More labels can easily be added later for fine-tuning.


## 🧩 Technical Notes

- Model used: yolov8n_coco_640x352.blob

- Resolution: 640×352 @ 30 FPS

- Confidence threshold: 0.4 (adjustable for smaller object detection)

- Tested on: MacBook M4 with Python 3.9 and DepthAI 2.30.0



## 🚀 Next Steps

- Fine-Tune YOLOv8 for lab-specific objects (robot parts, bottles, chairs, humans, etc.)

- Integrate SLAM (Simultaneous Localization and Mapping) for autonomous navigation.

- Add gesture recognition or motion tracking for user interaction.

- Replace voice system with a cross-platform version (optional).
