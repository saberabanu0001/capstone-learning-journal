# 📖 Week-4 Day-4 — YOLO + Depth
## 🎯 Goal

Upgrade the VisionSystem to use YOLO object detection + depth, while keeping earlier functions.
#### 👉 The robot can now know:

 - What object is detected (YOLO class)

 - How confident the detection is

 - Where it is in 3D space (X, Y, Z in mm)

 ---

## 🧩 What I Did

 - Extended modules/vision.py with 3 core functions:

- get_latest_frame() → live RGB frame (Day-2)

- get_center_depth() → distance at image center (Day-3)

 - get_detections_with_depth() → YOLO detections + depth (Day-4)
---

### Created ** test_vision_day4.py** :

- Displays RGB feed in OpenCV window.

- Prints center depth values.

- Prints YOLO detections with spatial coordinates.

---

### 📂 Files Created / Updated

- modules/vision.py → VisionSystem with YOLO + depth

- test_vision_day4.py → test script for all 3 functions

---

### ▶️ How to Run

- Activate environment:

**source depthai-env/bin/activate**


- Run test:

**python3 test_vision_day4.py**


- Quit with q.

### 🖥️ Output (Simulation Mode)

---

**Terminal:**

[Depth] Center depth: 1.72 meters
[YOLO] person (91.0%) at X=20mm, Y=120mm, Z=2400mm
[YOLO] dog (78.0%) at X=-60mm, Y=30mm, Z=1800mm

---


**Window:**

- RGB feed (blank in simulation).

- Real camera video when hardware is connected.

---

## ✅ Learning Outcome

- Learned how to integrate YOLO detection on OAK-D Lite.

- Combined detection + spatial info → each object has 3D coordinates.

- Finished VisionSystem v1.0 → reusable for the robot’s main program.

---

## 🚀 Next Step

- Optimize for person-only detection (e.g., Intel’s person-detection-0013 or YOLOv5 “person” class).

- Integrate with Jetson main code:

**[OAK-D Lite] → [VisionSystem] → [main.py on Jetson] → [Robot reacts]**
