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

DepthAI SDK (v2.30.0) → Builds real-time vision pipeline.

YOLOv8n Model (COCO dataset) → Detects common objects with bounding boxes and depth data.

Mac TTS (Text-to-Speech) → Gives audio feedback for detected objects.

OpenCV → Displays bounding boxes and object labels.