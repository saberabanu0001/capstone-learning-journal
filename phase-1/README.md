# 🚀 Phase 1 – Vision System Development

Project: AI Rover (Capstone Robotics Project)
Owner: Sabera Banu
**Duration: Weeks 1–5**
Goal: Build the foundational Vision Module for the rover using OAK-D (DepthAI)

## 📖 Phase Overview

Phase 1 focused on designing, implementing, and testing the Vision System, which enables the robot to "see" and understand its environment through RGB and depth perception.

#### Key outcomes:

- Built modular and testable VisionSystem class

- Integrated YOLO-based object detection

- Simulated OAK-D functions using webcam or dummy data for development before hardware arrival

## ⚙️ Weekly Progress
**Week	Focus	Achievements**
Week 1–2	Environment Setup	Installed DepthAI SDK, set up virtual environment
Week 3	Depth Pipeline	Created and tested stereo depth + center distance calculation
Week 4	Vision Foundation	Implemented frame capture and core vision architecture
Week 5	Object Detection	Integrated YOLO for detection + spatial depth estimation
## 🧩 VisionSystem Overview

Core methods implemented:

class VisionSystem:
    def get_latest_frame()         # Capture RGB frame
    def get_center_depth()         # Get depth at image center
    def get_detections_with_depth()# YOLO detection + spatial data


Simulation mode ensures full functionality even without OAK-D hardware.

## 🧪 Test Modules
Test File	Description
test_camera.py	RGB frame capture
test_depth.py	Depth reading
test_yolo.py	YOLO object detection
test_integration.py	Combined module verification

Run test:

python3 -m test.test_camera

## 📊 Phase-1 Outcome

✅ Vision module successfully implemented and verified in simulation mode.
🧠 Ready for hardware testing on Jetson + OAK-D in Phase 2.
⚙️ Structured and modular design for easy integration with Audio and Motor systems.

🔮 Next Phase (Phase 2 – Integration)

Connect OAK-D hardware and validate real-time detections

Integrate vision with motion control

Enable decision-making using detection + depth data